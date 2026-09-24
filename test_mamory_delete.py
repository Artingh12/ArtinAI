from database.db import (
    save_memory,
    get_memories
)

from database.memory_manager import (
    delete_memory_by_text
)


USER_ID = 999999


print("\n==============================")
print("MEMORY DELETE TEST")
print("==============================\n")


# اضافه کردن Memory آزمایشی
save_memory(
    USER_ID,
    "کاربر در حال یادگیری پایتون است."
)


print("Before delete:")

memories = get_memories(
    USER_ID
)

print(memories)


# درخواست طبیعی کاربر
text = "دیگه نمی‌خوام پایتون یاد بگیرم"


print("\nUser request:")
print(text)


# حذف Memory با استفاده از مفهوم جمله
result = delete_memory_by_text(
    USER_ID,
    text
)


print("\nDelete result:")
print(result)


print("\nAfter delete:")

memories = get_memories(
    USER_ID
)

print(memories)


print("\n==============================")
print("TEST FINISHED")
print("==============================\n")