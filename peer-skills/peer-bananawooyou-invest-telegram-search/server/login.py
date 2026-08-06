"""텔레그램에 한 번만 로그인해서 세션 파일을 만듭니다.

이 폴더에서 `python login.py`를 직접 실행하세요.
전화번호 -> 인증번호 -> (2단계 인증을 켜뒀다면) 비밀번호를 물어봅니다.

성공하면 telegram_session.session 파일이 생기고, 그 뒤로는 다시 할 필요가 없습니다.
이 파일은 내 계정 로그인 정보이므로 절대 남에게 주거나 커밋하지 마세요.
"""

import asyncio

from server import SESSION_PATH, get_credentials
from telethon import TelegramClient


async def main() -> None:
    api_id, api_hash = get_credentials()
    client = TelegramClient(str(SESSION_PATH), api_id, api_hash)

    # start()가 전화번호와 인증번호를 순서대로 물어봅니다.
    await client.start()

    me = await client.get_me()
    print()
    print(f"로그인 성공: {me.first_name} (@{me.username})")
    print(f"세션 파일: {SESSION_PATH}.session")
    print("이제 Claude Code에서 바로 쓸 수 있습니다.")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
