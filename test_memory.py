from database.memory_ai import extract_memory


tests = [
    "اسم من آرتین است و دارم پایتون یاد می‌گیرم.",
    "هدفم اینه که در آینده وارد حوزه هوش مصنوعی بشم.",
    "سلام، خوبی؟",
    "امروز هوا خیلی خوبه.",
    "من به یادگیری ماشین علاقه دارم."
]


for text in tests:

    print("\n--------------------")
    print("پیام:")
    print(text)

    memory = extract_memory(text)

    print("Memory:")
    print(memory)