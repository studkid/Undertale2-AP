from typing import Any

tracker_pages = {
    "Ruins": 0,
    "Archives": 1,
}


def map_page_index(data: Any):
    return tracker_pages[data] if (data in tracker_pages) else 0