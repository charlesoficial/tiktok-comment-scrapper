from __future__ import annotations

import time
from typing import Any, Iterable

import requests

from .models import Comment


class TikTokClientError(RuntimeError):
    pass


class TikTokClient:
    base_url = "https://www.tiktok.com"
    api_url = f"{base_url}/api"
    max_page_size = 50

    def __init__(self, *, timeout: int = 20, retries: int = 2, delay: float = 0.4) -> None:
        self.timeout = timeout
        self.retries = retries
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(
            {
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
                "referer": self.base_url,
                "user-agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
            }
        )

    def iter_comments(
        self,
        video_id: str,
        *,
        limit: int,
        include_replies: bool,
    ) -> Iterable[Comment]:
        cursor = 0
        yielded = 0

        while yielded < limit:
            page_size = min(self.max_page_size, limit - yielded)
            payload = self._get(
                "comment/list",
                {
                    "aid": 1988,
                    "aweme_id": video_id,
                    "count": page_size,
                    "cursor": cursor,
                },
            )

            raw_comments = payload.get("comments") or []
            if not raw_comments:
                break

            for raw_comment in raw_comments:
                comment = Comment.from_api(raw_comment)
                if include_replies and comment.reply_count:
                    comment.replies = list(self.iter_replies(video_id, comment.id))
                yield comment
                yielded += 1
                if yielded >= limit:
                    break

            if not payload.get("has_more"):
                break

            cursor = int(payload.get("cursor") or cursor + page_size)

    def iter_replies(self, video_id: str, comment_id: str) -> Iterable[Comment]:
        cursor = 0

        while True:
            payload = self._get(
                "comment/list/reply",
                {
                    "aid": 1988,
                    "item_id": video_id,
                    "comment_id": comment_id,
                    "count": self.max_page_size,
                    "cursor": cursor,
                },
            )

            raw_replies = payload.get("comments") or []
            if not raw_replies:
                break

            for raw_reply in raw_replies:
                yield Comment.from_api(raw_reply)

            if not payload.get("has_more"):
                break

            cursor = int(payload.get("cursor") or cursor + self.max_page_size)

    def get_video_meta(self, video_id: str) -> tuple[str, str]:
        payload = self._get(
            "comment/list",
            {
                "aid": 1988,
                "aweme_id": video_id,
                "count": 1,
                "cursor": 0,
            },
        )
        raw_comments = payload.get("comments") or []
        if not raw_comments:
            return "", ""

        share_info = raw_comments[0].get("share_info") or {}
        return str(share_info.get("title") or ""), str(share_info.get("url") or "")

    def _get(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        last_error: Exception | None = None

        for attempt in range(self.retries + 1):
            try:
                response = self.session.get(
                    f"{self.api_url}/{endpoint.strip('/')}/",
                    params=params,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                data = response.json()
                if not isinstance(data, dict):
                    raise TikTokClientError("a API retornou um formato inesperado")
                return data
            except (requests.RequestException, ValueError, TikTokClientError) as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(self.delay * (attempt + 1))

        raise TikTokClientError(f"falha ao consultar o TikTok: {last_error}") from last_error
