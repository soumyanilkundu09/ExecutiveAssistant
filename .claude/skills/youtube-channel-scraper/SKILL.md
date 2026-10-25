---
name: youtube-channel-scraper
description: Use this skill whenever Soumyanil wants to scan a whole YouTube channel for videos matching a topic and get a ranked shortlist — "scrape @Malkansview01 for videos on Glenmark", "which of this channel's videos talk about cup and handle", "scan this saree channel for bridal trends", "find all videos on X from @channel", "rank a channel's videos by relevance", or a channel handle/URL plus keywords or view/date thresholds. Works for trading channels (Malkan, Indian/US stock YouTubers) and saree-business research (competitor, wholesaler or trend channels). Outputs a relevance-ranked Google Sheet. Offers an optional transcript deep-scan for topics only mentioned in speech. Not for turning one video into social posts (use repurpose-youtube-video), not for scraping non-YouTube sites (use firecrawl-scraping), and not for broad multi-source topic research (use research).
---

# YouTube Channel Scraper

Turns "which videos on this channel are worth my time?" into a ranked Google Sheet. Deterministic Python does the fetching, matching and scoring (so results are reproducible and cost no AI tokens); your job is to gather the criteria, run it, and interpret the result.

## Prerequisites

- `YOUTUBE_API_KEY` in the repo-root `.env` (YouTube Data API v3 key; see `.env.example`). If missing, tell Soumyanil to add it - never read `.env` yourself or ask him to paste the key into chat. He does **not** need a client_secret: the API is read-only public data, and Sheets upload goes through the already-authenticated `gws` CLI.
- Python packages: `google-api-python-client python-dotenv openpyxl youtube-transcript-api` (already installed on this machine).

## Inputs to settle before running

1. **Channel** - `@handle`, a `youtube.com/@handle` or `/channel/UC...` URL, or a `UC...` id. Legacy `/c/` URLs aren't supported; ask for the @handle.
2. **Keywords** - the topics/tickers/phrases to hunt for. Ask if he gave none. Short keywords like "REC" are word-boundary matched, so they won't hit inside other words.
3. **Optional filters** - `min_views`, `min_likes`, `date_from`/`date_to`, `top_n` (default 30).
4. **Shorts** - excluded by default (they're noise for research; `include_shorts` for saree reels/trend scans where Shorts *are* the content). Shorts are videos <= `shorts_max_seconds` (default 60; YouTube now allows up to 3 min, raise it if needed).
5. **Deep scan?** - only if the topic is likely spoken, not titled (a specific stock named mid-video). Say it's slower and uses free auto-captions; videos without captions silently fall back to title/description matching.

Start from `criteria.example.json` (trading) or `criteria.saree-trends.example.json` (saree), copy it into the scratchpad, fill it in, and don't edit the examples.

## Run

```
python .claude/skills/youtube-channel-scraper/scripts/run.py --config <criteria.json> [--channel @x] [--deep-scan] [--include-shorts] [--top-n N] --upload [--folder-id <id>]
```

- Without `--upload` the .xlsx stays in `.tmp/yt/<slug>/` (gitignored, disposable). With it, the file is converted to a native Google Sheet in his Drive via `gws` and the link is printed. Default to `--upload` - deliverables live in the cloud. For saree-research output, use the "Ma Lakhsmi Stores" Drive folder (find its id via `gws drive files list`; see `projects/ma-lakshmi-stores/finance/README.md`).
- If upload fails, the local file is kept; report that rather than retrying blindly.
- Quota is trivial (a 2,000-video channel is < 100 of 10,000 daily units), so rerunning is safe.

## How ranking works (explain briefly if he asks)

`relevance = keyword_weight x keyword_component + engagement_weight x engagement_component`, 0-100.
- Keyword: 2 pts per keyword in the title, 1 pt if only in description/transcript, scaled so ~3 strong keyword hits saturate at 100 (`keyword_saturation`). Long keyword lists therefore don't punish good matches.
- Engagement: log-scaled views (or likes) across all the channel's videos, so one viral outlier doesn't flatten everything else.

## Report back (casual, short)

- Match count, how many Shorts were excluded, and the Sheet link.
- The top 5 videos as a table: score, title, views, date, matched keywords.
- Flag caveats that apply: 0 matches (suggest loosening filters or `--deep-scan`), many `transcript_status: unavailable`, or a keyword so generic it matched everything.

## Edge cases

- **Channel not found** -> the script exits with a clear message; surface it, usually a typo or a custom-URL channel.
- **No matches** -> empty Matched sheet, not an error. Say so and suggest next steps.
- **Topic only spoken** -> title/description search misses it; offer `--deep-scan` rather than guessing.
- **Member-only / private videos** don't appear in the uploads list; mention if a channel looks much smaller than expected.

## Follow-ups

- Emailing the result: send the Sheet link with `gws gmail` as a draft for his approval first - there is no SMTP/app-password path any more.
- To actually analyse a shortlisted video, hand its URL to the `repurpose-youtube-video` skill or `research`.
- If a trading finding matters (e.g. a stock call worth tracking), log it via `decisions/log.md` only once he decides to act on it.
