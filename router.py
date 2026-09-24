from tools.web_search import (
    needs_search,
    search_web,
    format_search_results
)

from ai.model import (
    ask_ai,
    answer_with_search
)


def generate_answer(messages):

    question = messages[-1]["content"]

    if needs_search(question):

        print("Search required...")

        results = search_web(question)

        formatted_results = format_search_results(
            results["results"]
        )

        return answer_with_search(
            question,
            formatted_results
        )

    else:

        print("Search not required...")

        return ask_ai(messages)