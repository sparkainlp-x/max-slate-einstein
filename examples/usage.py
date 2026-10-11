"""Demonstrate bounded routes without using a network service."""

from max_slate import answer_question


if __name__ == "__main__":
    for question in (
        "Explain time dilation simply.",
        "What is quantum computing?",
        "Did Einstein say this quotation?",
    ):
        answer = answer_question(question)
        print(f"{answer.route.mode.value}: {answer.text}")
