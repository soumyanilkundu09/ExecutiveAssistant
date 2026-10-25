---
name: repurpose-youtube-video
description: Use this skill whenever Soumyanil wants a YouTube video turned into social posts — "repurpose this video", "turn this into posts", "make me a LinkedIn/Instagram/X post from this", a pasted YouTube URL plus any mention of LinkedIn, Instagram, X/Twitter, or "social posts". Also reach for this when he drops a YouTube link with no further instruction but it's clearly content he wants distributed (his own video, a competitor's, a trend he wants to react to). Produces three platform-native drafts (LinkedIn, Instagram, X), each with its own AI-generated visual via Blotato, and only publishes them to Blotato after Soumyanil explicitly approves every draft. Do not use this for writing a single caption/post from a topic with no source video — that's plain copywriting, not repurposing.
---

# Repurpose YouTube Video

Turns one YouTube video into three platform-native posts (LinkedIn, Instagram, X), each with its own AI-generated visual, using [Blotato](https://www.blotato.com) for both visual generation and publishing. Nothing goes live until Soumyanil has seen every draft and said go.

This skill calls Blotato's REST API directly (base `https://backend.blotato.com/v2`, header `blotato-api-key: <key>`). The key lives in `.env` as `BLOTATO_API_KEY` — read it from there via Bash, never ask Soumyanil to paste it into chat, never echo it back, never commit it.

## Process

### 0. Parse the input
Pull the YouTube URL out of the message, plus any extra instruction (a specific angle, "focus on the part about X," a platform to skip, etc.).

### 1. Get the video's content
Shell out to `yt-dlp` to pull title, description, and captions:
```
yt-dlp --dump-json --skip-download <url>
yt-dlp --write-auto-sub --skip-download --sub-lang en <url>
```
If `yt-dlp` isn't installed, the video is private/age-restricted, or there are no captions available: stop and tell Soumyanil exactly what failed, then ask him to paste the transcript or key talking points instead. Don't guess at content from the title alone.

### 2. Determine the persona
Infer from the video's topic whether this is **personal brand** (trading/investing/IT career commentary) or **Ma Lakshmi Stores** (saree business) content — pattern-match against `context/me.md` and `context/work.md`. State your read in one line and let Soumyanil correct it before writing copy; getting this wrong flips the tone, hashtags, and CTA for all three posts.

### 3. Draft the three captions
Write each platform's post from the source material directly — not as truncations of each other:
- **LinkedIn** — longer-form, professional framing, a clear takeaway or lesson, ≤3,000 characters.
- **Instagram** — hook-first caption, conversational, built for the scroll, ≤2,200 characters.
- **X** — punchy, single idea, ≤280 characters.

Follow `.claude/rules/communication-style.md` for the external/public-facing tone — professional and platform-optimized, not the casual internal register used when talking to Soumyanil directly.

### 4. Plan and generate the visuals
Before spending any credits, confirm the Blotato side is ready:
```
GET /v2/users/me/accounts
```
If LinkedIn, Instagram, or X isn't connected, say so plainly and skip generating/publishing for that platform rather than guessing — Soumyanil connects accounts in Blotato's own UI, not through this skill.

For each connected platform, find a template:
```
GET /v2/videos/templates?fields=id,name,description,inputs
```
Pick an appropriate static-image template (e.g. a quote-card style) and aspect ratio per platform convention — Instagram typically 4:5 or 1:1, LinkedIn/X typically 1:1 or 16:9. Tell Soumyanil which template/aspect ratio you're about to generate for each platform and confirm before proceeding, since generation consumes paid credits. Then:
```
POST /v2/videos/from-templates   { templateId, inputs, render: true }
GET  /v2/videos/creations/{id}   (poll every 15s+ until status is "done")
```
Read the resulting image URL from `item.imageUrls`.

### 5. Save the draft
Create a dated folder and write the transcript, the three captions, and the visual URLs into it — create the folder without asking, mirroring how `research/` is organized:
- Ma Lakshmi Stores content → `projects/ma-lakshmi-stores/content/<YYYY-MM-DD>_<slug>/`
- Personal-brand content → `content/<YYYY-MM-DD>_<slug>/` (repo root; create this top-level folder on first use)

### 6. Present for review
Show all three platform drafts in the chat, clearly labeled, caption plus visual. This is the checkpoint — do not call the publish endpoint yet.

### 7. Publish only on explicit approval
Once Soumyanil has approved (edits allowed first — redraft and re-show if he asks for changes), for each approved platform:
```
POST /v2/posts
{
  "post": {
    "accountId": "<from step 4's accounts list>",
    "content": { "platform": "<twitter|linkedin|instagram>", "text": "<approved caption>", "mediaUrls": ["<visual url>"] },
    "target": { "targetType": "<twitter|linkedin|instagram>" }
  }
}
```
Omit `scheduledTime`/`useNextFreeSlot` entirely — this publishes immediately, which is exactly what the approval step is for. Then poll:
```
GET /v2/posts/:postSubmissionId
```
until `published` or `failed`, and report each platform's outcome plainly — don't claim success before the status confirms it.

### 8. Close out
Append the publish outcome (platform, status, link if Blotato returns one) to the draft folder's notes. Offer once — never automatically — to log the run in `decisions/log.md` if anything non-obvious happened (a platform skipped for no connected account, a draft that needed a persona correction, etc.). If Soumyanil declines or doesn't respond, drop it.
