# eval-anything

This file guides repository development. Keep product behavior in product documents and runtime instructions.

Explore how to evaluate AI outputs, skills, and agents, including subjective quality. The first implementation is an installable skill for text comparisons.

## Research

- Keep research and source links in `docs/research/`. Read `docs/research/research.md` before proposing an approach.

## Working rules

- Define the task, observable success, and required evidence before building. Separate required checks from human preferences.
- Make the smallest useful change. Add a module or dependency only when a concrete experiment needs it.
- Verify actual outputs and side effects. Use independent checks and human review where quality needs judgment.
- For tests, keep what the test tests for in multiline strings on the first lines of the code. Explain data structures or types that help prove what the test is looking to prove. These are the ONLY allowed comment lines throughout all code in this repository. These lines will be read by humans, so create them with the pstack:unslop skill.

### File structure

Use this layout as the skill is implemented. Add supporting scripts only when needed.

```text
AGENTS.md                   Development instructions
docs/
  research/                 Research and source notes
skills/
  eval-anything/
    SKILL.md                Instructions users install
    agents/                 Invocation settings
    references/             Detailed procedures
    scripts/                Supporting code
tests/                      Helper behavior tests
```

Run helper tests with `python3 -m unittest discover -s tests` after changing skill scripts.

## Language

- Avoid unnecessarily complex language, for example instead of using words like "deck" use words like "presentation".
