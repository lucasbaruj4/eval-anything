# eval-anything

This file guides repository development. Keep product behavior in product documents and runtime instructions.

Explore how to evaluate AI outputs, skills, and agents, including subjective quality. This project is in research. No implementation is selected.

## Research

- Keep research and source links in `docs/research/`. Read `docs/research/research.md` before proposing an approach.

## Working rules

- Define the task, observable success, and required evidence before building. Separate required checks from human preferences.
- Make the smallest useful change. Add a module or dependency only when a concrete experiment needs it.
- Verify actual outputs and side effects. Use independent checks and human review where quality needs judgment.

### File structure

Use this layout as the skill is implemented. Add supporting scripts only when needed.

```text
AGENTS.md                   Development instructions
docs/
  research/                 Research and source notes
skills/
  eval-anything/
    SKILL.md                Instructions users install (planned)
    scripts/                Supporting code (optional)
```

## Language

- Avoid unnecessarily complex language, for example instead of using words like "deck" use words like "presentation".
