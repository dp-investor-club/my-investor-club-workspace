"""텔레그램 채널을 검색하고 첨부 PDF 본문을 읽어주는 MCP 서버 (단독 실행판).

Claude Code가 이 파일을 실행해서 `search_channel` / `get_document_text` 두 도구를 씁니다.
같은 폴더의 .env에서 API 키를, telegram_session.session에서 로그인 정보를 읽습니다.

실행: python server.py   (직접 실행할 일은 없고, Claude Code가 알아서 띄웁니다)
"""

import asyncio
import io
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage
from pypdf import PdfReader
from telethon import TelegramClient

HERE = Path(__file__).resolve().parent
load_dotenv(HERE / ".env")

# 세션 파일은 이 파일과 같은 폴더에 만듭니다. login.py가 한 번 만들어 두면
# 그 뒤로는 로그인 없이 재사용됩니다.
SESSION_PATH = HERE / "telegram_session"
DOC_CACHE_DIR = HERE / "telegram_docs"

# 검색할 채널 목록. 내 텔레그램 계정이 이미 가입한 채널만 검색됩니다.
# 여기를 고치면 내가 보는 채널로 바꿀 수 있습니다.
DEFAULT_CHANNELS = ["DOC_POOL", "bornlupin", "benineb9", "BeOn_BeClear"]

MAX_RESULTS = 15
AUTO_FETCH_DOCUMENTS = 8
TEXT_TRUNCATE = 500
DOC_TEXT_TRUNCATE = 16000

# 리포트 채널은 캡션을 항상 같은 라벨 형식으로 씁니다 — 정규식으로 뽑으면
# PDF를 열지 않고도 제목/작성자/투자의견/목표주가를 알 수 있습니다.
_CAPTION_FIELD_PATTERNS = {
    "category": r"\*\*\[(.*?)\]\*\*",
    "title": r"제목:\s*(.+)",
    "author": r"작성자:\s*(.+)",
    "opinion": r"투자의견:\s*(.+)",
    "target_price": r"목표주가:\s*(.+)",
}

mcp = FastMCP("telegram-search")


def get_credentials() -> tuple[int, str]:
    api_id = os.environ.get("TELEGRAM_API_ID", "")
    api_hash = os.environ.get("TELEGRAM_API_HASH", "")
    if not api_id or not api_hash:
        raise RuntimeError(
            "TELEGRAM_API_ID / TELEGRAM_API_HASH가 없습니다 — "
            f"{HERE / '.env'} 파일에 넣어주세요. https://my.telegram.org 에서 발급합니다."
        )
    return int(api_id), api_hash


def _parse_caption_fields(text: str) -> dict:
    fields = {}
    for key, pattern in _CAPTION_FIELD_PATTERNS.items():
        match = re.search(pattern, text)
        if match:
            fields[key] = match.group(1).strip()
    if "author" in fields:
        broker_match = re.search(r"\((.+?)\)\s*$", fields["author"])
        if broker_match:
            fields["broker"] = broker_match.group(1).strip()
    return fields


def _client() -> TelegramClient:
    api_id, api_hash = get_credentials()
    return TelegramClient(str(SESSION_PATH), api_id, api_hash)


async def _require_authorized(client: TelegramClient) -> None:
    if not await client.is_user_authorized():
        raise RuntimeError(
            "텔레그램 세션이 없음 — 먼저 이 폴더에서 `python login.py`로 로그인해주세요."
        )


def _document_filename(message) -> str | None:
    if not message.document:
        return None
    for attr in message.document.attributes:
        if hasattr(attr, "file_name"):
            return attr.file_name
    return None


def _extract_pdf_text(data: bytes, max_chars: int) -> tuple[int, str, bool]:
    # 리포트가 40쪽이 넘는 경우도 있어 페이지마다 추출하면 느립니다.
    # 필요한 글자 수를 채우면 그 즉시 멈춥니다 — 핵심 수치는 앞쪽에 있습니다.
    reader = PdfReader(io.BytesIO(data))
    total_pages = len(reader.pages)
    chunks: list[str] = []
    collected = 0
    truncated = False
    for page in reader.pages:
        chunks.append(page.extract_text() or "")
        collected += len(chunks[-1])
        if collected >= max_chars:
            truncated = len(reader.pages) > len(chunks)
            break
    full_text = "\n\n".join(chunks)
    return total_pages, full_text[:max_chars], truncated or len(full_text) > max_chars


async def _download_and_extract(
    client: TelegramClient, channel: str, message, max_chars: int = DOC_TEXT_TRUNCATE
) -> dict:
    if not message.document:
        raise ValueError(f"message_id={message.id}에 PDF 첨부가 없음")
    filename = _document_filename(message) or f"{channel}_{message.id}.pdf"
    if message.document.mime_type != "application/pdf" and not filename.lower().endswith(".pdf"):
        raise ValueError(f"PDF가 아닌 첨부 파일: {filename} ({message.document.mime_type})")

    DOC_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = DOC_CACHE_DIR / f"{channel}_{message.id}.pdf"
    if cache_path.exists():
        data = cache_path.read_bytes()
    else:
        data = await client.download_media(message, file=bytes)
        cache_path.write_bytes(data)

    pages, text, truncated = await asyncio.to_thread(_extract_pdf_text, data, max_chars)
    return {"filename": filename, "pages": pages, "text": text, "truncated": truncated}


async def _search_one_channel(
    client: TelegramClient, channel: str, query: str, limit: int
) -> tuple[list[dict], list[object], str | None]:
    """채널 하나를 검색합니다. 가입 안 한 채널은 에러를 던지지 않고 error 문자열로
    돌려줘서, 나머지 채널 검색이 함께 죽지 않게 합니다."""
    entries: list[dict] = []
    messages: list[object] = []
    try:
        async for message in client.iter_messages(channel, search=query, limit=limit):
            filename = _document_filename(message)
            raw_text = message.text or ""
            entries.append(
                {
                    "channel": channel,
                    "message_id": message.id,
                    "date": message.date.strftime("%Y-%m-%d %H:%M") if message.date else None,
                    "text": raw_text[:TEXT_TRUNCATE],
                    "parsed": _parse_caption_fields(raw_text),
                    "link": f"https://t.me/{channel}/{message.id}",
                    "has_document": filename is not None,
                    "document_filename": filename,
                    # 수출입 채널(BeOn)은 수치를 그래프 이미지로 올린다. 캡션만으로는
                    # 금액을 알 수 없으므로, 이미지가 붙어 있으면 표시해서
                    # get_message_image로 직접 보게 한다.
                    "has_image": message.photo is not None,
                }
            )
            messages.append(message)
        return entries, messages, None
    except Exception as exc:  # noqa: BLE001
        return [], [], str(exc)


@mcp.tool()
async def search_channel(
    query: str,
    channel: str | list[str] | None = None,
    limit: int = MAX_RESULTS,
    auto_fetch_documents: int = AUTO_FETCH_DOCUMENTS,
) -> dict:
    """여러 텔레그램 채널을 텔레그램 서버 검색으로 한 번에 조회합니다.

    channel을 생략하면 DEFAULT_CHANNELS 전체를 동시에 검색해 최신순으로 병합합니다.
    상위 auto_fetch_documents건의 첨부 PDF는 본문(document.text)까지 함께 돌려주므로
    추가 호출이 필요 없습니다. 가입하지 않은 채널은 channel_errors에 담기고 나머지
    채널 결과는 정상적으로 옵니다.
    """
    channels = [channel] if isinstance(channel, str) else list(channel or DEFAULT_CHANNELS)

    client = _client()
    await client.connect()
    try:
        await _require_authorized(client)

        per_channel = await asyncio.gather(
            *(_search_one_channel(client, ch, query, limit) for ch in channels)
        )
        channel_errors = {
            ch: error for ch, (_, _, error) in zip(channels, per_channel, strict=True) if error
        }

        paired: list[tuple[dict, object]] = []
        for entries, messages, _ in per_channel:
            paired.extend(zip(entries, messages, strict=True))
        paired.sort(key=lambda pair: pair[0]["date"] or "", reverse=True)
        paired = paired[:limit]

        matches = [entry for entry, _ in paired]
        to_fetch = [
            (idx, entry["channel"], msg)
            for idx, (entry, msg) in enumerate(paired)
            if entry["has_document"]
        ][:auto_fetch_documents]

        # PDF 내려받기는 네트워크 대기라 동시에 처리합니다 — 하나씩 받으면 느려서
        # 도구 호출 자체가 시간 초과될 수 있습니다.
        if to_fetch:
            results = await asyncio.gather(
                *(_download_and_extract(client, ch, msg) for _, ch, msg in to_fetch),
                return_exceptions=True,
            )
            for (idx, _, _), result in zip(to_fetch, results, strict=True):
                if isinstance(result, Exception):
                    matches[idx]["document_error"] = str(result)
                else:
                    matches[idx]["document"] = result

        return {
            "channels_searched": channels,
            "channel_errors": channel_errors,
            "matches": matches,
        }
    finally:
        await client.disconnect()


@mcp.tool()
async def get_document_text(
    channel: str, message_id: int, max_chars: int = DOC_TEXT_TRUNCATE
) -> dict:
    """search_channel 결과 중 본문이 안 딸려온 매치의 PDF를 따로 읽습니다.

    channel에는 그 매치 자신의 channel 값을 넣습니다. 한 번 받은 PDF는
    telegram_docs/ 폴더에 저장해 두고 다시 받지 않습니다.
    """
    client = _client()
    await client.connect()
    try:
        await _require_authorized(client)
        message = await client.get_messages(channel, ids=message_id)
        if message is None:
            raise ValueError(f"message_id={message_id}를 찾을 수 없음")
        return await _download_and_extract(client, channel, message, max_chars)
    finally:
        await client.disconnect()


IMAGE_MAX_PX = 1600


def _shrink_to_jpeg(data: bytes, max_px: int = IMAGE_MAX_PX) -> bytes:
    """텔레그램 원본 이미지는 크기가 커서 그대로 넘기면 응답이 무거워진다.
    긴 변을 max_px로 줄이고 JPEG로 다시 인코딩한다 — 그래프의 숫자는 이 해상도에서
    충분히 읽힌다."""
    img = PILImage.open(io.BytesIO(data))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    if max(img.size) > max_px:
        ratio = max_px / max(img.size)
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), PILImage.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


async def _collect_group_photos(client: TelegramClient, channel: str, message) -> list:
    """같은 게시물 묶음(grouped_id)에 속한 사진 메시지를 모은다.

    BeOn 같은 채널은 '그래프 이미지 메시지'와 '설명 캡션 메시지'를 한 묶음으로
    올린다. 검색에 걸리는 쪽은 글자가 있는 캡션 메시지이므로, 그 주변 메시지까지
    훑어야 실제 데이터 이미지를 찾을 수 있다."""
    photos = [message] if message.photo else []
    if not message.grouped_id:
        return photos
    ids = list(range(message.id - 10, message.id + 11))
    siblings = await client.get_messages(channel, ids=ids)
    photos = [
        m
        for m in siblings
        if m is not None and m.photo and m.grouped_id == message.grouped_id
    ]
    photos.sort(key=lambda m: m.id)
    return photos


@mcp.tool()
async def get_message_image(channel: str, message_id: int, index: int = 0) -> Image:
    """게시물에 붙은 이미지를 가져와 그대로 보여준다 — 이미지 속 숫자를 직접 읽기 위한 도구.

    수출입 데이터 채널(BeOn_BeClear)은 금액·증감률을 캡션이 아니라 **그래프 이미지**로
    올린다. 캡션에는 품목·관련종목·기간만 있으므로, 수치가 필요하면 이 도구로 이미지를
    불러와 눈으로 읽어야 한다. 읽어낸 수치에는 반드시 [2차] 라벨과 잠정/확정 구분을
    함께 적는다.

    한 게시물에 이미지가 여러 장이면 index로 고른다(0부터). search_channel 결과의
    has_image가 true인 매치에 대해 호출한다.
    """
    client = _client()
    await client.connect()
    try:
        await _require_authorized(client)
        message = await client.get_messages(channel, ids=message_id)
        if message is None:
            raise ValueError(f"message_id={message_id}를 찾을 수 없음")

        photos = await _collect_group_photos(client, channel, message)
        if not photos:
            raise ValueError(f"message_id={message_id}에 이미지가 없음")
        if index >= len(photos):
            raise ValueError(f"이미지가 {len(photos)}장뿐인데 index={index}를 요청함")

        data = await client.download_media(photos[index], file=bytes)
        return Image(data=_shrink_to_jpeg(data), format="jpeg")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    mcp.run()
