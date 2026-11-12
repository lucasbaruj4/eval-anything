---
name: eval-anything
description: Check whether a skill improves text outputs when the user requests an evaluation, or offer a check after creating or changing a skill that affects text. Use for new skills and revisions, including subjective writing quality.
---

# Eval anything

Help the user decide whether a skill produces better text. Use their existing agent environment. This version supports text outputs.

## Start

On a direct request, start the conversation. After finishing a relevant skill change, offer once: "Would you like to check whether this works as intended?" Wait for acceptance. Remember a decline for that change during this conversation. Limit automatic offers to relevant skill changes outside an evaluation.

Use plain language. Explain each choice before asking for it. Ask one question at a time and reuse information already available.

## 1. Understand the change

Identify the skill, its intended audience, and the behavior it should change. Compare a new skill with no skill, or a revision with its previous version. Preserve the versions before running.

Suggest a few realistic requests using the user's context. Agree on required facts, unacceptable failures, and subjective preferences. Allow the user to start with vague statements about subjective preferences such as "I will know when I see it."

## 2. Explain the work

Read [Text comparisons](references/text-comparisons.md) before proposing runs. Check which fresh agent sessions and models are available. Explain missing capabilities instead of assuming access.

For example: "An agent will try the same requests with each version. A separate agent will review anonymous results. You will review some examples first so we can check whether its judgments match yours."

Propose the requests, versions, model choices, number of attempts, and review steps. Explain any model choice before requesting a preference. Start small. Get agreement on that scope before running. A direct evaluation request already accepts the invitation.

Describe usage without promising a price. Get agreement before expanding the run or using another provider.

## 3. Learn from examples

Run the agreed initial examples using the reference. Show one anonymous pair at a time. Ask: "Which would you use: A, B, either, or neither?" Then invite an optional reason: "What stands out?"

Suggest concrete criteria from the user's reactions and ask whether you understood. Keep requirements separate from preferences. Check the criteria on other examples the user has not helped tune. If preferences conflict, clarify the audience or criterion.

Compare the independent reviewer's decisions with the user's saved choices without showing those choices to the reviewer. Record disagreements. If no human choices are available, report the reviewer's views as unvalidated.

## 4. Compare

Follow the matched-run and blind-review procedure in the reference. Apply fixed checks to facts and explicit requirements. Use the reviewer for qualities that need judgment. Keep failed attempts in the record and comunicate them to the user.

Send disputed or unsupported judgments to the user. Also ask the user to review a sample of accepted results. More model agreement does not establish human agreement.

## 5. Report

Lead with the decision the evidence supports, including "not enough evidence yet." Link the actual outputs and explain failures and disagreements.

Report task and attempt counts, required-check results, human preferences, reviewer agreement, and available usage information. Keep repeated attempts on one task separate from coverage across tasks. A small initial check is exploratory.

Save the agreed plan, skill versions, prompts, outputs, checks, and judgments in a local location the user accepts, make sure to ask the user for this location before writing to disk. Record missing evidence. Keep reusable criteria for the next run. Leave skill changes for a separate agreed task.
