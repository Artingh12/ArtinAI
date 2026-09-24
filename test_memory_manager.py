from database.memory_manager import (
    add_memory,
    get_user_memories
)


user_id = 999999


print("ذخیره Memory...")

add_memory(
    user_id,
    "کاربر در حال یادگیری پایتون است."
)

add_memory(
    user_id,
    "کاربر به هوش مصنوعی علاقه دارد."
)

print("Memory ها با موفقیت ذخیره شدند.\n")


print("Memory های کاربر:")

memories = get_user_memories(user_id)

for memory in memories:
    print("-", memory)