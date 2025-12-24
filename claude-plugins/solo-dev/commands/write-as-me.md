---
description: Generate text in your voice using your AUTHOR_VOICE.md document. Provide a topic or prompt as argument.
allowed-tools: ["Read", "Write", "Task", "AskUserQuestion", "Glob"]
argument-hint: [topic or writing prompt, e.g., "a tweet about productivity" or "blog intro on AI tools"]
---

# Write As Me

Generate content in the user's authentic voice using their AUTHOR_VOICE.md document.

## Arguments

$ARGUMENTS

## Process

### Step 1: Locate Voice Document

Search for AUTHOR_VOICE.md in this order:
1. Current working directory: `./AUTHOR_VOICE.md`
2. Home directory: `~/AUTHOR_VOICE.md`
3. Use Glob to search: `**/AUTHOR_VOICE.md`

If not found, inform the user:
"No AUTHOR_VOICE.md found. Run `/craft-voice` first to create your voice profile."

### Step 2: Read Voice Document

Read the full AUTHOR_VOICE.md and internalize:
- Voice identity and tone parameters
- Structural patterns
- Vocabulary rules (USE and AVOID lists)
- Signature moves
- Anti-patterns to avoid

### Step 3: Clarify Request (if needed)

If arguments are vague or missing, use AskUserQuestion:

**If no topic provided:**
- header: "Topic"
- question: "What would you like me to write about?"
- freeform: true

**Clarify format:**
- header: "Format"
- question: "What format should this be?"
- options:
  - "Twitter/X post (single tweet)"
  - "Twitter/X thread (multi-tweet)"
  - "LinkedIn post"
  - "Blog intro paragraph"
  - "Full blog section"
  - "Newsletter segment"
  - "Email"
  - "Comment/reply"

**Clarify length (if applicable):**
- header: "Length"
- question: "How long should this be?"
- options:
  - "Short (1-2 sentences)"
  - "Medium (1-2 paragraphs)"
  - "Long (3+ paragraphs)"

### Step 4: Generate Content

Write content that:

1. **Opens strong** - Use the opening style from the voice doc
2. **Matches tone** - Follow tone parameters exactly
3. **Uses signature moves** - Incorporate at least one signature element
4. **Follows vocabulary rules** - Use approved words, avoid banned ones
5. **Maintains structure** - Match paragraph and sentence patterns
6. **Avoids anti-patterns** - Double-check against the NEVER list

### Step 5: Present and Iterate

Present the generated content to the user.

Use AskUserQuestion:
- header: "Result"
- question: "How's this?"
- options:
  - "Perfect - use as is"
  - "Good - minor edits needed"
  - "Okay - needs adjustment"
  - "Off - try again"

If not "Perfect", ask what to adjust:
- header: "Adjust"
- question: "What should I change?"
- multiSelect: true
- options:
  - "Make it shorter"
  - "Make it longer"
  - "More casual tone"
  - "More professional tone"
  - "Stronger hook/opening"
  - "Different angle"
  - "Add specific point"
  - "Remove something"

Regenerate based on feedback until satisfied.

### Step 6: Output Options

Once approved, ask:
- header: "Output"
- question: "What do you want to do with this?"
- options:
  - "Copy to clipboard (show final text)"
  - "Save to file"
  - "Just show me the final version"

## Examples

**Input:** `/write-as-me a tweet about why most productivity advice is wrong`

**Process:**
1. Read AUTHOR_VOICE.md
2. Note: user has "Provocateur" voice, uses "Contrarian takes"
3. Generate tweet with strong hook, contrarian angle, matches vocabulary
4. Present for feedback
5. Iterate if needed

**Input:** `/write-as-me`

**Process:**
1. Ask for topic
2. Ask for format
3. Read voice doc
4. Generate
5. Iterate

## Voice Compliance Checklist

Before presenting content, verify:

- [ ] Tone matches voice doc parameters
- [ ] Uses words from the USE list
- [ ] Avoids words from the AVOID list
- [ ] Includes at least one signature move
- [ ] Structure matches documented patterns
- [ ] Opening follows the voice doc style
- [ ] No anti-patterns present
- [ ] Appropriate length for format
