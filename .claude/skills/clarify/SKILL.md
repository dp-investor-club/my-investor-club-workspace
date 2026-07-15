---
name: clarify
description: 모호한 것을 반복 질문으로 구체화한다. 이 클럽에서는 나의 방향(journey.md의 "나의 선언")을 선명하게 만드는 데 쓴다. "clarify", "/clarify", "방향 명확히", "선언 다듬어줘", "내가 뭘 원하는지", "make this clearer", "요구사항 명확히" 요청에 사용.
---

<!-- ─────────────────────────────────────────────────────────────────────
  CLUB NOTE (Delta 추가 — team-attention 원본 스킬 위에 얹은 사용 지침):
  이 클럽에서 이 스킬의 대상은 소프트웨어 요구사항이 아니라 **참가자의 방향**이다.
  1. 대상은 journey.md의 "나의 선언"(또는 참가자가 말하는 흐린 방향/목표).
  2. 아래 본문의 프로토콜(가설-옵션 질문 → Before/After 요약)을 그대로 따르되,
     "requirement/spec"을 "나의 방향/선언"으로 읽는다.
  3. Phase 4(저장)에서는 requirements/ 대신 **journey.md의 "나의 선언"을 덮어쓸지**
     참가자에게 묻고, 승인하면 선명해진 선언으로 교체한다.
  아래 본문은 team-attention 원본이다(출처·변경점: 같은 폴더 SOURCE.md).
────────────────────────────────────────────────────────────────────── -->

# Vague: Requirement Clarification

Transform vague or ambiguous requirements into precise, actionable specifications through hypothesis-driven questioning. **ALWAYS use the AskUserQuestion tool** — never ask clarifying questions in plain text.

## When to Use

- Ambiguous feature requests ("add a login feature")
- Incomplete bug reports ("the export is broken")
- Underspecified tasks ("make the app faster")

For strategy/planning blind spot analysis, use the **unknown** skill. For content-vs-form reframing, use the **metamedium** skill.

## Core Principle: Hypotheses as Options

Present plausible interpretations as options instead of asking open questions. Each option is a testable hypothesis about what the user actually means.

```
BAD:  "What kind of login do you want?"           ← open question, high cognitive load
GOOD: "OAuth / Email+Password / SSO / Magic link" ← pick one, lower load
```

## Protocol

### Phase 1: Capture and Diagnose

Record the original requirement verbatim. Identify ambiguities:
- What is unclear or underspecified?
- What assumptions would need to be made?
- What decisions are left to interpretation?

### Phase 2: Iterative Clarification

Use AskUserQuestion to resolve ambiguities. **Batch up to 4 related questions per call.** Each option is a hypothesis about what the user means.

**Cap: 5-8 total questions.** Stop when all critical ambiguities are resolved, OR user indicates "good enough", OR cap reached.

**Example AskUserQuestion call:**
```
questions:
  - question: "Which authentication method should the login use?"
    header: "Auth method"
    options:
      - label: "Email + Password"
        description: "Traditional signup with email verification"
      - label: "OAuth (Google/GitHub)"
        description: "Delegated auth, no password management needed"
      - label: "Magic link"
        description: "Passwordless email-based login"
    multiSelect: false
  - question: "What should happen after registration?"
    header: "Post-signup"
    options:
      - label: "Immediate access"
        description: "User can use the app right away"
      - label: "Email verification first"
        description: "Must confirm email before access"
    multiSelect: false
```

### Phase 3: Before/After Summary

Present the transformation:

```markdown
## Requirement Clarification Summary

### Before (Original)
"{original request verbatim}"

### After (Clarified)
**Goal**: [precise description]
**Scope**: [included and excluded]
**Constraints**: [limitations, preferences]
**Success Criteria**: [how to know when done]

**Decisions Made**:
| Question | Decision |
|----------|----------|
| [ambiguity 1] | [chosen option] |
```

### Phase 4: Save Option

Ask whether to save the clarified requirement to a file. Default location: `requirements/` or project-appropriate directory.

## Ambiguity Categories

| Category | Example Hypotheses |
|----------|-------------------|
| **Scope** | All users / Admins only / Specific roles |
| **Behavior** | Fail silently / Show error / Auto-retry |
| **Interface** | REST API / GraphQL / CLI |
| **Data** | JSON / CSV / Both |
| **Constraints** | <100ms / <1s / No requirement |
| **Priority** | Must-have / Nice-to-have / Future |

## Rules

1. **Hypotheses, not open questions**: Every option is a plausible interpretation
2. **No assumptions**: Ask, don't assume
3. **Preserve intent**: Refine, don't redirect
4. **5-8 questions max**: Beyond this is fatigue
5. **Batch related questions**: Up to 4 per AskUserQuestion call
6. **Track changes**: Always show before/after
