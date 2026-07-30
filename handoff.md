## 2026-07-30 — 7차 · 스캐폴드 재구조 설계: 클럽 주차축 / 개인 워크스페이스 분리 (C안 채택)

Operator: @zoon / Company Hermes

Input:

- @zoon: "My Investor Club 워크스페이스의 완성도를 더 올리고 스캐폴더에 대해서 조금 더 신경을 쓰려고 … 세션 내용에 대한 인풋을 단일화하고 참고 폴더를 일원화한 구조"
- @zoon(3안 제시 후): "C가 좋아. 주차축을 단위화해서 그 주차 안에 들어와야 될 인풋의 종류를 뭐 클럽, AI 클럽 자료, 사람들의 했던 어떤 강연 내용, 학생들이 냈던 어떤 주차별 과제 내용, 그리고 기타 소스 노트 … 참고로 이 주차축은 클럽 전체인 거고, 나의 워크스페이스는 좀 따로 만들어 놓는 거지"

Source checked:

- `dp-investor-club` org 4레포 전수 — `orgs/.../repos`(가시성·default_branch), `git/trees?recursive=1` × `my-investor-club-workspace`(main + club-materials) / `ai-layer` / `operations` / `my-investor-club-workspace-zoon`.
- 템플릿 `main` tarball clone 후 스킬 15개 + 루트 5파일 원문 직접 판독, `grep -rn "sources/\|outputs/\|weeks/\|week-0"`로 경로 참조 전수 추출.
- `club-materials` 브랜치 README + `.claude/club-skills.txt` manifest 원문.

Applied:

- `artifacts/2026-07-30-dpic-workspace-scaffold-week-axis-restructure-v0.md` 신설 — 4중 중복 실측표, 확정 구조 2축, **영향 파일 15행 줄 단위 수정표**, 미결 2건 권고, 실행 7단계.
- `current-state.md` 7차 신설.
- `next-actions.md` 최상단 신규 항목 — 미결 2건(호스팅 위치 / `submissions/` 내용)을 권고와 함께 owner 슬롯으로 등재.

Judgment:

- **구조 설계 전에 실측한 것이 결론을 바꿨다.** zoon의 요청은 "일원화할 구조를 만들자"였지만 실측하니 주차축이 이미 4곳(private `operations` / `club-materials` 브랜치 / `ai-layer` / 학생 로컬)에 존재하고 W1 강의 원본이 2곳에 이중 존재했다. 새 구조를 얹는 문제가 아니라 **기존 4개를 접는 문제**로 재정의했다 — 새로 만들면 5번째 중복이 된다.
- **호스팅 권고 B의 근거를 설계 논리가 아니라 실패 실측에 두었다.** `club-materials`는 구조가 나쁘지 않은데 4주간 1건이다. 원인은 README가 요구하는 `git checkout club-materials`가 운영자 비용이고 그 비용이 실제로 지불되지 않았다는 것 — 같은 브랜치에 폴더만 늘리면 동일하게 빌 것이라고 판정했다. 브랜치 스위치를 없애는 것이 4칸 구조보다 선행 조건.
- **`submissions/` 칸을 학생 push 파이프와 분리한 것이 이번 설계의 핵심 판정.** 5차에서 규명한 권한 단절(26명 403) 때문에 학생 산출물은 Slack에만 있다. 이 칸을 "학생이 올리는 곳"으로 정의하면 회수 경로 결정이 열릴 때까지 영구히 빈 칸이 되고, 캠프 8/13 교차 설치가 다시 미검증 전제 위에 서게 된다. 그래서 **운영진 harvest 칸**으로 정의하고 `peer-skills/` PR(학생 직접 반환)과 명시적으로 다른 파이프로 못박았다.
- **개인 워크스페이스에서 `weeks/`를 없애는 것이 학습 장치를 해치지 않는다고 판정한 근거**: 온보딩 블록 2의 학습 목표는 "AI에게 위임해본다"이고 폴더 생성은 그 소재였을 뿐이다. "자기 언어로 재정리"는 `outputs/w0N-*.md` + `journey.md` 세션노트가 그대로 받는다. 실제로 4주간 이 폴더는 레포에 한 번도 올라오지 않았다.
- **기존 학생 로컬 마이그레이션을 강제하지 않기로 했다.** 잔여 세션이 W5+캠프 2회뿐이라 구조 재학습 비용이 성과보다 크다. 재구조의 본체는 3기·캠프 재사용 원형이며, 2기에는 문구 변경만 `/update`로 흘린다.
- 실행하지 않은 이유: 신규 public 레포 생성은 카운터파티 org의 새 공개물(외부 표면), 학생 실명 산출물 재배포는 되돌릴 수 없는 참가자 데이터 노출. 둘 다 hard boundary라 권고까지만.

Verification:

- 4중 중복은 단일 응답에 의존하지 않고 레포별 `git/trees` + 브랜치별 조회로 교차 확인. `weeks/` 미존재는 템플릿 main·zoon 레포 양쪽 tree에서 부재 확인.
- 영향 파일 수정표는 추정이 아니라 clone 후 `grep -rn` 결과의 줄 번호를 그대로 사용.
- `club/` 유령 경계는 `submit/SKILL.md` Step 0-2 원문 + 4레포 tree에 `club/` 경로 0건으로 확인.

Boundary: 설계·실측·정본 기록만 — 레포 생성·변경·push 없음, 스킬 패치 없음, 참가자·NHR 발송 없음, 학생 산출물 재배포 없음, 학생 로컬 마이그레이션 강제 없음.


