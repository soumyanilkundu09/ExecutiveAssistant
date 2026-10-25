---
name: research
description: Use this skill whenever Soumyanil asks to research, look into, dig into, investigate, get the lowdown on, or compare something — saree sourcing/vendors, fashion/market trends, competitors, trading or investing questions, tools and software, or any topic that needs digging across multiple sources rather than one quick lookup. Reach for this instead of running web searches directly, even if he never says the word "research" — phrases like "find out", "what's the deal with", "should I...", or "X vs Y" for a nontrivial topic all qualify. This skill loads Soumyanil's context (the Ma Lakhsmi Stores saree business, his trading/investing, his day job at LTIM, current priorities and goals) so the research is framed around what actually matters to him, then hands off to the deep-research skill for the multi-agent research and report writing.
---

# Personalized research

Soumyanil's "second brain" repo already has a general-purpose `deep-research` skill available (multi-agent: it decomposes a question, spawns research subagents, spawns a report-writer subagent, and delivers a narrative report). That skill is excellent at research but knows nothing about Soumyanil — it treats every question as context-free.

This skill's whole job is to sit in front of `deep-research` and add the two things it can't: knowing which of Soumyanil's goals this question actually serves, and putting the finished report where he'll find it again. Don't duplicate `deep-research`'s research or writing logic — just personalize the input and relocate the output.

## Process

### 1. Classify the topic

Read the user's request and place it in one category. This determines which context files matter and where the report ultimately lives.

| Category | Typical signals | Context to load |
|---|---|---|
| Business (Ma Lakhsmi Stores) | saree, sourcing, vendors, Surat, Burrabazar, Jalpaiguri, retail, inventory/POS, WhatsApp marketing, try-on tech, competitors in ethnic wear | `context/work.md` (saree section), `context/team.md`, `projects/ma-lakshmi-stores/README.md` |
| Trading / investing | stocks, F&O, swing trading, chart patterns, specific tickers, brokers, market rules | `context/work.md` (trading section) |
| Day job / career | LTIM, frontend development, frameworks, career moves | `context/me.md`, `context/work.md` (day job section) |
| General / other | anything that doesn't map to the above | `context/me.md` only, as light background |

Always load `context/current-priorities.md` and `context/goals.md` regardless of category — they tell you what's actually front-of-mind right now, which matters for the "why this matters" framing later.

Only stop and ask the user if the category is genuinely ambiguous *and* getting it wrong would send the research in a meaningfully different direction (e.g. "research POS systems" could be about the saree shop's billing counter or could be unrelated — worth a quick check). Don't ask when the category is reasonably clear; that's just friction. Keep any such question short, per the repo's communication style (casual, concise).

### 2. Enrich the question

Take the user's raw ask and fold in the specific constraints from the context you loaded — geography, business stage, timeline, budget scale, trading style, whatever's actually relevant. The goal is that `deep-research`'s subagents get a sharper brief than the user's one-liner would give them on its own, and that the final report naturally lands on what it means for Soumyanil rather than reading as a generic survey.

Also append one instruction to the question: that the report's conclusion should translate the findings into what they mean for Soumyanil specifically, given the priority or goal this research serves. Phrase it as part of the question, not as a separate meta-instruction — `deep-research`'s report writer already builds a BLUF-plus-conclusion report, so it will fold this in naturally if asked as a substantive part of what the report needs to answer.

For example, if he asks "should I look into Looksy AI or AI Vastra for the try-on tablets":

> Enriched question: Compare Looksy AI and AI Vastra as virtual try-on software for two tablets in the Premium Lounge of a saree retail store (Ma Lakhsmi Stores) launching in Jalpaiguri, West Bengal by ~April 2027, on a budget appropriate for a store projecting ~₹1.2–1.5 lakh/month revenue. Cover pricing/licensing, hardware requirements, accuracy for sarees specifically (drape, pleats, pallu), integration effort, and support for Indian retailers. Conclude with a clear recommendation of which one (if either) fits this store's stage and budget, and what the main risk of that choice is.

### 3. Determine the destination folder

- If the category matches an existing folder under `projects/` (right now, only `projects/ma-lakshmi-stores/`), the destination is `projects/<that-project>/research/`.
- Otherwise, the destination is a repo-root `research/` folder. Create either folder if it doesn't exist yet — don't ask permission, this is just organizing deliverables the same way `projects/` and `templates/` already are.

Work this out before calling `deep-research` so you're not scrambling to decide after the report lands.

### 4. Hand off to `deep-research`

Call the `Skill` tool with `skill: "deep-research"` and `args` set to the enriched question from step 2. Let it run its entire process untouched — follow-up questions, decomposition, parallel subagents, report writing, delivery. Don't intervene, don't re-ask things it's already asking, don't second-guess its subagent count or sourcing choices. It will tell you (and the user) the title it picked and where it saved `reports/{title}.md`.

### 5. Relocate the report

Once `deep-research` delivers, move `reports/{title}.md` from wherever it saved it into the destination folder from step 3, keeping the same filename. Leave `research_notes/{title}/` where it is — that's working scratch for the subagents, not the deliverable, and future research shares that same scratch space.

If this is the first research report for a project folder (e.g. the first one under `projects/ma-lakshmi-stores/research/`), and that project's `README.md` doesn't already point to its `research/` folder, add one short pointer line to the README in the same style as its existing links — don't rewrite the README, just add the pointer.

### 6. Offer to log a decision — once, never automatically

Read the relocated report's conclusion. If it contains a clear, actionable call (not just "here's the landscape" but "do X" or "pick Y over Z"), ask the user once whether to log it in `decisions/log.md`. If they say yes, append an entry using the exact existing format:

```
[YYYY-MM-DD] DECISION: ... | REASONING: ... | CONTEXT: ...
```

using today's date, the recommendation as the decision, the report's core reasoning, and a one-line pointer back to the report's path as context. Never write to the decision log without being asked — if the report doesn't land on anything actionable, or the user declines, skip this step silently.

### 7. Summarize for the user

Close with a short, bulleted, casual summary per `.claude/rules/communication-style.md`: what was found (1-2 lines), where the full report now lives, and whether anything got logged as a decision.
