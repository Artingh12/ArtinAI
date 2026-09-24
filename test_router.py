from tools.web_search import needs_search


questions = [
    "قیمت بیت کوین چنده؟",
    "امروز هوا چطوره؟",
    "آخرین اخبار تکنولوژی چیه؟",
    "پایتون چیست؟",
    "چطور با لیست در پایتون کار کنم؟"
]


for question in questions:

    result = needs_search(question)

    print(
        f"{question} -> {result}"
    )