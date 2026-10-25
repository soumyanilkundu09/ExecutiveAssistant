---
name: otb-calculator
description: Use this skill whenever Soumyanil wants an Open-to-Buy (OTB) / inventory budget / margin calculator for Ma Lakhsmi Stores, or wants to know how much cash he can spend on stock — "build the OTB sheet", "make me the OTB Excel", "how much can I buy this month", "how much cash do I take to Surat / Burrabazar", "am I over-stocked on silks/bridal", "should I pause procurement", "review my OTB sheet", or when he hands over a filled-in OTB workbook. Two modes — Build (generate the formula-driven Excel from inputs) and Review (read his filled-in workbook and give a buy/pause procurement brief). Not for stock analysis or trading (use fundamental-stock-analysis / malkan-score), and not for one-off GST questions with no inventory angle.
---

# OTB Calculator — Ma Lakhsmi Stores

Retail stores rarely die from lack of sales; they die from cash stuck in dead stock. This skill builds and reviews an Open-to-Buy workbook that tells Soumyanil exactly how much he may spend per category, per sourcing hub (Surat / Burrabazar / Other), each month — without touching rent, salaries or the cash buffer.

Everything lives as live formulas, so the workbook works on its own after this skill hands it over. **The live copy is a Google Sheet** ("OTB – Ma Lakhsmi Stores", folder "Ma Lakhsmi Stores" in his Drive; ID in `projects/ma-lakshmi-stores/finance/README.md`), reached through the `gws` CLI. The local .xlsx is only the build output. Sales are entered manually each week (no POS/API integration yet — revisit once Marg ERP or Zoho Inventory is live; see Priority #1 in `context/current-priorities.md`).

## Files in this skill

- `scripts/build_otb.py <inputs.json> <out.xlsx>` — deterministic generator. Never hand-improvise the workbook; change the script if the structure needs to change.
- `inputs.example.json` — placeholder defaults (₹10L capital, ₹2.5L setup, ₹1.35L base monthly sales, 60% GM, Bengal festival seasonality, category mix 30/35/25/10, source splits).
- `scripts/recalc_excel.ps1 <xlsx>` — recalculates in desktop Excel via COM (LibreOffice isn't installed on this machine). Must run before reading values.
- `scripts/check_otb.py <xlsx>` — scans for formula errors and dumps the Dashboard as JSON (category signals, sourcing cash, cash position, aging). Set `PYTHONIOENCODING=utf-8` (₹ in headers).

## Workbook model (what the formulas do)

- **OTB at cost** = planned sales at cost + planned closing stock − opening stock − on order. Closing stock target = next month's planned sales at cost × that category's *months of cover*.
- **Margin**: cost = selling price × (1 − target GM). 60% GM ⇒ 2.5× markup.
- **Seasonality**: monthly index (Puja Sep–Oct peak, weddings Nov–Feb, Poila Boishakh Apr, monsoon slump Jun–Aug).
- **Cash guardrail**: OTB is scaled down when opening cash + planned sales − fixed costs − buffer (N months of fixed costs) can't fund it.
- **Dashboard flags** per category: OVER-INDEXED stock mix → PAUSE PROCUREMENT; bought > approved OTB → PAUSE; weeks of cover > max → PAUSE; sell-through < minimum → SLOW; under-stocked → PRIORITISE.
- **Stock Aging** doubles as the purchase register (what counts against OTB): Fresh → Watch → Ageing (markdown) → Dead (clearance / vendor exchange).

Sheets: README · Inputs · Dashboard · Monthly OTB · Sales Log · Stock Aging.

## Mode 1 — Build

1. Ask once for any real numbers he has: working capital, setup costs, rent, salaries, electricity, EMI, expected monthly sales, plan start month, and any change to the category mix / source splits. Whatever he doesn't give stays a placeholder — say so.
2. Copy `inputs.example.json` to the scratchpad, overwrite the given values, and run:
   ```
   python scripts/build_otb.py <inputs.json> projects/ma-lakshmi-stores/finance/OTB_Ma_Lakhsmi_<YYYY-MM>.xlsx
   powershell -NoProfile -File scripts/recalc_excel.ps1 <that xlsx>
   python scripts/check_otb.py <that xlsx>
   ```
   (Script paths are relative to this skill folder; the output path is relative to the repo root — use absolute paths.)
3. `total_errors` must be 0. If not, fix `build_otb.py`, not the output file.
4. Save the inputs JSON next to the workbook (`OTB_inputs_<YYYY-MM>.json`) so the build can be rerun.
5. **Publish to Google Sheets.** Check `projects/ma-lakshmi-stores/finance/README.md` for an existing Sheet ID first.
   - **No Sheet yet:** upload with conversion into the "Ma Lakhsmi Stores" Drive folder:
     ```
     gws drive files create --json '{"name":"OTB – Ma Lakhsmi Stores","mimeType":"application/vnd.google-apps.spreadsheet","parents":["<folderId>"]}' --params '{"fields":"id,webViewLink"}' --upload <xlsx> --upload-content-type application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
     ```
     Record the new ID and link in the finance README.
   - **Sheet already exists:** it holds his live Sales Log / Stock Aging data, so never replace it silently. Changing numbers only? Tell him to edit the yellow Inputs cells in the Sheet itself (no rebuild needed). Rebuilding the structure? Ask first, then upload as a *new* dated Sheet, copy his log rows across, and keep the old one (never trash it).
   - Verify by reading back `'Monthly OTB'!A71:N75` with `gws sheets spreadsheets values get` — the numbers must match the local recalc.
6. Reply with a short table: month-1 approved OTB per category, the Surat / Burrabazar / Other cash split, buffer protected, which inputs are still placeholders, and the Sheet link.

## Mode 2 — Review

Trigger: he says he's updated the sheet, asks "what should I buy", or before a sourcing run.

1. Pull the live Google Sheet down as .xlsx (ID from the finance README). `gws` refuses `--output` paths outside the current directory, so `cd` into the scratchpad first:
   ```
   cd <scratchpad> && gws drive files export --params '{"fileId":"<id>","mimeType":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}' --output otb_live.xlsx
   ```
   Fall back to the latest local `OTB_Ma_Lakhsmi_*.xlsx` only if he says he's been using the Excel file. Never write back to the Sheet during a review.
2. Google already computed the values, so run `check_otb.py` on the export directly (for a local .xlsx, run `recalc_excel.ps1` on a scratchpad copy first). If the copy shows `plan_month_index` 0, the as-of date is outside the 12-month plan — tell him to rebuild with a new start month.
3. Write a procurement brief to `projects/ma-lakshmi-stores/finance/otb-review-<YYYY-MM-DD>.md`:
   - **Verdict table**: category → ACTION, OTB left (₹), stock mix vs target, sell-through, weeks of cover.
   - **Sourcing run**: ₹ still to spend at Surat / Burrabazar / Other; if one is negative, say which category overspent there.
   - **Dead/ageing stock**: ₹ value and what to do (markdown, WhatsApp push, vendor exchange).
   - **Cash**: closing cash, runway, cash-capped or not, sales vs plan this month.
   - **Top 3 actions** for this week, plainly worded.
   - Caveat when relevant: the plan's opening stock assumes last month's plan was hit; if actual stock (Dashboard) is far above plan, the Dashboard flags override the Monthly OTB number.
4. Reply in chat with just the verdict table and top 3 actions (casual tone, short), plus the brief's path.
5. If a review leads to a real decision (e.g. pausing bridal buying for a month, changing the mix), append it to `decisions/log.md`.

## Notes

- All money is ex-GST. GST rate on sarees depends on HSN/price — the Inputs cell is reference only; point him to his CA for compliance.
- All formulas (EDATE, SUMIFS, INDEX/MATCH, conditional formats, cross-sheet dropdowns) convert to Google Sheets cleanly, verified 2026-10-24. Keep new formulas to Excel-2007-era functions so both stay in sync.
- Sharing: currently private to him. When hires join, share via `gws drive permissions create` (editor for the billing exec on Sales Log / Stock Aging) — only after he names the people.
- Future upgrade path: once the POS is chosen, add a CSV-import step (Marg/Zoho sales export → Sales Log) rather than manual entry.
