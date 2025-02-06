"""Search module."""

import os
import warnings

import requests
from bs4 import BeautifulSoup
from loguru import logger

warnings.filterwarnings("ignore", module="bs4")


def search(query: str, num: int) -> list[str]:
    """Do a request and colleting result."""
    user_agent = os.getenv("USER_AGENT")
    search_link = os.getenv("SEARCH_LINK")
    cookie = os.getenv("COOKIE")
    user_black_list = os.getenv("BLACK_LIST").split(", ")

    black_list = [
        # Yandex black list
        "https://passport.yandex.ru/",
        "https://yandexwebcache.net/",
        "https://yandex.ru/support/",
        "https://cloud.yandex.ru/",
        "https://yandex.ru/",
        "https://www.ya.ru",
    ]

    black_list += user_black_list

    url = f"{search_link}{query}"
    urls = []

    page = requests.get(
        url,
        headers={
            "user-agent": user_agent,
            "cookie": cookie,
        },
        timeout=20,
    )
    soup = BeautifulSoup(page.text, "html.parser")

    for link in soup.find_all("a"):
        url = str(link.get("href"))

        black = False
        if url.startswith("http"):
            for black_url in black_list:
                if black_url in url:
                    black = True
                    break
            if not black:
                urls.append(url)
                logger.debug("URL: {}", url)
            else:
                logger.error("URL: {}", url)

    return urls[:num]


def extract_text(url: str) -> str:
    """Extract text from url."""
    try:
        page = requests.get(url, timeout=40)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        logger.error(e)
        return ""
