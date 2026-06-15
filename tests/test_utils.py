import pytest

from tiktok_exporter.utils import VideoIdError, extract_video_id


def test_extract_video_id_from_plain_id():
    assert extract_video_id("7418294751977327878") == "7418294751977327878"


def test_extract_video_id_from_video_url():
    url = "https://www.tiktok.com/@user/video/7418294751977327878"
    assert extract_video_id(url) == "7418294751977327878"


def test_extract_video_id_from_query_string():
    url = "https://www.tiktok.com/share/video?item_id=7418294751977327878"
    assert extract_video_id(url) == "7418294751977327878"


def test_extract_video_id_rejects_invalid_value():
    with pytest.raises(VideoIdError):
        extract_video_id("not-a-video")
