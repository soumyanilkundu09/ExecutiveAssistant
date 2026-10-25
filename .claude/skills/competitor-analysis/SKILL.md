---
name: competitor-analysis
description: Use this skill whenever Soumyanil wants a competitor analysis, competitive research, or feature/market scan against similar players — "do a competitor analysis on X", "who are my competitors", "what are other [saree sellers / AI lead-gen tools / brokers] doing that I'm not", "compare me against the market", "what features should I be matching", "benchmark X against its competitors", or "check in on my competitors again". Works for ANY subject he names, not just his own ventures — his own business (Ma Lakhsmi Stores), a trading-adjacent tool/category, or a fully general external topic with no existing project (e.g. "AI lead-gen tools", "note-taking apps"). Always asks per-run what competitive scope he means (local/regional, national, or broader feature-inspiration products) rather than assuming. Shortlists ~4-5 candidate competitors for approval before doing the expensive research, runs one deep-dive per approved competitor, then delivers a Core-feature vs Differentiator-feature breakdown with ranked feature combinations, and maintains a persistent tracker file per subject that gets refreshed and diffed (not overwritten) on every later re-run. This is NOT for a single quick "what does X do" lookup on one company — use `research` for that — and NOT for scoring one of Soumyanil's own ideas in isolation — use `business-validator` for a GO/NO-GO teardown. This skill is specifically for mapping multiple competitors side by side, pulling out what's working for them, and tracking that market over time.
---

# Competitor Analysis

Soumyanil wants to be able to point this skill at any subject — his own saree business, a tool category he's evaluating, a trading-adjacent niche, anything — and get back a side-by-side read of who the real players are, what they offer, and what he should build or match. The point isn't a single research report; it's a living view of a market that gets cheaper and sharper to refresh every time he comes back to it.

This is a sibling to `research` (which answers one question well) and `business-validator` (which teardowns one idea in isolation). This skill's job is specifically comparative and ongoing: multiple competitors, mapped against each other, tracked over time.

## Process

### 0. Classify the subject and load context

Place the subject in one bucket, the same way `research` classifies its topics:

| Category | Typical signals | Context to load |
|---|---|---|
| Business (Ma Lakhsmi Stores) | saree, sourcing, retail, Jalpaiguri, in-store tech, "my competitors", "my store" | `context/work.md` (saree section), `context/team.md`, `projects/ma-lakshmi-stores/README.md` |
| Trading / investing | brokers, trading platforms, specific trading tools/categories | `context/work.md` (trading section) |
| Day job / career | LTIM, frontend tooling/frameworks, employer-adjacent tools | `context/me.md`, `context/work.md` (day job section) |
| General / external | a tool category, product type, or market with no tie to Soumyanil's own ventures (e.g. "AI lead-gen tools", "note-taking apps") | none — treat as a cold-start subject, skip personal context entirely |

If the subject matched Business/Trading/Day-job, also load `context/current-priorities.md` and `context/goals.md` — they feed the "fit adjustment" in step 7 and the positioning paragraph in step 6's subagent briefs. If the subject is General/external, don't load any personal context at all; there's nothing of Soumyanil's own to compare against, and dragging it in would just bias a market scan that should stay objective.

Only stop and ask (via `AskUserQuestion`) if the bucket is genuinely unclear and getting it wrong would send the whole run in a different direction. Don't ask when it's reasonably obvious — that's just friction.

### 1. Capture any business info Soumyanil volunteers

If the subject matched an existing project and he mentions new or changed details about his own business as part of the request — updated positioning, a feature he just shipped, a changed revenue figure, a competitor he's already spotted — fold that into the existing `context/work.md` section and/or `projects/<name>/README.md` in place. Edit or append the relevant section; don't spin up a new dedicated file for this. Skip this step entirely for General/external subjects — there's no "his own business" file to update.

### 2. Determine the output destination

Same logic `research` uses for its destination:

- If the subject matches an existing folder under `projects/`, the destination is `projects/<that-project>/research/`.
- Otherwise, the destination is a repo-root `research/` folder.

Create either folder on first use without asking — this is just organizing deliverables, same as `projects/` and `templates/` already are.

Pick a Title Case name for the subject (not a kebab-slug) to use in file names going forward — e.g. "Ma Lakhsmi Stores Local Saree Sellers" or "AI Lead-Gen Tools". Everything downstream keys off this title.

### 3. Check for an existing tracker

Look for `<destination>/<Subject Title> Competitor Tracker.md`.

- **Found** → this is a refresh run. Read it in full: the recorded scope, the approved competitor set, the current snapshots, the feature landscape, and the change log. Tell the user in one line what you found before continuing (e.g. "Found an existing tracker for this, last updated 2026-08-12, tracking 4 competitors — refreshing it.").
- **Not found** → this is a first run.

### 4. Confirm competitive scope — every run, never assumed

Scope changes what "competitor" even means for a given subject, so ask every time via `AskUserQuestion` rather than guessing:

- **Local/regional direct competitors** — the players actually fighting for the same customers in the same geography.
- **National/major players** — the bigger, more established names in the same space.
- **Broader feature-inspiration products** — not direct competitors at all, but worth stealing good ideas from.

On a first run, ask fresh with no default suggested. On a refresh run, show the scope already recorded in the tracker and ask whether to keep it or change it for this pass — the market or the question behind it may have shifted since last time.

### 5. Shortlist 4-5 candidates — confirm before the expensive step

This is a deliberate cheap checkpoint before the costly part of the workflow: it's much cheaper to fix a wrong shortlist now than to discover five deep-dive subagents researched the wrong set of companies.

- **First run:** run a lightweight `WebSearch` scoping pass (1-2 queries, not subagents) to surface ~4-5 candidates matching the subject and the approved scope, each with a one-line "why this one" note. Present the shortlist via `AskUserQuestion` (multi-select, plus a free-text option to add one of the user's own) for approval or edits.
- **Refresh run:** show the previously-approved set from the tracker and ask via `AskUserQuestion` whether to keep it as-is, drop anyone, add anyone by name, or also run a fresh scoping pass to catch new entrants to the market.

Do not move on to subagent dispatch until the user has explicitly approved the final list for this run.

### 6. Dispatch one deep-dive subagent per approved competitor

For each approved competitor, launch an `Agent` (`general-purpose` type). Batch 3-5 concurrently — same cap `fundamental-stock-analysis` uses for its per-ticker research — rather than firing all of them at once.

Every subagent prompt must be fully self-contained, since subagents share no memory with you or each other. Fill in the `{...}` placeholders and send this template as-is:

```
You are researching ONE competitor as part of a competitor analysis for Soumyanil. You have no memory of any other conversation — everything you need is in this prompt.

SUBJECT BEING ANALYZED: {SUBJECT}
COMPETITIVE SCOPE FOR THIS RUN: {SCOPE_TYPE}
COMPETITOR TO RESEARCH: {COMPETITOR_NAME}

{IF SUBJECT IS SOUMYANIL'S OWN VENTURE, INCLUDE:}
FOR CONTEXT, SOUMYANIL'S OWN OFFERING: {one-paragraph positioning pulled from context/work.md or projects/<project>/README.md}
As you research, note anywhere this competitor's features compare directly to what Soumyanil already has or plans.

{IF THIS IS A REFRESH RUN, INCLUDE:}
This competitor was last researched on {LAST_CHECKED_DATE}. Here is what was found then: {PRIOR SNAPSHOT}. Specifically check whether anything has changed since then (new features, pricing changes, new reviews/press, funding, leadership) and call that out explicitly.

Research this competitor and return a STRUCTURED SUMMARY under these exact headers — not a transcript of your searches:

1. Identity & scale — legal entity/brand (flag if the name resolves to multiple unrelated companies), website, years operating, funding/headcount if known, geographic footprint.
2. Positioning — one paragraph: how they position themselves and to whom.
3. Pricing & packaging — model, tiers, currency, what's included at each tier.
4. Basic / table-stakes features — bullet list of features standard for any player in this space.
5. Advanced / differentiating features — bullet list of features that are NOT universal, the things that make this competitor stand out.
6. What's working for them — traction signals: reviews/ratings, press mentions, named clients, growth signals, social proof. Cite source + rough date for each.
7. What's not working / weaknesses — documented complaints, gaps, unverified marketing claims (treat unsubstantiated claims like "100% accuracy" with explicit skepticism, don't repeat them as fact).
8. Changes since last check — only if a prior snapshot was given above; otherwise omit this section.
9. Watch-this-next signal — the single clearest thing to keep an eye on for this competitor.

Cite rough figures with source and date where possible so stale numbers aren't presented as current without caveat.
```

### 7. Synthesize — this step is yours, not the subagents'

Once every subagent reports back, compute the rest yourself:

1. **Merge basic features.** Dedupe every subagent's "basic/table-stakes" list into one master list. For each feature, record how many of the N researched competitors have it, as `x/N`.
2. **Merge advanced features.** Do the same for every "advanced/differentiating" list, same `x/N` count per feature.
3. **Split advanced features into Core vs Differentiator**, by this rule, stated plainly in the output so Soumyanil can see the logic rather than take it on faith:
   - **Core Feature candidate** — present in **≥50%** of researched competitors' advanced-feature lists. Advanced today, but trending toward table-stakes — what you need just to not fall behind.
   - **Differentiator Feature candidate** — present in **<50%**. A minority or unique feature — what would actually set Soumyanil apart rather than just catch him up.
4. **Generate every 2-Core + 1-Differentiator combination.** Cap the chat output to the **top 5-8** by priority score, and mention the total number of combinations generated.
5. **Score each combo transparently:**
   - Base score = the sum of the `x/N` fractions of the 3 features involved.
   - **+ synergy bonus** if 2 or more of the 3 features were called out together in the same competitor's "what's working for them" section — a sign they succeed as a bundle, not in isolation.
   - **+ fit adjustment**, only when personal context was loaded in step 0 (i.e. the subject is Soumyanil's own venture) — boost combos that fit his current priorities, budget, or stage from `context/current-priorities.md`. State this adjustment explicitly in the "why" column; never let it be a hidden thumb on the scale.

On a refresh run, also diff the new synthesis against the tracker's prior state — competitors added or dropped, features gained or lost per competitor, any resulting shift in which combo ranks highest — before moving to step 8.

### 8. Write or update the two output files

In the destination folder from step 2, Title Case naming:

- **`<Subject Title> Competitor Analysis.md`** — a one-off narrative report: bolded key claims, inline citations with source and rough date, prose style (match the tone of `projects/ma-lakshmi-stores/research/Looksy AI versus AI Vastra.md` as a style reference). Overwrite this file in full every run — it's a point-in-time snapshot, not the running record.
- **`<Subject Title> Competitor Tracker.md`** — the persistent record. Use this exact structure:

```markdown
# <Subject Title> — Competitor Tracker

**Scope:** <scope type chosen this run>
**Last updated:** <YYYY-MM-DD>

## Approved Competitor Set
- <Name 1> — approved <date>
- <Name 2> — approved <date>

## Current Competitor Snapshots
### <Name 1>
(latest structured findings from that competitor's subagent: identity, positioning, pricing, basic features, advanced features, traction, weaknesses, watch-next, source links + dates)

## Feature Landscape (as of last update)
- Basic features table
- Advanced features table
- Core vs Differentiator split table
- Top combo table

## Change Log
[2026-10-24] Initial tracker created. Competitors: X, Y, Z. <1-line summary of findings.>
[2026-12-01] Refresh run. Added: <name> | Dropped: <name> | Changed: <competitor> now offers <feature> (new) | Combo ranking shift: <old top combo> -> <new top combo>, because <reason>.
```

There's no separate shortlist-confirmation file — the approved competitor set lives in the tracker's own `## Approved Competitor Set` section, which is also what a refresh run reads back in step 3/5.

**Diff mechanism on refresh:** compute the delta against the tracker's *current* `## Feature Landscape` and `## Current Competitor Snapshots` sections before overwriting them, write that delta as one new dated line in `## Change Log`, then overwrite the snapshot and landscape sections with the fresh state. History lives only in the change log, not in accumulating old snapshots — the tracker stays a manageable size while still giving Soumyanil a running "what changed, when" view.

### 9. Add a README pointer — first time only

If this is the first file this skill has placed in a given project's `research/` folder, and that project's `README.md` doesn't already link to its `research/` folder, add one short pointer line in the same style as its existing links. Don't rewrite the README — just add the pointer.

### 10. Deliver the output in chat

Post the synthesis directly in chat as exactly three tables, in this order — this is the deliverable Soumyanil actually reads; the files above are the record:

**Table 1 — Full feature inventory**

| Feature | Type (Basic/Advanced) | Competitors with it (x/N) |
|---|---|---|

**Table 2 — Core vs Differentiator split**

| Feature | Classification | Competitors with it (x/N) | Why |
|---|---|---|---|

**Table 3 — Top combos, descending priority**

| Rank | Core Feature 1 | Core Feature 2 | Differentiator Feature | Why this combo | Competitors demonstrating it |
|---|---|---|---|---|---|

### 11. Offer to log a decision — once, never automatically

If the synthesis landed on a clear, actionable call — a specific recommended combo, or an explicit "you're missing a Core feature everyone else already has" flag — ask once whether to log it in `decisions/log.md`. If accepted, append:

```
[YYYY-MM-DD] DECISION: ... | REASONING: ... | CONTEXT: ...
```

using today's date, the recommended combo or action as the decision, the priority-score reasoning (feature coverage + synergy + fit) as the reasoning, and a one-line pointer to both file paths as context. If declined or there's no response, drop it silently — never ask twice, and never log automatically on a flat landscape-only result with no real call to make.

### 12. Summarize for the user

Close with a short, bulleted, casual summary per `.claude/rules/communication-style.md` — competitor count, the top combo in one line, both file paths, and whether anything got logged as a decision. The three tables in step 10 are the documented exception to the "under 3 sentences" rule, the same way other skills' report or workbook outputs are exempt.
