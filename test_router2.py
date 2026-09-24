from router import generate_answer


question = input("سؤال: ")

print("\nدر حال پردازش...\n")

answer = generate_answer(question)

print("\n--- ARTIN AI ---\n")
print(answer)