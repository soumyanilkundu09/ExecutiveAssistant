---
name: fundamental-stock-analysis
description: Use this skill whenever Soumyanil wants a fundamentals/valuation screen on one or more stocks — "run a fundamental analysis on these stocks", "screen this watchlist", "give me a buy/sell/wait call on [ticker]", "is [stock] over/undervalued", "check the PEG/EV-EBITDA on X", "what's the moat on Y", or when he hands over an Excel sheet of tickers and wants them rated. Covers both Indian (NSE/BSE) and US equities. This is NOT for technical/chart/price-action/RSI analysis — route those requests to the separate `malkan-score` skill instead, since that one handles the GFS 12-parameter technical scoring. This is also NOT a deep accounting-quality, governance, or red-flag forensic dive on Indian names — the separate `forensic-compounder` skill already owns that; this skill only surfaces it once as an optional follow-up, never runs it itself. Trigger even if Soumyanil never says "fundamental" explicitly, as long as the ask is grounded in financials — valuation, growth, debt, dividends, competitive moat, or a buy/sell/hold call — rather than chart patterns or price action.
---

# Fundamental Stock Analysis

Soumyanil occasionally hands over a watchlist — a few tickers typed in chat, or an Excel sheet with a column of symbols — and wants them screened the way a senior sell-side equity analyst would screen names for a high-net-worth client: fundamentals, valuation, growth, risk, and a definitive call per stock. This skill runs that screen and lands the output in an Excel workbook he can act on, not just a wall of chat text.

Adopt that voice for the analysis: a senior equity analyst with two decades screening stocks for HNW clients — rigorous about numbers, willing to say "wait" or "sell" when the fundamentals don't support a buy, and allergic to hedge-everything language. The point of this skill is a clear call per stock, not a balanced-sounding summary that doesn't actually commit.

This skill is sized for a watchlist, not a universe — roughly 5–20 tickers per run. If Soumyanil hands over more than that, say so and ask whether to trim the list or run it anyway (it'll just take longer and burn more research calls).

## Process

### 0. Parse the input and classify each ticker

Figure out what was handed over:

- **Excel file path** — read it (use the `xlsx` skill) and pull the ticker column (and sector column, if present).
- **Typed list in chat** — just use it directly.

For each ticker, classify the market it trades on — Indian (NSE/BSE) or US — from the suffix (`.NS`, `.BO`) or obvious context (a well-known Indian company name, rupee-denominated discussion, etc.) if no suffix is given. This matters downstream: currency (₹ vs $), which comparable sector averages make sense, and whether to surface the `forensic-compounder` note at the end.

### 1. Research each stock — delegate it, don't do it inline

Gathering P/E, five-year revenue history, debt-to-equity, dividend history, consensus estimates, and moat signals for even five stocks means a lot of raw web search output — more than belongs in the main conversation. So for each ticker, launch a research sub-agent (`Agent` tool, `general-purpose` type) rather than searching inline yourself. Batch a handful at a time (e.g. 3–5 concurrent) rather than firing off all 20 at once.

Give each sub-agent a self-contained brief naming the ticker, its market, and exactly what to come back with — it has no memory of this conversation, so it needs the full ask in the prompt. Ask it to return a structured summary, not a transcript of its searches:

- Current P/E, and the sector/peer-group average P/E for comparison
- Revenue for each of the last 5 fiscal years (or as many as available) and the resulting trend
- Total debt, total equity, and the resulting debt-to-equity ratio, plus a brief health read (comfortable / stretched / risky)
- Trailing dividend yield, payout ratio, and whether that payout looks sustainable against free cash flow
- EV/EBITDA, and whatever forward-earnings guidance or consensus growth estimate exists to judge whether that multiple is cheap, fair, or rich
- Consensus (or best-available estimate) for next quarter's revenue and EPS
- Qualitative moat signals — pricing power, brand, switching costs, network effects, regulatory position — with enough detail for you to grade it in the next step
- Analyst price targets or recent guidance that would inform a bull/bear 12-month range
- Any single metric that's the clearest "watch this next" signal for that specific company (an upcoming product cycle, a debt maturity, a regulatory decision, a margin inflection)

Tell the sub-agent to cite rough figures with their source/date where possible (e.g. "P/E ~24x per Screener.in, Oct 2026") so you're not presenting stale numbers as current without caveat.

### 2. Score and synthesize — this step is yours, not the sub-agent's

Once a sub-agent reports back, you compute and judge the rest directly:

- **PEG ratio** — P/E divided by the expected earnings growth rate. Below ~1 is cheap for its growth, above ~2 is rich; say where it lands and why.
- **EV/EBITDA justified-or-not verdict** — don't just report the multiple; state plainly whether it's justified given the forward-earnings picture the sub-agent found, or whether the market's pricing in more growth than the numbers support.
- **Moat rating** — weak / moderate / strong, with one sentence of reasoning tied to the specific signals the sub-agent surfaced (not a generic "strong brand" unless you can say what that actually protects).
- **Risk rating, 1–10** — 1 is sleep-well-at-night, 10 is speculative. Justify it in a sentence referencing the specific risk (leverage, customer concentration, regulatory exposure, valuation downside) — a number with no reasoning is useless to Soumyanil.
- **Bull case** — the specific scenario that gets this stock higher, a 12-month price target, and the implied % upside.
- **Bear case** — the specific scenario that breaks the thesis, a 12-month downside target, and the implied % downside.
- **Key metrics to watch** — carry forward the sub-agent's "watch this next" signal, sharpened if needed.
- **Final recommendation** — Buy / Sell / Wait. A "Wait" means the story's fine but the entry point or current valuation isn't, and that distinction matters — don't collapse everything into Buy or Sell.

### 3. Build the two-sheet workbook

Invoke the `xlsx` skill (via the `Skill` tool) to build one workbook with exactly two sheets:

1. **"Stock Screen"** — one row per ticker, columns for every field above (P/E, sector P/E, revenue trend, D/E + health read, dividend yield + sustainability, moat rating, PEG, EV/EBITDA + verdict, next-quarter consensus revenue/EPS, bull case + target + upside%, bear case + target + downside%, risk rating + reasoning, key metric to watch, and the final recommendation). Use ₹ or $ per each stock's market. This sheet IS the Buy/Sell/Review view Soumyanil asked for — sort or group it so Buy/Sell/Wait names are easy to scan at a glance (e.g. sort by recommendation).
2. **"Buy Justification"** — a narrative paragraph for each **Buy-rated stock only** (skip anything rated Sell or Wait), explaining which specific metrics drove the call. This is the "why" sheet for the names actually worth acting on.

### 4. Save the file

Save to `reports/stock-analysis/<date>_<short-name>.xlsx` in this repo, where `<date>` is today's date (`YYYY-MM-DD`) and `<short-name>` is a short slug for the run (e.g. the first ticker, or a name Soumyanil gave the list). Create `reports/stock-analysis/` if it doesn't exist yet — this repo already has a `reports/` folder at its root, so this is just a subfolder under it, not a new top-level convention.

### 5. Flag the forensic-compounder follow-up — once, if relevant

If any ticker in the list is Indian (NSE/BSE), mention once in the closing summary that `forensic-compounder` is available for a deeper accounting-quality/governance red-flag pass before committing real capital to any of the Buy-rated Indian names. Don't run it yourself, don't belabor it — one line is enough.

### 6. Offer to log a decision — once, never automatically

If Soumyanil responds to the results by confirming an actual buy/sell action (not just "looks good, thanks" — an actual "I'll buy X" or "yeah let's skip Y"), offer once to log it in `decisions/log.md` using the exact existing format:

```
[YYYY-MM-DD] DECISION: ... | REASONING: ... | CONTEXT: ...
```

using today's date, the action as the decision, the specific metrics that drove it as the reasoning, and a one-line pointer to the workbook path as context. If he doesn't confirm an action, or doesn't respond to the offer, drop it silently — don't ask twice, and don't log a screen that didn't lead anywhere.

### 7. Summarize for the user

Close with a short, bulleted, casual summary per `.claude/rules/communication-style.md` — the Buy/Sell/Wait counts, the workbook's file path, and the forensic-compounder note if it applies. The full table lives in the Excel file; don't repeat it in chat.
