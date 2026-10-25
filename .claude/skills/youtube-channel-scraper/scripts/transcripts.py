"""Optional --deep-scan: keyword-match video transcripts (auto-captions).

Catches topics only spoken aloud, which title/description matching misses. Uses
youtube-transcript-api (no API key, no Data API quota). Only runs on candidates that
already pass the view/like/date/Shorts filters, and caches each transcript so reruns
are free. Videos without captions are marked transcript_status="unavailable" - that is
normal, not an error.

Sets on each scanned video:
  matched_in_transcript  keyword names found in the transcript
  transcript_snippets    short text excerpts around the first hit of each keyword
  transcript_status      "ok" | "unavailable" | "skipped"
"""
import json
import re
import time
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

SNIPPET_RADIUS = 80


def _fetch_text(video_id, languages):
    """Return transcript text; supports both the 1.x (.fetch) and older (.get_transcript) APIs."""
    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        entries = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        return " ".join(e["text"] for e in entries)
    fetched = YouTubeTranscriptApi().fetch(video_id, languages=languages)
    return " ".join(s.text for s in fetched)


def get_transcript(video_id, languages, cache_dir):
    cache = Path(cache_dir) / "transcripts"
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / f"{video_id}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["text"]
    try:
        text = _fetch_text(video_id, languages)
    except Exception:  # captions disabled / not in requested language / blocked - all just "no transcript"
        text = None
    path.write_text(json.dumps({"text": text}, ensure_ascii=False), encoding="utf-8")
    return text


def deep_scan(videos, compiled_keywords, languages, cache_dir, delay=0.5):
    candidates = [v for v in videos if v.get("passes_filters")]
    print(f"Deep scan: reading transcripts for {len(candidates)} videos (cached ones are instant)...")
    for i, v in enumerate(candidates, 1):
        text = get_transcript(v["video_id"], languages, cache_dir)
        if text is None:
            v["transcript_status"] = "unavailable"
            continue
        v["transcript_status"] = "ok"
        hits, snippets = [], []
        for name, pattern in compiled_keywords.items():
            m = pattern.search(text)
            if m:
                hits.append(name)
                a, b = max(0, m.start() - SNIPPET_RADIUS), min(len(text), m.end() + SNIPPET_RADIUS)
                snippets.append("..." + re.sub(r"\s+", " ", text[a:b]) + "...")
        v["matched_in_transcript"] = hits
        v["transcript_snippets"] = snippets
        if i % 25 == 0:
            print(f"  {i}/{len(candidates)}")
        time.sleep(delay)
    for v in videos:
        v.setdefault("transcript_status", "skipped")
    unavailable = sum(1 for v in candidates if v.get("transcript_status") == "unavailable")
    if unavailable:
        print(f"  {unavailable} videos had no usable captions (title/description matching only for those).")
    return videos
