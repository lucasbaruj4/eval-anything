# How Matt Pocock and Poteto verify AI work

Retrieved **2026-11-11**. The system clock confirmed that date in UTC. This note separates published working practices, executable checks, and measured evidence. It reports source inspection, not experiments run for this project.

## 1. Sources and authorship

Poteto is Lauren Tan. The canonical pstack source is **`cursor/plugins/pstack`**, inside Cursor's public plugin repository. Its manifest names Lauren Tan as author. Poteto opened the [original plugin PR][p-origin]. The [standalone mirror][mirror] explicitly identifies that upstream and describes its own portability changes. `backnotprop` maintains that mirror. Its changes must not automatically be attributed to Poteto.

The following commits fix the source versions used here. Every code link below uses one of these immutable snapshots.

| Repository | Inspected commit | Relevant state |
| --- | --- | --- |
| `mattpocock/skills` | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | Package version 1.3.2. |
| `mattpocock/evalite` | `4129d73fe5cbba256fe8db91ef3f475ea4a04389` | Deprecation merged on 2026-11-09. |
| `cursor/plugins` | `5866df557357d005b3c0c9d3da0d9e739b4bdde3` | pstack manifest version 0.15.36. |
| `poteto/verification-skill-example` | `d5abe70d0d8c671672b6cef4069363f26c488feb` | Fictional example, with driver scripts omitted. |

Versions come from the [Matt skills package][m-package], [Evalite deprecation commit][e-deprecation], and [pstack manifest][p-manifest]. The example's [README][p-example] states its limits.

First-party writing includes Matt's AI Hero articles and pstack's upstream guide. Poteto's X article links were also located: [The Complete Guide to pstack, part 1][p-article1] and [part 2][p-article2]. Direct retrieval returned HTTP 403. Their full text does not support any substantive claim here. Public upstream Markdown supplies the readable first-party evidence.

## 2. Matt Pocock: engineering checks and application evaluations

### Skills are instructions whose behavior needs checking

Matt's [writing-for-agents skill][m-writing] treats reliability as repeatable process, while allowing different outputs. It describes weak reference wording as a cause of variation. Clear completion conditions reduce early termination. Its pruning test asks whether an instruction changes behavior relative to the model's default. Disagreements should be settled by running the document.

The accompanying [first-party explanation][m-writing-doc] explicitly describes manual execution rather than an automated evaluation for this writing method. It also warns that a skill distilled from one successful session can fit that session too closely. The proposed correction is deliberate generalization to a task class.

This supports a practical behavioral comparison. It does not establish a published, repeated experiment measuring each skill's benefit. Nor does the manual-method statement establish that Matt never evaluates skills with other tools.

### Code quality comes from checks that can expose the actual failure

His [diagnosing-bugs skill][m-diagnosis] requires an executed command that can fail on the user's exact symptom before hypothesis testing. Options include tests, HTTP requests, browser automation, trace replay, generated inputs, and comparisons between versions. A successful command that merely avoids crashing does not meet that requirement.

For intermittent defects, the skill seeks a higher reproduction rate through repeated triggers and stress. It requires the original scenario to pass after the fix. A regression test belongs at a boundary that can reproduce the real interaction. If that boundary is unavailable, the skill records the limitation.

His [TDD skill][m-tdd] similarly favors observable behavior through public interfaces. Expected values need an independent basis, such as a specification or worked example. Recalculating the expected result with the implementation's logic creates a test that cannot provide independent evidence.

The [code-review skill][m-review] separates standards review from specification review. It asks two agents to inspect those axes independently, then reports each separately. This is a review procedure. Finding counts do not measure the probability that the generated code is correct.

### Evalite is concrete evaluation-runner evidence

Matt's [The Three Types Of Evals][m-three] distinguishes deterministic checks, model judges, and human feedback. He describes judge failures as signals for human inspection and retains human oversight. [Your App Is Only As Good As Its Evals][m-evals] describes datasets, tasks, and scorers. It argues for production-representative examples informed by user feedback.

Evalite implements that pattern. Its [runner code][e-runner] executes tasks and scorers, with input, output, and expected values available to scorers. `evalite.each()` creates variants for comparisons. `trialCount` expands each dataset item into repeated executions and defaults to one.

The [trial-count tests][e-trials] provide particularly concrete evidence. They run fixtures and assert that two inputs with three trials produce six stored results. Further checks cover trial indices and configuration precedence. These are executable runner tests inspected in source. They were not run during this research.

The [threshold implementation][e-threshold] sets a failing exit code for task failures or an insufficient mean score. The [CI guide][e-ci] documents JSON results and static HTML exports. The [AI SDK wrapper][e-tracing] captures model inputs, outputs, token usage, and call timing. Those records help investigate failures and estimate usage costs. Token counts alone are not monetary costs.

Matt's [tool-agent workshop][m-tools] applies deterministic scoring to expected tool selection. It compares models on shared cases and includes ambiguous requests, missing information, and requests needing no action. These cases test when the agent should request clarification. His [evaluation project][m-project] extends this to memory extraction and complete agents requiring multiple retrieval steps. These are published teaching workflows, not independently verified production results.

**Current maintenance status matters.** Evalite was [archived and deprecated][e-deprecation] on **2026-11-09**. Matt states that his work changed focus and recommends Langfuse. The migration notes say that Langfuse is not a direct replacement. Historical Evalite code remains useful evidence of implementation, but describing it as actively maintained would be wrong. The older [v1 preview][m-v1] describes beta features. Those features must not be silently combined with the inspected main branch's [0.19.0 package][e-package].

**Assessment:** repeated trials and shared datasets enable useful comparisons. A mean score and a chosen threshold do not establish statistical confidence. The inspected runner paths do not define a confidence-interval procedure or a required sample size. Dataset coverage, independent trials, scorer validity, and human agreement still need separate justification. Repeated calls also need fresh outputs. Reusing cached responses cannot measure generation variability.

## 3. Poteto: prove behavior in the real application

### Verification skills give agents a way to observe results

Pstack's [create-verification-skill][p-create] generates project-specific instructions for starting an app, checking its health, controlling it, collecting evidence, and cleaning up. It derives commands from the repository. It also creates a feature map describing user paths and observable success conditions.

The proof standard includes the initiating action and its result. It requires checking side effects, such as written files or database changes, alongside visible UI behavior. Calling internal setters is insufficient evidence for a user path. Generation ends with an actual run through one mapped feature. An unexecuted result remains a draft.

[Maintain-verification-skill][p-maintain] compares the map with source and exercises every mapped feature live. It distinguishes stale instructions, gaps in the driver, and product defects. Product defects must be reported rather than hidden by rewriting the map.

The separate [Atlas example][p-example-skill] shows how this documentation looks for a large desktop application. It covers isolated instances, screenshots, accessibility inspection, performance traces, and success, error, cancellation, and persistence paths. However, its README says Atlas is fictional and omits the control scripts. It is a design example, not a runnable product demonstration or a published agent benchmark.

### Formal checks add explicit properties and explicit limits

[Create-formal-verification-skill][p-formal] chooses a property where failure matters and ordinary tests have limited reach. It selects a suitable checker and records the covered code, assumptions, bounds, and last synchronized commit. The generated check must detect a deliberately broken version before handoff.

There is executable machinery here. The [statechart runner][p-state-run] invokes TLC, the TLA+ model checker, with pinned defaults for the checker and Java. Its [corpus tests][p-state-tests] compare generated reports, diagrams, exit results, and counterexample paths with fixtures or plain TLC behavior. The compiler entered upstream in the [2026-10-27 change][p-state-change]. This is substantive recent implementation evidence, rather than repository-age evidence.

[Statechart's instructions][p-state] explain incomplete checking and diagram limits. They require replaying model counterexamples against real code. [Formal-check maintenance][p-formal-maintain] checks for divergence between code and model, reruns checks, and confirms that updated verification can still detect a break.

**Assessment:** this can establish a property within stated assumptions and bounds. It does not establish that the property expresses the user's full intent. A correct model can describe the wrong system. Compiler tests also do not measure how reliably an AI agent chooses or writes the right model.

## 4. Poteto: blinded skill comparisons and measured improvement

The [upstream guide][p-guide] recommends testing skill changes and adopted skills against the user's own work. It warns that edits based on one bad session can overfit that session.

The [Eval playbook][p-eval] specifies a deliberate experiment. The coordinator defines three to six grading criteria and keeps them from candidates. Candidates receive the same organic-looking request in separate environments. Visible paths and prompts must hide evaluation terms and the existence of competing candidates.

A judge from another model family sees neutral output labels. When comparing variants, one judge grades both sets together. The coordinator checks which files candidates actually opened and inspects the resulting code. Candidate claims that they followed instructions are insufficient. The coordinator also reads all outputs and compares them with the judge's verdict.

This is stronger than asking an agent whether a skill helped. Nevertheless, the playbook leaves sample size, repeated trials per task, task sampling, and confidence estimates unspecified. Different candidate models can also confound a skill comparison unless the experiment balances model and skill variants. Another model family reduces one possible source of shared bias. It does not establish judge accuracy.

Pstack's [Interrogate skill][p-interrogate] takes a related approach to reviews. Only findings supported by runs survive. The coordinator reruns each proposed reproduction. This verifies particular defects. A report with no verified findings does not establish an error rate or prove correctness.

For performance work, the [benchmark checklist][p-benchmark] is more explicit about repetition. Comparisons require at least five alternating runs per side, with median and range. A difference smaller than variation is not measurable improvement. It checks errors, realistic settings, system limits, and whether the claimed work actually ran.

The [Hillclimb playbook][p-hillclimb] freezes the measurement procedure after checking its sensitivity. Each attempt changes one thing, measures before and after, and passes a regression gate. Changes remain only when improvement exceeds noise. Its decision log records rejected attempts as well as accepted ones. These are instructions for experiments, not results showing pstack's average benefit.

## 5. What the evidence supports

Both practitioners put observable behavior ahead of an agent's assurance. Matt's public material combines engineering checks with an implemented application-evaluation runner. Poteto's public stack combines application control, bounded formal checks, blinded comparisons, and experiment procedures.

The evidence answers different questions:

| Question | Suitable evidence | Remaining uncertainty |
| --- | --- | --- |
| Did this output satisfy a concrete requirement? | Independent assertion or real-app observation. | Requirements omitted by the check. |
| Did the agent use the intended workflow? | Tool records, opened files, and resulting artifacts. | Whether that workflow improved quality. |
| Does a skill improve outcomes across tasks? | Repeated comparisons on matched tasks with and without the skill. | Sampling error, model effects, and judge errors. |
| Does a safety property hold? | A checked model or code-level property with stated scope. | Wrong assumptions, bounds, and model divergence. |

The third row is an analytical requirement for measuring general benefit. The sources inspected here do not establish a public controlled result that either complete skill collection reliably improves arbitrary work. That is a limit of this evidence, not a claim that private evaluations or other public results do not exist.

A small experiment informed by these sources would compare one unchanged model on matched tasks with and without one skill. It would repeat each condition, preserve outputs and tool records, and use independent outcome checks. Human review would inspect failures and disputed model judgments. Any result would state run counts, variation, failures, elapsed time, and model usage. This is a research recommendation, not an implementation decision.

[p-origin]: https://github.com/cursor/plugins/pull/73
[mirror]: https://github.com/backnotprop/pstack/blob/08547969e1dffaa6457ea65141cc62c1d9a2eef1/README.md
[m-package]: https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/package.json
[e-deprecation]: https://github.com/mattpocock/evalite/commit/4129d73fe5cbba256fe8db91ef3f475ea4a04389
[e-package]: https://github.com/mattpocock/evalite/blob/4129d73fe5cbba256fe8db91ef3f475ea4a04389/packages/evalite/package.json
[p-manifest]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/.cursor-plugin/plugin.json
[p-example]: https://github.com/poteto/verification-skill-example/blob/d5abe70d0d8c671672b6cef4069363f26c488feb/README.md
[p-article1]: https://x.com/poteto/article/2094457600259842065
[p-article2]: https://x.com/i/article/2094940651607715840
[m-writing]: https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/writing-for-agents/SKILL.md
[m-writing-doc]: https://www.aihero.dev/skills-writing-for-agents
[m-diagnosis]: https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/diagnosing-bugs/SKILL.md
[m-tdd]: https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/tdd/SKILL.md
[m-review]: https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/code-review/SKILL.md
[m-three]: https://www.aihero.dev/three-types-of-evals
[m-evals]: https://www.aihero.dev/what-are-evals
[e-runner]: https://github.com/mattpocock/evalite/blob/4129d73fe5cbba256fe8db91ef3f475ea4a04389/packages/evalite/src/evalite.ts
[e-trials]: https://github.com/mattpocock/evalite/blob/4129d73fe5cbba256fe8db91ef3f475ea4a04389/packages/evalite-tests/tests/trial-count.test.ts
[e-threshold]: https://github.com/mattpocock/evalite/blob/4129d73fe5cbba256fe8db91ef3f475ea4a04389/packages/evalite/src/reporter/EvaliteRunner.ts
[e-ci]: https://github.com/mattpocock/evalite/blob/4129d73fe5cbba256fe8db91ef3f475ea4a04389/apps/evalite-docs/src/content/docs/guides/ci.mdx
[e-tracing]: https://github.com/mattpocock/evalite/blob/4129d73fe5cbba256fe8db91ef3f475ea4a04389/packages/evalite/src/ai-sdk.ts
[m-tools]: https://www.aihero.dev/workshops/evals-skill-building-j36oe
[m-project]: https://www.aihero.dev/workshops/evals-project-21d8s
[m-v1]: https://www.aihero.dev/evalite-v1-preview
[p-create]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/create-verification-skill/SKILL.md
[p-maintain]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/maintain-verification-skill/SKILL.md
[p-example-skill]: https://github.com/poteto/verification-skill-example/blob/d5abe70d0d8c671672b6cef4069363f26c488feb/.cursor/skills/verify-atlas/SKILL.md
[p-formal]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/create-formal-verification-skill/SKILL.md
[p-state-run]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/statechart/scripts/run.ts
[p-state-tests]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/statechart/scripts/test/corpus.test.ts
[p-state-change]: https://github.com/cursor/plugins/commit/34b1b7c96f09f81a21a6c78f65b7833f7dcb5b24
[p-state]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/statechart/SKILL.md
[p-formal-maintain]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/maintain-formal-verification-skill/SKILL.md
[p-guide]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/docs/guide/09-make-it-yours.md
[p-eval]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/poteto-mode/playbooks/eval.md
[p-interrogate]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/interrogate/SKILL.md
[p-benchmark]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/benchmark-checklist/SKILL.md
[p-hillclimb]: https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/poteto-mode/playbooks/hillclimb.md
