import json

from ai.model import ask_ai


def clean_json_response(result):

    result = result.strip()

    fence = "`" * 3

    result = result.replace(
        fence + "json",
        ""
    )

    result = result.replace(
        fence,
        ""
    )

    return result.strip()


def extract_memory(text):

    messages = [
        {
            "role": "system",
            "content": (
                "وظیفه تو استخراج اطلاعات ماندگار و مفید درباره کاربر است.\n\n"

                "فقط اطلاعاتی را استخراج کن که ارزش ذخیره شدن "
                "به عنوان حافظه بلندمدت دارند.\n\n"

                "مواردی که باید Memory شوند:\n"
                "- نام کاربر\n"
                "- علایق\n"
                "- مهارت‌ها\n"
                "- اهداف بلندمدت\n"
                "- برنامه‌ها و قصدهای آینده\n"
                "- پروژه‌های کاربر\n"
                "- ترجیحات پایدار\n"
                "- اطلاعاتی که در آینده برای شخصی‌سازی پاسخ‌ها مفید هستند\n\n"

                "اهداف و برنامه‌های آینده را حتماً ذخیره کن.\n\n"

                "اگر اطلاعات ماندگاری وجود ندارد، memory را null قرار بده.\n\n"

                "Memory باید همیشه یک متن کوتاه و ساده باشد.\n"
                "هرگز memory را به صورت object یا list برنگردان.\n\n"

                "فقط JSON معتبر برگردان.\n\n"

                'مثال بدون Memory: {"memory": null}\n'
                'مثال با Memory: {"memory": "کاربر به نجوم علاقه دارد."}\n\n'

                "هیچ متن دیگری خارج از JSON ننویس."
            )
        },
        {
            "role": "user",
            "content": text
        }
    ]

    result = ask_ai(messages)

    print(
        "RAW MEMORY AI:",
        repr(result)
    )

    try:

        result = clean_json_response(result)

        data = json.loads(result)

        memory = data.get("memory")

        if not memory:
            return None

        if isinstance(memory, dict):

            interests = memory.get(
                "interests",
                []
            )

            if interests:

                return (
                    "کاربر به "
                    + "، ".join(
                        str(item)
                        for item in interests
                    )
                    + " علاقه دارد."
                )

            return None

        if isinstance(memory, list):

            return "، ".join(
                str(item)
                for item in memory
            )

        return str(memory).strip()

    except (
        json.JSONDecodeError,
        AttributeError,
        TypeError
    ):

        return None


def find_similar_memory(
    new_memory,
    old_memories
):

    if not old_memories:

        return None

    memories_text = "\n".join(
        f"{index + 1}. {memory}"
        for index, memory in enumerate(old_memories)
    )

    messages = [
        {
            "role": "system",
            "content": (
                "تو مسئول تشخیص ارتباط بین Memoryهای یک کاربر هستی.\n\n"

                "یک Memory جدید و چند Memory قبلی دریافت می‌کنی.\n\n"

                "بررسی کن آیا Memory جدید به یکی از Memoryهای قبلی "
                "مربوط است یا نه.\n\n"

                "این موارد را مرتبط در نظر بگیر:\n"
                "- یک موضوع کلی و جزئیات دقیق‌تر همان موضوع\n"
                "- یک علاقه کلی و علاقه به یکی از موارد زیرمجموعه آن\n"
                "- یک مهارت کلی و توضیح دقیق‌تر همان مهارت\n"
                "- یک هدف کلی و جزئیات بیشتر درباره همان هدف\n"
                "- یک ترجیح کلی و ترجیح دقیق‌تر درباره همان موضوع\n\n"

                "مثال:\n"
                "Memory قبلی: کاربر به BMW علاقه دارد.\n"
                "Memory جدید: کاربر BMW M4 را بیشتر دوست دارد.\n"
                "نتیجه: مرتبط است.\n\n"

                "اگر Memory جدید به یکی از Memoryهای قبلی مرتبط است، "
                "شماره آن Memory را برگردان.\n\n"

                "اگر هیچ Memory مرتبطی وجود ندارد، null برگردان.\n\n"

                "فقط JSON معتبر برگردان.\n\n"'اگر مرتبط است: {"similar_memory_id": 1}\n'
                'اگر مرتبط نیست: {"similar_memory_id": null}\n\n'

                "هیچ متن دیگری خارج از JSON ننویس."
            )
        },
        {
            "role": "user",
            "content": (
                f"Memory جدید:\n{new_memory}\n\n"
                f"Memoryهای قبلی:\n{memories_text}"
            )
        }
    ]

    result = ask_ai(messages)

    print(
        "RAW MEMORY COMPARISON:",
        repr(result)
    )

    try:

        result = clean_json_response(result)

        data = json.loads(result)

        similar_id = data.get(
            "similar_memory_id"
        )

        if similar_id is None:

            return None

        return int(similar_id) - 1

    except (
        json.JSONDecodeError,
        AttributeError,
        ValueError,
        TypeError
    ):

        return None


def update_memory_with_ai(
    old_memory,
    new_memory
):

    messages = [
        {
            "role": "system",
            "content": (
                "تو مسئول به‌روزرسانی Memory کاربر هستی.\n\n"

                "یک Memory قدیمی و یک اطلاعات جدید دریافت می‌کنی.\n\n"

                "اگر اطلاعات جدید جزئیات بیشتری درباره همان موضوع "
                "اضافه می‌کند، Memory قدیمی را با اطلاعات جدید ترکیب کن.\n\n"

                "اگر اطلاعات جدید با Memory قدیمی تناقض دارد، "
                "اطلاعات جدیدتر را در نظر بگیر.\n\n"

                "اگر اطلاعات جدید چیز مفیدی به Memory قبلی اضافه نمی‌کند، "
                "همان Memory قبلی را برگردان.\n\n"

                "Memory نهایی باید کوتاه، واضح و مناسب ذخیره‌سازی "
                "بلندمدت باشد.\n\n"

                "فقط JSON معتبر برگردان.\n\n"

                'فرمت پاسخ: {"memory": "Memory نهایی"}\n\n'

                "هیچ متن دیگری خارج از JSON ننویس."
            )
        },
        {
            "role": "user",
            "content": (
                f"Memory قدیمی:\n{old_memory}\n\n"
                f"اطلاعات جدید:\n{new_memory}"
            )
        }
    ]

    result = ask_ai(messages)

    print(
        "RAW MEMORY UPDATE:",
        repr(result)
    )

    try:

        result = clean_json_response(result)

        data = json.loads(result)

        memory = data.get("memory")

        if not memory:

            return old_memory

        if isinstance(memory, dict):

            return old_memory

        return str(memory).strip()

    except (
        json.JSONDecodeError,
        AttributeError,
        TypeError
    ):

        return old_memory
    
def find_memory_to_delete(
    text,
    memories
):

    if not memories:

        return None

    memories_text = "\n".join(
        f"{index + 1}. {memory}"
        for index, memory in enumerate(memories)
    )

    messages = [
        {
            "role": "system",
            "content": (
                "تو مسئول تشخیص درخواست حذف Memory هستی.\n\n"

                "بررسی کن آیا کاربر می‌خواهد اطلاعاتی از Memory "
                "بلندمدت خودش حذف شود یا نه.\n\n"

                "اگر کاربر درخواست حذف یک Memory را دارد، "
                "شماره Memory مرتبط را برگردان.\n\n"

                "اگر کاربر درخواست حذف Memory ندارد، null برگردان.\n\n"

                "اگر درخواست حذف وجود دارد اما هیچ Memory مرتبطی "
                "وجود ندارد، null برگردان.\n\n"

                "فقط JSON معتبر برگردان.\n\n"

                'مثال: {"memory_id": 2}\n'
                'اگر حذف لازم نیست: {"memory_id": null}\n\n'

                "هیچ متن دیگری خارج از JSON ننویس."
            )
        },
        {
            "role": "user",
            "content": (
                f"پیام کاربر:\n{text}\n\n"
                f"Memoryهای کاربر:\n{memories_text}"
            )
        }
    ]

    result = ask_ai(
        messages
    )

    print(
        "RAW MEMORY DELETE AI:",
        repr(result)
    )

    try:

        result = clean_json_response(
            result
        )

        data = json.loads(
            result
        )

        memory_id = data.get(
            "memory_id"
        )

        if memory_id is None:

            return None

        return int(
            memory_id
        ) - 1

    except (
        json.JSONDecodeError,
        AttributeError,
        ValueError,
        TypeError
    ):

        return None