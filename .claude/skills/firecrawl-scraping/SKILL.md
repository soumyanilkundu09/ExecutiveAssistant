---
name: firecrawl-scraping
description: Use this skill whenever Soumyanil wants data pulled off a specific website or page — "scrape this site", "crawl this URL", "map out this site's pages", "extract the product list/prices/specs from this page", "get me a screenshot of this page", "pull the markdown/HTML/links off this URL", or any ask that names a particular website and wants its content, structure, or a visual of it. This covers competitor saree-site scraping, vendor/sourcing page pulls, and any other raw-page-data job via the `firecrawl` MCP server. Trigger even if Soumyanil never says "Firecrawl" or "scrape" explicitly, as long as the underlying need is pulling data off one or more specific, named pages rather than researching a topic broadly. This is NOT for open-ended multi-source topic research with no fixed URL — route that to the `research` skill instead. This is NOT for comparing multiple competitors' features and positioning — route that to the `competitor-analysis` skill instead (it may call this skill internally for the raw per-site pulls, but owns the comparison and write-up). And this is NOT a reason to reach for a one-off `WebFetch`/`WebSearch` call when the job actually needs real scraping/crawling/structured-extraction/screenshot capability — use this skill's tools for that instead, since they handle JS-rendered pages, PDFs, and structured JSON extraction that a generic page fetch can't.
---

# Firecrawl Scraping

Soumyanil has the `firecrawl` MCP server connected and authenticated. This skill is what to reach for whenever a request is about pulling something off a specific, named website or page — not researching a topic in the abstract. Think: "what does this competitor's saree site show as their bestseller price," "map every product category page on this vendor's site," "screenshot this landing page so I can see their layout," "extract this page's product specs as structured JSON."

## Before calling anything

Read [references/firecrawl-cheatsheet.md](../../../references/firecrawl-cheatsheet.md) (repo root). It documents the exact Firecrawl tool set available in this workspace — `firecrawl_search`, `firecrawl_scrape` (both URL mode and Alexandria structured-data mode), `firecrawl_find_tools`, `firecrawl_developer_search`, `firecrawl_gov_search`, the research-paper tools, and `firecrawl_search_feedback` — along with their parameters and a quick-picker table. That table is the fastest way to land on the right tool; don't guess at parameters from memory.

The Firecrawl tools are deferred (not loaded by default). Load them with `ToolSearch` — they live under the `mcp__claude_ai_Firecrawl__*` namespace — before the first call in a session.

## Picking the right tool for the job

- **One known URL, want its content** → `firecrawl_scrape` in URL mode. Default to `markdown`; add `screenshot` if Soumyanil wants a visual, or `links` if he wants the outbound links. Use `jsonOptions: {prompt, schema}` when he wants specific structured fields (price, product name, stock status) rather than the whole page.
- **Don't know the page structure yet, need to find it / want fresh (not cached) content** → set `maxAge: 0` to force a live fetch instead of Firecrawl's cache — useful for price checks or anything time-sensitive.
- **Multiple pages on the same site, or "map this site"** → use `firecrawl_find_tools` first if the site matches a known structured-data provider (company data, retail/prices, job listings, etc.) — it's free discovery and can save a lot of manual scraping. If no provider fits, fall back to scraping the pages you need individually, or ask Soumyanil which specific pages matter rather than trying to crawl an entire site blind.
- **A general question that isn't tied to one URL** ("who are the top saree wholesalers in Surat") → that's `research` skill territory, not this one. If it's genuinely ambiguous, ask which Soumyanil actually wants.

## Output

- For a single scrape/extract: report the result inline unless it's long, in which case save to a sensibly-named file under `research/` or the relevant `projects/ma-lakshmi-stores/research/` folder and point to it.
- For screenshots: save the image and tell Soumyanil the file path.
- Always note the source URL and when it was fetched (live vs. cached), since page content changes — especially pricing and stock pages.

## Logging

If a scrape surfaces something that changes a decision (e.g. a competitor's pricing undercuts the planned positioning), flag it and offer to log it in `decisions/log.md` using the standard `[YYYY-MM-DD] DECISION: ... | REASONING: ... | CONTEXT: ...` format.
