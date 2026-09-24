from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import TELEGRAM_TOKEN, BOT_NAME

from router import generate_answer

from database.db import (
    create_database,
    save_message,
    get_messages
)

from database.memory_ai import extract_memory

from database.memory_manager import (
    add_memory,
    get_user_memories,
    delete_memory_by_text
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    await update.message.reply_text(
        f"سلام {user.first_name} 👋\n\n"
        f"من {BOT_NAME} هستم 🤖\n"
        "دستیار هوشمند شخصی تو.\n\n"
        "پیامت رو بفرست تا با هم شروع کنیم."
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    print("\n==============================")
    print("NEW MESSAGE:", text)

    save_message(
        user_id,
        "user",
        text
    )

    print("User message saved.")

    # ==============================
    # بررسی درخواست حذف Memory
    # ==============================

    print("Checking memory delete request...")

    deleted = delete_memory_by_text(
        user_id,
        text
    )

    print(
        "Memory delete result:",
        deleted
    )

    if deleted:

        print("Memory deletion handled.")

        await update.message.reply_text(
            "باشه، اون اطلاعات رو از حافظه‌ام حذف کردم."
        )

        print("==============================\n")

        return

    # ==============================
    # استخراج Memory جدید
    # ==============================

    print("Extracting memory...")

    memory = extract_memory(
        text
    )

    print(
        "Extracted memory:",
        memory
    )

    if memory:

        print("Saving memory...")

        add_memory(
            user_id,
            memory
        )

        print("Memory saved.")

    else:

        print("No memory to save.")

    # ==============================
    # دریافت Memoryهای کاربر
    # ==============================

    print("Getting user memories...")

    memories = get_user_memories(
        user_id
    )

    print(
        "User memories:",
        memories
    )

    # ==============================
    # دریافت تاریخچه گفتگو
    # ==============================

    print("Getting conversation history...")

    history = get_messages(
        user_id
    )

    # فقط ۲۰ پیام آخر برای AI ارسال می‌شود
    history = history[-20:]

    print(
        "History messages:",
        len(history)
    )

    # ==============================
    # ساخت Memory برای AI
    # ==============================

    memory_text = ""

    if memories:

        memory_text = (
            "اطلاعاتی که از قبل درباره کاربر ذخیره شده:\n"
            + "\n".join(
                f"- {memory}"
                for memory in memories
            )
        )

    # ==============================
    # ساخت Messages
    # ==============================

    messages = []

    if memory_text:

        messages.append({
            "role": "system",
            "content": memory_text
        })

    for role, content in history:

        messages.append({
            "role": role,
            "content": content
        })

    # ==============================
    # تولید پاسخ AI
    # ==============================

    print("Generating answer...")

    answer = generate_answer(
        messages
    )

    print(
        "AI ANSWER:",
        repr(answer)
    )

    # ==============================
    # ذخیره پاسخ AI
    # ==============================

    save_message(
        user_id,
        "assistant",
        answer
    )

    print("AI answer saved.")

    # ==============================
    # ارسال پاسخ
    # ==============================

    await update.message.reply_text(
        answer
    )

    print("Reply sent.")
    print("==============================\n")


def main():
    create_database()

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message
        )
    )

    print(
        f"{BOT_NAME} is running..."
    )

    app.run_polling()


if __name__ == "__main__":

    main()