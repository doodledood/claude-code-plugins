# First-Principles Prompting: Derived from LLM Training

> **Purpose**: Practical prompting strategies derived directly from how LLMs are trained. Every recommendation traces back to a training mechanism, not intuition or folklore.

---

## Core Premise

Every LLM behavior emerges from training objectives. Effective prompting means:
- **Activating** patterns the training rewarded
- **Compensating** for what training couldn't address
- **Avoiding** triggers that activate unwanted behaviors

---

## Principle 1: Work WITH Next-Token Prediction

**Training reality**: Models generate left-to-right, one token at a time. They cannot "see ahead" or plan holistically.

### Do This

**Sequential decomposition** — structure tasks so each step informs the next:

```
First, identify the core problem.
Then, list the constraints.
Then, propose a solution that satisfies those constraints.
Finally, verify your solution against each constraint.
```

**Make reasoning explicit** — force intermediate tokens that build toward the answer:

```
Before answering, work through:
1. What are the key facts?
2. What are the relationships between them?
3. What follows logically?
```

**Use "think step by step" variants** — this works because it forces the model to generate reasoning tokens before conclusion tokens:

```
Think through this carefully before answering.
```

### Don't Do This

```
"Give me a comprehensive plan that accounts for all edge cases"
(Requires holistic view the model can't have while generating)

"Make sure the beginning is consistent with the end"
(Model can't see the end when writing the beginning)
```

---

## Principle 2: Defeat Reward Hacking

**Training reality**: RLHF optimizes for what *looks good* to humans/reward models, not what *is* good. This creates verbose, confident-sounding, sycophantic outputs.

### Do This

**Specify anti-patterns explicitly**:

```
Be concise. If you don't know, say so. Don't pad your response.
Disagree with me if I'm wrong.
```

**Request specific artifacts, not qualities**:

```
Good: "Return only the function signature and a one-line docstring"
Bad:  "Give me a thorough, high-quality answer"
```

**Provide verification criteria upfront**:

```
Your answer is correct if:
1. It compiles without errors
2. It handles the empty input case
3. It runs in O(n) time

Check your answer against these criteria before responding.
```

**Ask for confidence calibration**:

```
Rate your confidence (low/medium/high) and explain what would make you uncertain.
```

### Don't Do This

```
"Give me the best possible answer"
(Activates reward-hacked "impressive-looking" patterns)

"Be thorough and comprehensive"
(Triggers verbosity that was rewarded in training)

"What do you think about my approach?"
(Invites sycophantic agreement)
```

---

## Principle 3: Manage Attention Architecture

**Training reality**: Transformers have U-shaped attention—strong at context start and end, weak in the middle. Information degrades over long contexts.

### Do This

**Put critical constraints at the END** (highest attention):

```
[Long context here...]

CRITICAL REQUIREMENTS (must satisfy all):
- Must be thread-safe
- Must not allocate memory
- Must return within 10ms
```

**Repeat key information** at strategic points:

```
Remember: you are acting as a security auditor. Your goal is to find vulnerabilities.

[... long task description ...]

As a security auditor focused on finding vulnerabilities, now analyze:
```

**Summarize before synthesis**:

```
Before writing your final answer, first list:
1. The 3 most important facts from the above
2. The key constraint that must not be violated
Then write your answer.
```

### Don't Do This

- Putting critical requirements in paragraph 3 of 10
- Assuming the model "remembers" something from 5000 tokens ago
- Long contexts without repetition of key points

---

## Principle 4: Externalize State

**Training reality**: LLMs can reliably track only 5-10 variables. No persistent memory across sessions. Context drift causes "forgetting" within sessions.

### Do This

**Make the model write things down**:

```
As you investigate, maintain a running list of findings.
After each step, update your findings list before proceeding.
```

**Use structured formats for tracking**:

```
Track your progress using this format:
KNOWN: [facts established]
UNKNOWN: [questions remaining]
NEXT: [immediate next step]
```

**Chunk complex tasks with explicit state transfer**:

```
Step 1: Analyze the requirements. Output a numbered list.
Step 2: For each requirement in your list, identify implementation approach.
Step 3: For each approach, write the code.
```

### Don't Do This

```
"Keep track of all the edge cases as you go"
(Model will lose track after ~5)
```

- Multi-step tasks without explicit state checkpoints
- Assuming the model maintains consistent internal state

---

## Principle 5: Leverage Constitutional Training

**Training reality**: Models are trained to follow explicit principles and evaluate their own outputs against guidelines. Constitutional AI makes them responsive to stated rules.

### Do This

**State principles explicitly**:

```
Principles for this task:
1. Correctness over completeness—a partial correct answer beats a complete wrong one
2. Admit uncertainty—"I don't know" is acceptable
3. Preserve existing behavior—don't change what works
```

**Use self-evaluation prompts**:

```
Before finalizing, check:
- Does this actually solve the stated problem?
- Did I introduce any new issues?
- Am I confident this is correct?
```

**Frame constraints as guidelines, not restrictions**:

```
Good: "Follow the principle: minimal changes to achieve the goal"
Bad:  "Don't change too much stuff"
```

### Don't Do This

- Implicit expectations the model should "just know"
- Vague quality requirements ("make it good")
- Assuming the model shares your unstated values

---

## Principle 6: Compensate for Statistical Knowledge

**Training reality**: Knowledge comes from token co-occurrence statistics. Common patterns are strong; rare patterns are weak or wrong. Models can't distinguish "true but rare" from "false but common."

### Do This

**Provide examples for unusual tasks**:

```
I need a function that does X. Here's an example of the pattern I want:
[example]
Now apply this pattern to:
[actual task]
```

**Supply domain-specific facts**:

```
Context: In this codebase, we use `Result<T, E>` for all fallible operations.
Errors are logged via `tracing::error!`. Never use `unwrap()` in production code.
```

**Ask for sources of uncertainty**:

```
What aspects of this question might you be uncertain about?
What would you need to verify?
```

### Don't Do This

- Assuming accuracy on niche/specialized topics
- Trusting confident-sounding claims without verification
- Asking for "the latest" information (training cutoff)

---

## Principle 7: Activate Tool Use Training

**Training reality**: Agency training makes models good at using tools when the need is clear. But accuracy degrades with many tools, and models may not know when tools would help.

### Do This

**Make tool needs explicit**:

```
You have access to file search. USE IT before making claims about the codebase.
Don't guess at file locations—search for them.
```

**Reduce tool choice paralysis**:

```
For this task, you'll primarily need:
- Read: to examine files
- Edit: to make changes
- Bash: only for running tests
```

**Verify tool results**:

```
After making changes, verify by:
1. Reading the file back
2. Running the tests
3. Confirming the output matches expectations
```

### Don't Do This

- Assuming the model will proactively use tools
- Providing 50 tools without guidance on which to use
- Trusting tool use without verification

---

## Meta-Principle: Structure Over Instruction

**The fundamental insight**: LLMs follow structure more reliably than instruction. Structure creates token-level patterns that guide generation; instructions are just content to be processed.

### Structure beats instruction

| Instruction (Weak) | Structure (Strong) |
|-------------------|-------------------|
| "Be concise" | Enforce a format: "Answer in ≤3 sentences" |
| "Think carefully" | Require explicit steps: "First X, then Y, then Z" |
| "Don't make mistakes" | Require verification: "Check your answer against [criteria]" |
| "Remember the requirements" | Repeat them: Place at end of prompt |
| "Track your progress" | Provide format: "Update this list after each step: [format]" |

---

## Quick Reference: Prompting Patterns

| Training Mechanism | Prompting Pattern |
|-------------------|-------------------|
| Next-token prediction | Sequential decomposition; explicit reasoning steps |
| Reward hacking (RLHF) | Specific artifacts > quality words; state anti-patterns |
| U-shaped attention | Critical info at END; repeat key points |
| Limited working memory | Externalize state; structured tracking formats |
| Constitutional AI | Explicit principles; self-evaluation prompts |
| Statistical knowledge | Provide examples; supply domain facts; ask for uncertainties |
| Tool use training | Make tool needs explicit; reduce choice paralysis |

---

## Example: Applying All Principles

**Bad prompt**:
```
Review this code and make it better.
```

**Good prompt** (with principles noted):

```
[PRINCIPLE 6: Supply domain facts]
Context: This is a Python async service. We use `asyncio.gather` for
concurrency and `structlog` for logging. Errors should raise, not return None.

[PRINCIPLE 2: Specific artifacts, not qualities]
Review this code for:
1. Bugs that would cause incorrect behavior
2. Error handling gaps
3. Race conditions

[PRINCIPLE 1: Sequential decomposition]
For each issue found:
- State the problem in one sentence
- Show the problematic code
- Show the fix

[PRINCIPLE 4: Externalize state]
Track issues as you find them. After reviewing, list all issues before proposing fixes.

[PRINCIPLE 5: Self-evaluation]
Before finalizing, verify:
- Each fix addresses exactly one issue
- No fix introduces new problems
- Fixes are minimal (don't refactor unrelated code)

[PRINCIPLE 3: Critical constraints at END]
IMPORTANT: Only report real bugs. Do not suggest stylistic improvements,
performance optimizations, or "nice to haves". If no bugs exist, say "No bugs found."
```

---

## Summary

This framework treats prompting as **engineering for a specific system architecture**, not persuasion or communication. The model isn't understanding your intent—it's generating tokens based on patterns. Structure those patterns deliberately.

| Don't Think Of It As... | Think Of It As... |
|------------------------|-------------------|
| Asking a person | Programming a pattern matcher |
| Giving instructions | Structuring token generation |
| Hoping for understanding | Engineering for predictable outputs |
| Trusting intelligence | Compensating for known limitations |

---

## Related Documents

- **[LLM_TRAINING.md](./LLM_TRAINING.md)** — Deep dive into how LLMs are trained (the basis for these principles)
- **[LLM_CODING_CAPABILITIES.md](./LLM_CODING_CAPABILITIES.md)** — LLM strengths and limitations for coding tasks

---

*Derived from: LLM_TRAINING.md analysis*
*Last updated: 2026-01-18*
