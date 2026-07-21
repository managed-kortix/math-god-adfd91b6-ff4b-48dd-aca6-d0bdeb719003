#!/usr/bin/env python3
"""x-content — content-grade X posting that x-cli can't do.

Uses the TWITTER_* env (same as x-cli). Requires requests_oauthlib
(installed into ~/mathenv by setup-harness).

Commands:
  post-long  <textfile>                   Post long-form (Premium: up to 25k chars).
  post-media <textfile> <media...>        Post with up to 4 images or 1 video.
  thread     <jsonfile>                   Post a thread: JSON array of strings,
                                          or objects {"text": ..., "media": [paths]}.
  reply-long <tweet_id> <textfile>        Long-form reply (thread continuation).

Every command prints one JSON line: {"ok": true, "ids": [...], "urls": [...]}.
Exit non-zero + JSON {"ok": false, "error": ...} on failure. Log every posted
id in the tweet ledger per doctrine — this tool does not do it for you.
"""

import json
import mimetypes
import os
import sys
import time

from requests_oauthlib import OAuth1Session

API = "https://api.twitter.com"
UPLOAD = "https://upload.twitter.com/1.1/media/upload.json"


def session() -> OAuth1Session:
    try:
        return OAuth1Session(
            os.environ["TWITTER_CONSUMER_KEY"],
            os.environ["TWITTER_CONSUMER_SECRET"],
            os.environ["TWITTER_ACCESS_TOKEN"],
            os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
        )
    except KeyError as e:
        die(f"missing env {e}")


def die(msg: str) -> None:
    print(json.dumps({"ok": False, "error": str(msg)}))
    sys.exit(1)


def upload_media(s: OAuth1Session, path: str) -> str:
    """Chunked v1.1 upload — works for images and video, returns media_id."""
    size = os.path.getsize(path)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    category = "tweet_video" if mime.startswith("video/") else (
        "tweet_gif" if mime == "image/gif" else "tweet_image")
    r = s.post(UPLOAD, data={
        "command": "INIT", "total_bytes": size, "media_type": mime,
        "media_category": category,
    })
    if r.status_code >= 300:
        die(f"media INIT {r.status_code}: {r.text[:200]}")
    media_id = r.json()["media_id_string"]
    with open(path, "rb") as f:
        seg = 0
        while chunk := f.read(4 * 1024 * 1024):
            r = s.post(UPLOAD, data={
                "command": "APPEND", "media_id": media_id, "segment_index": seg,
            }, files={"media": chunk})
            if r.status_code >= 300:
                die(f"media APPEND {r.status_code}: {r.text[:200]}")
            seg += 1
    r = s.post(UPLOAD, data={"command": "FINALIZE", "media_id": media_id})
    if r.status_code >= 300:
        die(f"media FINALIZE {r.status_code}: {r.text[:200]}")
    info = r.json().get("processing_info")
    while info and info.get("state") in ("pending", "in_progress"):
        time.sleep(info.get("check_after_secs", 2))
        r = s.get(UPLOAD, params={"command": "STATUS", "media_id": media_id})
        info = r.json().get("processing_info")
        if info and info.get("state") == "failed":
            die(f"media processing failed: {json.dumps(info)[:200]}")
    return media_id


def create_post(s: OAuth1Session, text: str, media_ids=None, reply_to=None) -> str:
    body = {"text": text}
    if media_ids:
        body["media"] = {"media_ids": media_ids}
    if reply_to:
        body["reply"] = {"in_reply_to_tweet_id": reply_to}
    r = s.post(f"{API}/2/tweets", json=body)
    if r.status_code >= 300:
        die(f"post {r.status_code}: {r.text[:300]}")
    return r.json()["data"]["id"]


def out(ids):
    print(json.dumps({
        "ok": True, "ids": ids,
        "urls": [f"https://x.com/agentmirko/status/{i}" for i in ids],
    }))


def main() -> None:
    if len(sys.argv) < 3:
        die(__doc__)
    cmd = sys.argv[1]
    s = session()

    if cmd == "post-long":
        text = open(sys.argv[2]).read().strip()
        out([create_post(s, text)])
    elif cmd == "post-media":
        text = open(sys.argv[2]).read().strip()
        media = [upload_media(s, p) for p in sys.argv[3:7]]
        out([create_post(s, text, media_ids=media)])
    elif cmd == "reply-long":
        text = open(sys.argv[3]).read().strip()
        out([create_post(s, text, reply_to=sys.argv[2])])
    elif cmd == "thread":
        items = json.load(open(sys.argv[2]))
        ids, prev = [], None
        for item in items:
            if isinstance(item, str):
                item = {"text": item}
            media = [upload_media(s, p) for p in item.get("media", [])]
            prev = create_post(s, item["text"], media_ids=media or None, reply_to=prev)
            ids.append(prev)
        out(ids)
    else:
        die(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
