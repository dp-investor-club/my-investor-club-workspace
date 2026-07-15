# clarify 스킬 출처 (provenance)

이 스킬은 team-attention이 만든 공개 스킬을 가져와 내장한 것이다. 외부에서 원본을 긁어와 대조할 수 있다.

- **원본**: `team-attention/plugins-for-claude-natives` → `plugins/clarify/skills/vague/SKILL.md`
- **원본 URL**: https://github.com/team-attention/plugins-for-claude-natives/blob/main/plugins/clarify/skills/vague/SKILL.md
- **raw**: https://raw.githubusercontent.com/team-attention/plugins-for-claude-natives/main/plugins/clarify/skills/vague/SKILL.md
- **가져온 커밋**: `fd9c20754dba0b0ab040f3f2cd2cb533fc43347d`
- **가져온 날짜**: 2026-07-14

## 우리가 바꾼 것 (본문은 verbatim)

1. frontmatter `name: vague` → `name: clarify` (`/clarify`로 부르기 위함, 라우팅 목적)
2. frontmatter `description` → 한국어 트리거 + 클럽 용도(방향/선언 명확화) 반영
3. 본문 맨 위 `CLUB NOTE` 주석 1개 추가 — 대상을 "소프트웨어 요구사항"이 아니라 "참가자의 방향(journey.md의 나의 선언)"으로 읽고, Phase 4에서 journey.md 선언을 덮어쓰도록 안내. **본문(프로토콜/규칙)은 원본 그대로.**

## 내장하지 않은 원본 형제 스킬

원본 clarify 플러그인에는 `vague` 외에 `unknown`(전략 사각지대), `metamedium`(내용 vs 형식 재구성)이 있다. 이 클럽 W2 용도에는 `vague`만 필요해 나머지는 내장하지 않았다. 본문에 남은 "use the unknown/metamedium skill" 문장은 원본 그대로이며, 그 스킬들은 위 원본 저장소에 있다.
