# Firecrawl MCP Cheat Sheet

Two Firecrawl connections exist in this workspace: `claude.ai Firecrawl` and `firecrawl` (added via `claude mcp add --transport http firecrawl https://mcp.firecrawl.dev/v2/mcp-oauth`, authenticated via `claude mcp login firecrawl`). Both expose the same tool set, surfaced under the `mcp__claude_ai_Firecrawl__*` namespace. Tools are deferred — load with `ToolSearch` (`query: "firecrawl"`) before first use in a session.

## Quick picker

| Need | Tool |
|---|---|
| General web search | `firecrawl_search` |
| Scrape/read one known URL | `firecrawl_scrape` (url mode) |
| Pull structured data (companies, filings, prices, jobs...) | `firecrawl_find_tools` → `firecrawl_scrape` (alexandria mode) |
| Coding question (library/error/API) | `firecrawl_developer_search` |
| US legal/regulatory question | `firecrawl_gov_search` |
| Academic/clinical literature | `firecrawl_research_search_papers` + related research tools |
| Rate a search result's usefulness | `firecrawl_search_feedback` |

---

## `firecrawl_search`
General web search with specialized categories and optional Alexandria (structured data provider) matches.

- `query` (required), `objective` (required — one sentence on the underlying goal, reused across related calls)
- `categories`: `research` | `pdf` | `developer` | `gov` (gov can't combine with others)
- `sources`: `web`, `images`, `news`, `alexandria`, `exchange` — authenticated sessions (ours) always add `alexandria`; use `sources: ["alexandria"]` alone for provider discovery with no web results
- `includeDomains` / `excludeDomains` (mutually exclusive), `limit` (max 100)
- Operators in `query`: quoted phrases, `-term`, `site:host`, `inurl:term`, `intitle:term`, `related:host`
- `toolDetail`: `compact` (default) | `summary` | `full` — detail level for matched Alexandria providers

**Example:** `query: "saree wholesale market Surat", objective: "find vendor sourcing options for Ma Lakhsmi Stores", categories: ["web"]`

## `firecrawl_scrape`
Scrape one URL, or execute a selected Alexandria capability. Mutually exclusive modes.

**URL mode:**
- `url` (required), `objective` (required)
- `formats`: `markdown` (default), `html`, `rawHtml`, `screenshot`, `links`, `images`, `summary`, `changeTracking`, `branding`, `json`, `query`, `audio`
- `jsonOptions: {prompt, schema}` — extract structured JSON matching a schema
- `queryOptions: {prompt, mode: "directQuote"|"freeform"}` — ask a targeted question about the page
- `onlyMainContent`, `maxAge` (set `0` to force a live fetch instead of cached), `waitFor`, `location: {country, languages}`
- `domainTools: true` — also return domain-matched Alexandria tools for that page

**Alexandria mode:**
- `alexandria: {provider, capability, options}` (or an array of up to 10) — mutually exclusive with `url`
- Get `provider`/`capability` values from `firecrawl_search` or `firecrawl_find_tools` first
- Billed per capability's listed price

**Example (URL):** `url: "https://competitor-saree-site.com", formats: ["markdown", "screenshot"], objective: "check competitor pricing and layout"`

## `firecrawl_find_tools`
Browse/discover Alexandria structured-data providers (companies, people, jobs, finance/filings, public records, real estate, retail/prices, dev registries, news, research, etc.) without executing them. Free.

- No args → browse categories
- `query` — semantic discovery of providers for a need
- `urls` — find providers matching a specific website
- `providers` / `capabilities` / `categories` / `groups` — narrow a listing
- `expand`: `["options", "response"]` for input/output shape without examples; omit for full contracts
- Use when `firecrawl_search` didn't return the full contract you need, or before scraping the same structured fields repeatedly

## `firecrawl_developer_search`
Search public repos, GitHub issues/PRs, READMEs, and code docs for programming questions.

- `query` (required) — include the library/error/API involved
- `k` — number of results (default 10)
- `skills: "only"` — restrict to agent-skill files

## `firecrawl_gov_search`
Search US federal/state/local statutes, regulations, case law, agency publications.

- `query` (required)
- Filters: `jurisdiction` (`us`, `us-ca`, etc.), `court`, `courtType`, `cites` (citation string or id), `domain`, `k`
- Verify issuer/jurisdiction/effective status before citing — results can include historical or superseded text
- Not useful outside the US; irrelevant to Ma Lakhsmi Stores (India) beyond edge cases like US import/export rules

## Research paper tools (biomedical + arXiv)
- **`firecrawl_research_search_papers`** — natural-language search over abstracts; filters: `authors`, `categories`, `from`/`to` dates, `k` (default 40)
- **`firecrawl_research_inspect_paper`** — metadata for one paper by `paperId` (e.g. `arxiv:1706.03762`, `pmid:...`, `doi:...`)
- **`firecrawl_research_read_paper`** — full-text passages relevant to a `question`, by `paperId`; `k` passages (default 4)
- **`firecrawl_research_related_papers`** — citation-graph expansion from 1–10 `seed_ids`; `mode`: `similar` (default) | `citers` | `references`

## `firecrawl_search_feedback`
Rate a prior `firecrawl_search` result by its `searchId` (UUID returned in that search's response).

- `rating`: `good` | `partial` | `bad`
- `good` needs a `valuableSources` entry; `partial` needs a valuable source or `missingContent`; `bad` needs `missingContent` or `querySuggestions`
- First eligible feedback on a search can refund 1 credit (subject to daily cap)

---

## Notes for this workspace
- **Billing:** web/developer/research search and `firecrawl_scrape` are billed (Alexandria execution at the capability's listed price); government search and Alexandria discovery (`firecrawl_find_tools`, or `firecrawl_search` with `sources: ["alexandria"]` alone) are free.
- **Likely uses here:** competitor saree-site scraping (`firecrawl_scrape`), vendor/market research for Surat/Burrabazar sourcing (`firecrawl_search`), general market/trend research feeding the `research` and `competitor-analysis` skills.
- See `references/skills-backlog.md` item 16 ("Web crawler/scraper") — this cheat sheet is the reference for building that skill.
