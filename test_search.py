from tools.web_search import (
    search_web,
    format_search_results
)

from ai.model import answer_with_search


question = "قیمت بیت کوین امروز چقدر است؟"

print("در حال جستجو...")

results = search_web(question)

print("Search OK")

formatted = format_search_results(
    results["results"]
)

print("\n--- SEARCH RESULTS ---\n")
print(formatted)

print("\nدر حال ارسال نتایج به AI...")

answer = answer_with_search(
    question,
    formatted
)

print("\n--- ARTIN AI ---\n")
print(answer)