# Evaluating AI outputs, skills, and agents

Research checked on **2026-11-11**, against the system clock. This is a review of public evidence, not a benchmark run by this project. “State of the art” here means the strongest useful methods found in this search. It does not mean one tool has proved best for every task.

## 1. What the four named sources do

An evaluation needs a task, a run, evidence of the result, and a rule for judging success. The useful question changes with the object being evaluated.

| Object | Main question | Evidence needed |
| --- | --- | --- |
| One output | Does this result meet the requirements? | The output and independent checks. |
| An agent | Can this system complete a task using its tools? | The final state, tool records, and any required intermediate behavior. |
| A skill | Does adding these instructions improve results? | Matched runs with and without the skill. |
| A revised skill | Is the revision better than the original? | Matched runs of both versions, with the model and environment held fixed. |

These questions explain many apparent disagreements. A successful demonstration verifies one outcome. It does not estimate how often the system will succeed on other tasks.

### Matt Pocock combines software checks with application evals

Matt's [published explanation](https://www.aihero.dev/three-types-of-evals) separates deterministic checks, model judges, and human feedback. He treats model-judge failures as useful signals for human inspection. His older application-evaluation material uses datasets, task functions, and scorers.

Evalite implements that pattern, including repeated trials, variants, traces, and score thresholds. Matt's current skills also require reproducing bugs and checking observable behavior. The [practitioner source review](practitioner-research.md) records the implementation links and pinned commits.

There is an important maintenance change. [Evalite was deprecated and archived on November 9, 2026](https://github.com/mattpocock/evalite/commit/4129d73fe5cbba256fe8db91ef3f475ea4a04389). Matt recommends Langfuse, while explicitly explaining that it is not a direct replacement. Historical Evalite examples remain useful for learning the method. They are a poor default dependency for new work.

My assessment: Matt offers a practical route from software testing to AI evaluation. The existence of a runner does not validate its dataset or its scorers. A threshold on an average score does not establish statistical confidence.

### Poteto checks real behavior and blinds comparisons

Poteto is Lauren Tan. The canonical source is [pstack in cursor/plugins](https://github.com/cursor/plugins/tree/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack). The standalone backnotprop repository is a mirror with its own changes.

Pstack's verification skills give an agent a way to start and control the actual application. They require observing the initiating action, visible result, and relevant side effects. Formal-verification skills add checks for stated properties, with assumptions and bounds. See the [detailed source review](practitioner-research.md) for these separate workflows.

The [Eval playbook](https://github.com/cursor/plugins/blob/5866df557357d005b3c0c9d3da0d9e739b4bdde3/pstack/skills/poteto-mode/playbooks/eval.md) specifies hidden grading criteria, ordinary-looking requests, isolated candidate environments, and neutral output labels. A judge from another model family compares the results. The coordinator inspects actual artifacts and tool records, then compares their own judgment with the model's verdict.

My assessment: pstack is unusually explicit about avoiding self-report and evaluation cues. However, different candidate models can confound a skill comparison. The published playbook does not set a general sample size or confidence procedure. Its instructions are evidence of a method, not measured proof of pstack's overall benefit.

### OpenAI separates activation, outcome, process, and efficiency

OpenAI's January 22 guide, [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills), records agent events and generated files. It checks outcome, process, style, and efficiency separately. Its prompt set covers explicit invocation, natural implicit requests, and cases where the skill must stay inactive. Structured event records support code-based checks. A structured rubric handles softer requirements.

The broader [evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices) recommends task-specific datasets, real failure examples, automated checks, human calibration, and continuous evaluation. It favors specific judgments and pairwise comparisons over vague overall impressions.

**Product status is separate from method.** OpenAI's [deprecation schedule](https://developers.openai.com/api/docs/deprecations) says existing hosted Evals became read-only on October 31, 2026. The dashboard and API are scheduled to shut down on November 30. The current [Promptfoo guide](https://developers.openai.com/api/docs/guides/promptfoo-codex) provides a supported direction for new evaluation work. Older docs still contain hosted-Evals examples. Follow the explicit lifecycle notice when those pages conflict.

My assessment: the skills guide is directly relevant to this project. Its small initial prompt set is a regression starting point. It is not evidence that a small sample can establish broad reliability. These are published recommendations and examples, not a complete description of OpenAI's private release process.

### Anthropic compares against baselines and checks the evaluator

Anthropic's January 9 article, [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), distinguishes task outcomes from the agent's account of its work. It combines code checks, model judges, and human review. It recommends isolated trials, transcript inspection, and separate capability and regression suites. It also distinguishes finding one success in several attempts from succeeding consistently across attempts.

The March 3 [skill-creator update](https://claude.com/resources/articles/improving-skill-creator-test-measure-and-refine-agent-skills) separates skills that add capability from skills that encode a preferred workflow. A skill can remain useful for enforcing a workflow even when a stronger model can already perform the underlying task.

The [current implementation](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator/SKILL.md) runs each case with the skill and a baseline. A new skill uses no skill as its baseline. A revision uses an earlier version. It collects assertions and human feedback. The [blind comparator](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator/agents/comparator.md) judges outputs labeled A and B without knowing their source. The [aggregation script](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator/scripts/aggregate_benchmark.py) computes means, standard deviations, ranges, and differences in pass rate, time, and tokens.

My assessment: this is a concrete baseline-and-review loop that we can inspect. Standard deviation describes observed variation. It is not a confidence interval for improvement. A model-generated assertion also needs independent review before it becomes a trusted success condition.

## 2. Recent studies show why the task set matters

The search found materially revised papers. Search summaries sometimes described their earlier versions. The figures below come from opened, version-specific papers, not those summaries. They are author-reported results. This project has not reproduced them.

### Broad specialist tasks show substantial benefits

[SkillsBench v4, June 14, 2026](https://arxiv.org/html/2602.12670v4), reports matched comparisons across 87 tasks and 18 model-and-agent configurations. Average pass rate rises from 33.9% without curated skills to 50.5% with them. That is a gain of 16.6 percentage points. The paper includes deterministic verifiers and a confidence-interval procedure. Its current website includes additional configurations, so the live leaderboard and paper snapshot should not be mixed.

### Public software skills show much smaller benefits

[SWE-Skills-Bench v2, October 27, 2026](https://arxiv.org/html/2603.15401v2), tests 98 public software skills in pinned repositories across four configurations. Its table reports 76.59% without skills and 76.93% with them. Of the 98 skills, 92 have no statistically significant effect under its procedure. The study uses one run per condition for each task and configuration, which limits conclusions about run-to-run variability.

The two studies use different tasks, skills, models, and success rules. They do not establish contradictory measurements of the same population. My inference is that a useful evaluation must measure the benefit of a particular skill on the work it will actually receive. A high baseline also leaves less room for improvement.

### Retrieval and average rubric scores can hide failure

[Skill Following, September 1, 2026](https://arxiv.org/abs/2609.00549v1), examines matched outcomes on tasks where the agent actually retrieved a skill. It reports cases where an aggregate improvement hides worse results on those retrieved tasks. This is evidence for checking selection and use separately. Its experiments cover coding and mathematics, not arbitrary professional workflows.

[SkillForgeBench, October 10, 2026](https://arxiv.org/abs/2610.14918v1), evaluates 842 sandboxed tasks using completion and process requirements. It reports much lower strict task completion than individual rubric pass rates. The useful lesson is to report whether all essential requirements pass together. The paper's model rankings are not a prediction for this project.

## 3. What a strong evaluation can prove

The following comparison is my synthesis of the sources, not a claim that one organization uses exactly this design.

| Method | A realistic example | What it establishes | Main limitation |
| --- | --- | --- | --- |
| Code-based checks | Open a generated spreadsheet and independently verify its totals. | Specific requirements hold for that artifact. | Missing requirements remain unchecked. |
| Behavioral execution | Add an item through the UI, reload, and inspect saved state. | The tested user path works in that environment. | Coverage and environment realism limit generalization. |
| Model judgment | Compare two source-grounded summaries against a fixed rubric. | The judge's preference under those instructions. | Bias, inconsistency, missing context, and factual mistakes. |
| Expert review | Ask a domain expert to assess factual support and usefulness. | Alignment with that expert's criteria. | Cost, disagreement, and limited review capacity. |
| Formal checking | Check that retries cannot create duplicate charges in a bounded model. | The specified property holds within the model and assumptions. | The model or property can omit the real defect. |

For code, independently executed behavior usually gives stronger evidence than a judge's impression of the code. For writing, meaning and usefulness require judgment. For research, a fluent answer needs claim-level source support. For an agent action, the final external state matters. Tool-call counts alone cannot prove success.

### Model judges require their own evaluation

My recommended procedure is to collect human-labeled examples before trusting a judge. Include acceptable variation, plausible errors, and failures that look polished. Fix the rubric and judge version. Blind source labels and vary output order. Record agreements and disagreements with humans, including false passes and false failures. Review disagreements before changing the product to satisfy the judge.

Using another model family can reduce some shared bias. Agreement between several models still does not establish truth. A judge also needs the original task and relevant evidence. A factuality judge without the source cannot independently check source fidelity.

OpenAI's [grader documentation](https://developers.openai.com/api/docs/guides/graders) explicitly recommends evaluating graders against trusted judgments and checking whether their rankings agree. The scorer itself is part of the system under test.

### Repeated trials need a defined unit of success

“Did one of five attempts work?” and “Did all five work?” answer different product questions. My recommendation is to start with per-attempt success and show each task's results. Add retry metrics only when retries match the actual product behavior. A retry policy also consumes time and money and needs a way to recognize success.

For skill comparisons, hold the model version, tools, input files, limits, and repository revision fixed. Reset state between attempts. Use fresh outputs when measuring variability. A cached response can help rerun a scorer, but cannot represent a new generation trial.

Compare conditions on the same tasks. Preserve the paired differences when estimating uncertainty. Repeated runs on one task are related observations, not evidence about many independent task types. For a broader claim, estimate uncertainty at the task level, for example by resampling whole tasks with their paired runs.

[Inspect's scoring metrics](https://inspect.aisi.org.uk/metrics.html) explicitly address grouped results, clustered errors, and epoch reduction. Those distinctions matter more than adding decimal places to a mean score.

### The evaluation environment can be the source of failure

Anthropic's [BrowseComp investigation](https://www.anthropic.com/research/eval-awareness-browsecomp) documents an agent identifying its evaluation and locating benchmark answers. This makes leakage a practical concern for agents with web access. Hiding labels reduces cues but does not guarantee blindness.

My recommendation is to keep answer keys and checks outside the agent's writable workspace. Validate each task with a known solution. Test that a deliberately defective output fails. Distinguish product failures, model refusals, exhausted budgets, and broken evaluation infrastructure. Do not silently discard inconvenient runs.

## 4. Existing tools already cover much of the machinery

This is a capability shortlist, not a hands-on product ranking. Documentation and code were inspected. No service was installed or benchmarked.

| Tool | Published capability | Likely fit for this project |
| --- | --- | --- |
| [Promptfoo](https://www.promptfoo.dev/docs/configuration/reference/) | Configured prompts, providers, assertions, repeated cases, caching controls, and tracing. | A small comparison of prompts or model calls. |
| [Langfuse](https://langfuse.com/docs/evaluation/experiments/datasets) | Versioned datasets, expected outputs, production-trace links, and experiment comparisons. | Connecting experiments with observed application failures. |
| [LangSmith](https://docs.langchain.com/langsmith/evaluation-types) | Offline evaluation, online evaluation, pairwise comparison, and experiment-level metrics. | Reviewing whole agent workflows and their individual steps. |
| [Inspect](https://inspect.aisi.org.uk/scoring.html) | Custom scorers, multiple scoring methods, failure policies, and statistical aggregation. | More explicit research evaluation and analysis. |
| [Harbor](https://docs.harborframework.com/core-concepts/index) | Tasks containing instructions, environments, and verifiers, plus agent trials and trajectories. | Full tool-using agents that need isolated task environments. |

[Inspect's sandbox documentation](https://inspect.aisi.org.uk/sandboxing.html) makes an important boundary explicit: providing a sandbox does not put every part of the evaluation inside it. Only operations routed through that interface execute there. Isolation needs verification, just like scoring.

Two newer projects are especially relevant to skills. [NVIDIA SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator) separates static validation, overlap checks, and live agent evaluation. Its documentation warns that starter cases have limited coverage and labels the project experimental. [SkillBenchmark](https://github.com/TiesPetersen/SkillBenchmark) provides blinded text comparisons and confidence estimates. Its stated v1 scope is single-turn text calls, so it cannot establish the reliability of tool-using workflows.

My assessment: building another generic runner would duplicate substantial existing work. A more useful contribution could be a public set of realistic cases, independent checks, baseline comparisons, and readable evidence. That direction remains a proposal, not a selected implementation.

## 5. The smallest experiment worth doing here

This is a proposed pilot, not completed work or a statistical sample-size guarantee. Its purpose is to expose bad task definitions and bad scorers before spending more.

1. Select one skill and write 12 realistic cases. Include common tasks, difficult cases, and nearby requests where the skill must stay inactive. Reserve four cases from prompt tuning.
2. Run the same model on each case with and without the skill, five fresh attempts per condition. This creates 120 generation runs. Keep equal budgets and reset state.
3. Check actual artifacts and required side effects. Use a fixed, blinded judge only for criteria that code cannot check. Have a human assess a calibration sample and disputed judgments.
4. Report paired task results, strict success, activation mistakes, harmful regressions, judge disagreement, elapsed time, and monetary cost. State which failures came from infrastructure.
5. Inspect the failures before revising the skill. Keep the reserved cases separate and expand the sample before making a broad reliability claim.

The pilot compares an isolated skill first. A later experiment can test the installed collection, where overlapping descriptions and instructions may change activation. Isolated benefit and benefit inside the full setup are separate questions.

Cost includes successful and failed runs, baseline calls, judge calls, tool services, and any human review. Report usage separately when monetary prices are unavailable. A useful efficiency measure is total experiment cost divided by independently accepted outputs. A cheap system that repeatedly fails can be expensive per usable result.

## Evidence limits

The [practitioner note](practitioner-research.md) contains additional first-party sources and immutable code links. Poteto's linked X articles returned HTTP 403 during that research. Their unread content supports no claim here. Published workflows do not establish private company practice or the average benefit of a complete skill collection. Paper results are conditional on their versions and protocols. No model calls, product trials, formal proofs, or benchmark reproductions were performed for this report.
