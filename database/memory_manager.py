from database.db import (
    save_memory,
    get_memories,
    update_memory,
    delete_memory
)

from database.memory_ai import (
    find_similar_memory,
    update_memory_with_ai,
    find_memory_to_delete
)

def delete_memory_by_text(
    user_id,
    text
):

    memories = get_memories(
        user_id
    )

    if not memories:

        return False

    old_memory_texts = [
        memory
        for memory_id, memory in memories
    ]

    index = find_memory_to_delete(
        text,
        old_memory_texts
    )

    if index is None:

        return False

    if index < 0 or index >= len(memories):

        return False

    memory_id = memories[index][0]

    memory = memories[index][1]

    print(
        "Memory selected for deletion:",
        memory
    )

    delete_memory(
        memory_id
    )

    print(
        "Memory deleted:",
        memory
    )

    return True

def remove_memory(memory_id):

    delete_memory(
        memory_id
    )

    print(
        "Memory deleted."
    )

def add_memory(user_id, memory):

    if not memory:
        return

    memories = get_memories(user_id)

    old_memory_texts = [
        old_memory
        for memory_id, old_memory in memories
    ]

    print("Checking for similar memories...")

    similar_index = find_similar_memory(
        memory,
        old_memory_texts
    )

    print(
        "Similar memory index:",
        similar_index
    )

    if similar_index is not None:

        old_memory_id = memories[similar_index][0]
        old_memory = memories[similar_index][1]

        print(
            "Similar memory detected:",
            old_memory
        )

        print(
            "Memory ID:",
            old_memory_id
        )

        print("Checking if memory should be updated...")

        updated_memory = update_memory_with_ai(
            old_memory,
            memory
        )

        print(
            "Updated memory result:",
            updated_memory
        )

        if updated_memory:

            if updated_memory.strip() == old_memory.strip():

                print(
                    "No update needed."
                )

            else:

                update_memory(
                    old_memory_id,
                    updated_memory
                )

                print(
                    "Memory updated."
                )

        return

    save_memory(
        user_id,
        memory
    )

    print("New memory saved.")


def get_user_memories(user_id):

    memories = get_memories(user_id)

    return [
        memory
        for memory_id, memory in memories
    ]