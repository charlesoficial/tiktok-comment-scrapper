from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

import requests


class VideoIdError(ValueError):
    pass


def extract_video_id(value: str, *, resolve_short_url: bool = True) -> str:
    candidate = value.strip()
    if not candidate:
        raise VideoIdError("informe o ID ou a URL do video")

    if re.fullmatch(r"\d{10,25}", candidate):
        return candidate

    parsed = urlparse(candidate)
    query = parse_qs(parsed.query)
    for key in ("aweme_id", "item_id"):
        if query.get(key) and re.fullmatch(r"\d{10,25}", query[key][0]):
            return query[key][0]

    path_match = re.search(r"/video/(\d{10,25})", parsed.path)
    if path_match:
        return path_match.group(1)

    if resolve_short_url and parsed.netloc in {"vm.tiktok.com", "vt.tiktok.com"}:
        return _resolve_short_url(candidate)

    raise VideoIdError("nao encontrei um ID de video valido nessa entrada")


def _resolve_short_url(url: str) -> str:
    try:
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=15,
            headers={"user-agent": "Mozilla/5.0"},
        )
    except requests.RequestException as exc:
        raise VideoIdError(f"nao consegui resolver a URL curta: {exc}") from exc

    return extract_video_id(response.url, resolve_short_url=False)
