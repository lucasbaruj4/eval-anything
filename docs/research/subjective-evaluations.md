# Subjective evaluations and the user's goal

## Article reviewed

Cameron R. Wolfe's [Evaluating Agents on Highly Subjective Tasks](https://cameronrwolfe.substack.com/p/subjective-evals) connects human evaluation, automatic evaluation, and monitoring of real usage.

The useful points from the article are:

- Define quality with human reviewers, concrete criteria, and examples before relying on automatic scores.
- Check agreement between humans. Resolve unclear criteria before treating their judgments as references.
- Evaluate the LLM judge against validated human judgments. Agreement between humans provides context for interpreting judge agreement.
- Report uncertainty. Repeated attempts reduce variation within a task but do not replace diverse tasks.
- Use actual user feedback to improve evaluation cases over time.

The article is a methodological overview. It does not establish that one judge, rubric, or sample size works for every subjective task.

## Project direction

Lucas identified three useful evaluation methods: deterministic checks, LLM judges, and human feedback. His previous PowerPoint workflow used human feedback. Use "presentation" when discussing that example.

Comparison reviews must hide model and skill identities from judges. Randomize output order and keep run metadata separate. This is a product requirement, recorded here during research. Judge inputs still need the task, source material, and required output constraints.

## Proposed starting flow

This is a proposal, not an implemented system or an approved architecture.

1. Establish the decision. Is the user checking one output, comparing skill versions, or testing an agent's reliability?
2. Collect the task, intended audience, requirements, and accepted or rejected examples.
3. Propose a mix of fixed checks, LLM judgments, and human review for those requirements.
4. Validate the criteria and judge on examples the user has reviewed. Keep separate examples for later checks.
5. Run matched comparisons and report evidence, failures, disagreements, cost, and uncertainty.

For presentation quality, an LLM judge needs rendered slides to assess appearance and source material to assess factual accuracy. A separate judging session prevents it from relying on the candidate's working conversation. A different model family is an experiment choice, not proof that the judge is accurate.

Proposed reasons for human review include missing evidence, disputed judgments, unfamiliar task types, and criteria the judge has not been validated to assess. Review a sample of accepted results too. A judge can approve a poor result without expressing uncertainty.

The first deliverable should be a short evaluation plan the user can inspect. Broad support for arbitrary file types and a production-monitoring platform can wait for evidence that they are needed.
