# Local issue tracker

Keep specs and tickets in `.scratch/`. Use one directory per feature.

- Save the spec at `.scratch/<feature-slug>/spec.md`.
- Save each ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`.

Number tickets in dependency order from `01`. Give each ticket a `Blocked by:` line and a checklist of verifiable acceptance criteria. Record blockers by ticket number and put the triage label in a `Status:` line.

When a skill asks you to publish a spec or ticket, write it to its local path.
