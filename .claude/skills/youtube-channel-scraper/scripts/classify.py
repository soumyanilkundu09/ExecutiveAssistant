"""Tag videos against a config's keyword list plus view/like/date/type filters.

Per video this records:
  matched_keywords      keywords found in title, description or (deep-scan) transcript
  matched_in_title      subset found in the title
  passes_filters        min_views / min_likes / date range / Shorts exclusion
  is_match              matched_keywords non-empty AND passes_filters

Safe to call twice: after a --deep-scan the transcript hits (matched_in_transcript,
set by transcripts.py) are folded in on the second call.
"""
import re


def compile_keywords(keywords):
    """Word-boundary, case-insensitive regex per keyword; multi-word keywords tolerate extra whitespace."""
    compiled = {}
    for kw in keywords:
        pattern = r"\b" + r"\s+".join(re.escape(w) for w in kw.split()) + r"\b"
        compiled[kw] = re.compile(pattern, re.IGNORECASE)
    return compiled


def passes_filters(video, config):
    if video.get("video_type") == "short" and not config.get("include_shorts", False):
        return False
    if config.get("min_views", 0) and (video.get("view_count") or 0) < config["min_views"]:
        return False
    if config.get("min_likes", 0) and (video.get("like_count") or 0) < config["min_likes"]:
        return False
    date_from, date_to = config.get("date_from"), config.get("date_to")
    if (date_from or date_to) and video.get("published_at"):
        pub_date = video["published_at"][:10]
        if date_from and pub_date < date_from:
            return False
        if date_to and pub_date > date_to:
            return False
    return True


def classify_video(video, compiled, config):
    title = video.get("title") or ""
    description = video.get("description") or ""
    from_transcript = set(video.get("matched_in_transcript", []))

    matched, in_title = [], []
    for name, pattern in compiled.items():
        t = bool(pattern.search(title))
        if t:
            in_title.append(name)
        if t or pattern.search(description) or name in from_transcript:
            matched.append(name)

    video["matched_keywords"] = matched
    video["matched_in_title"] = in_title
    video["passes_filters"] = passes_filters(video, config)
    video["is_match"] = bool(matched) and video["passes_filters"]
    return video


def classify_videos(videos, config):
    compiled = compile_keywords(config["keywords"])
    return [classify_video(v, compiled, config) for v in videos]
