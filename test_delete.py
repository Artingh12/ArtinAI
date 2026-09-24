from database.db import (
    create_database,
    save_memory,
    get_memories,
    delete_memory
)


create_database()

user_id = 999999

save_memory(
    user_id,
    "کاربر به BMW علاقه دارد."
)

print(
    "Before delete:"
)

print(
    get_memories(user_id)
)

memories = get_memories(
    user_id
)

memory_id = memories[-1][0]

delete_memory(
    memory_id
)

print(
    "After delete:"
)

print(
    get_memories(user_id)
)