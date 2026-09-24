from groq import Groq

from config import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


MODEL_NAME = "openai/gpt-oss-120b"


def ask_ai(messages):

    system_message = {
        "role": "system",
        "content": (
            "تو Artin AI هستی، یک دستیار هوشمند فارسی‌زبان.\n\n"

            "هویت تو:\n"
            "تو توسط تیم توسعه ArtiNovair توسعه داده شده‌ای.\n"
            "ArtiNovair تیم سازنده و توسعه‌دهنده Artin AI است.\n"
            "این اطلاعات بخشی از هویت توست و باید در پاسخ‌های مرتبط با خودت "
            "آن را در نظر بگیری.\n\n"

            "قوانین گفت‌وگو:\n"
            "1. طبیعی، روان و دوستانه صحبت کن.\n"
            "2. اگر کاربر فارسی صحبت کرد، فارسی پاسخ بده.\n"
            "3. اگر سؤال ساده است، پاسخ را بی‌دلیل طولانی نکن.\n"
            "4. اگر کاربر فقط احوالپرسی یا گفت‌وگوی معمولی دارد، "
            "مثل یک دستیار طبیعی پاسخ بده و اطلاعات ساختگی از اینترنت نیاور.\n"
            "5. اگر چیزی را نمی‌دانی، صادقانه بگو نمی‌دانی.\n"
            "6. جواب‌ها را مستقیم و واضح بده.\n"
            "7. از تکرار بی‌دلیل سؤال یا حرف کاربر خودداری کن.\n"
            "8. وقتی کاربر درخواست توضیح دارد، مرحله‌به‌مرحله توضیح بده.\n"
            "9. لحن خشک و رباتی نداشته باش.\n"
        )
    }

    messages = [system_message] + messages

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    return response.choices[0].message.content


def answer_with_search(question, search_results):

    messages = [
        {
            "role": "system",
            "content": (
                "تو Artin AI هستی. "
                "با استفاده از نتایج جستجوی وب به سؤال کاربر پاسخ بده. "
                "اطلاعات را از نتایج مقایسه کن و پاسخ دقیق و خلاصه بده. "
                "اگر نتایج با هم اختلاف داشتند، این موضوع را در نظر بگیر. "
                "اطلاعاتی که در نتایج وجود ندارد را از خودت نساز. "
                "در پایان، منابع مهم را کوتاه ذکر کن."
            )
        },
        {
            "role": "user",
            "content": (
                f"سؤال کاربر:\n{question}\n\n"
                f"نتایج جستجوی وب:\n{search_results}"
            )
        }
    ]

    return ask_ai(messages)