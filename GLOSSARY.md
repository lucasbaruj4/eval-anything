# Eval anything

This project evaluates AI outputs, skills, and agents.

## Language

**Human preference**

A person's answer when asked which of two outputs they would use. The answer can be A, B, either, or neither.

**Output review**

An evaluation run that checks outputs against output requirements and gathers judgments about their quality. Its conclusions apply to the outputs examined.

**Evaluation plan**

The agreed description of what to evaluate, which evaluation tasks and task conditions to use, and what evidence to collect. It records the output requirements for each evaluation task.

**Evaluation run**

One execution of an evaluation plan.

**Evaluation task**

A request we give an agent, with the source material it needs to carry out the request.

**Task condition**

The setup under which an agent attempts an evaluation task. It can specify which skill version the agent can use.

**Attempt**

One try at an evaluation task under one task condition. A failed try still counts as an attempt.

**Output**

The result an agent produces in an attempt. A draft of text is one example.

**Output requirement**

A rule an output must meet to pass the evaluation task.

**Output check**

An assessment of whether an output meets an output requirement.

**Setup check**

An assessment of whether the setup used in an evaluation run matches the evaluation plan. It can assess one attempt or compare settings across attempts.
