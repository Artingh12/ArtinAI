import requests

from config import TINYFISH_API_KEY


def search_web(query):

    url = "https://api.search.tinyfish.ai"

    headers = {
        "X-API-Key": TINYFISH_API_KEY
    }

    params = {
        "query": query
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()

def format_search_results(results):

    text = ""

    for result in results:

        title = result.get("title", "")
        url = result.get("url", "")
        snippet = result.get("snippet", "")

        text += (
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Snippet: {snippet}\n\n"
        )

    return text

def needs_search(question):

    keywords = [
        "امروز",
        "الان",
        "قیمت",
        "قیمت امروز",
        "آخرین",
        "جدیدترین",
        "اخبار",
        "خبر",
        "آب و هوا",
        "هوا",
        "دلار",
        "یورو",
        "بیت کوین",
        "بورس",
        "نتیجه",
        "مسابقه",
        "بازی امروز",
        "تاریخ امروز"
    ]

    question_lower = question.lower()

    for keyword in keywords:
        if keyword in question_lower:
            return True

    return False
