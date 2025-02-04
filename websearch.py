"""Search module."""

import os
import warnings

import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", module="bs4")


def search(query: str, num: int) -> list[str]:
    """Do a request and colleting result."""
    user_agent = os.getenv("USER_AGENT")
    search_link = os.getenv("SEARCH_LINK")

    red_list = [
        "https://passport.yandex.ru/",
        "https://yandexwebcache.net/",
        "https://yandex.ru/support/",
        "https://cloud.yandex.ru/",
        "https://www.ya.ru",
    ]

    url = f"{search_link}{query}"
    urls = []

    page = requests.get(
        url,
        headers={
            "User-agent": user_agent,
        },
        timeout=20,
    )
    soup = BeautifulSoup(page.text, "html.parser")

    for link in soup.find_all("a"):
        url = str(link.get("href"))

        red = False
        if "http" in url:
            for red_url in red_list:
                if red_url in url:
                    red = True
                    break
            if not red:
                urls.append(url)

    return urls[:num]


def extract_text(url: str) -> str:
    """Extract text from url."""
    page = requests.get(url, timeout=20)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup.get_text()
