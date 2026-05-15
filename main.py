import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from pdf_ingestion import ingest_pdf

from memory import (
    save_note,
    get_notes,
)

from chroma_memory import (
    save_memory,
    search_memory,
)

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

# -----------------------------------
# MEMORY STORAGE
# -----------------------------------

conversation_history = []

conversation_summary = ""

# -----------------------------------
# CREATE LLM
# -----------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

print("\nAI Learning Companion Started!")
print("Type 'exit' to quit.\n")

# -----------------------------------
# MEMORY IMPORTANCE CHECK
# -----------------------------------

def should_save_memory(text):

    important_keywords = [
        "i learned",
        "i struggle",
        "important",
        "remember",
        "difficulty",
        "weak at",
        "confused",
        "don't understand",
    ]

    text_lower = text.lower()

    return any(
        keyword in text_lower
        for keyword in important_keywords
    )

# -----------------------------------
# CONVERSATION SUMMARIZATION
# -----------------------------------

def summarize_conversation(history):

    history_text = "\n".join(history)

    summary_prompt = f"""
Summarize this conversation briefly.

Focus on:
- important concepts
- user struggles
- learning progress
- preferences

Conversation:
{history_text}
"""

    response = llm.invoke(summary_prompt)

    return response.content

# -----------------------------------
# MAIN CHAT LOOP
# -----------------------------------

while True:

    user_input = input("You: ")

    # -----------------------------------
    # EXIT
    # -----------------------------------

    if user_input.lower() == "exit":
        break

    # -----------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------

    conversation_history.append(
        f"User: {user_input}"
    )

    # -----------------------------------
    # CONVERSATION SUMMARIZATION
    # -----------------------------------

    if len(conversation_history) > 10:

        conversation_summary = summarize_conversation(
            conversation_history
        )

        # Keep only recent messages
        conversation_history = (
            conversation_history[-4:]
        )

        print("\n[Conversation Summarized]")

    # -----------------------------------
    # SAVE NORMAL NOTES
    # -----------------------------------

    if "save note" in user_input.lower():

        note = (
            user_input
            .replace("save note", "")
            .strip()
        )

        save_note(note)

        print("\nAgent:")
        print("Note saved successfully.")

    # -----------------------------------
    # SHOW NOTES
    # -----------------------------------

    elif "show my notes" in user_input.lower():

        notes = get_notes()

        print("\nAgent:")
        print(notes)

    # -----------------------------------
    # SAVE SEMANTIC MEMORY
    # -----------------------------------

    elif "save semantic memory" in user_input.lower():

        memory_text = (
            user_input
            .replace(
                "save semantic memory",
                ""
            )
            .strip()
        )

        result = save_memory(memory_text)

        print("\nAgent:")
        print(result)

    # -----------------------------------
    # INGEST PDF
    # -----------------------------------

    elif "ingest pdf" in user_input.lower():

        pdf_path = (
            user_input
            .replace("ingest pdf", "")
            .strip()
        )

        result = ingest_pdf(pdf_path)

        print("\nAgent:")
        print(result)

    # -----------------------------------
    # NORMAL RAG CHAT
    # -----------------------------------

    else:

        # -----------------------------------
        # RETRIEVAL ROUTING
        # -----------------------------------

        pdf_keywords = [
            "pdf",
            "document",
            "notes",
            "paper",
            "file",
        ]

        memory_keywords = [
            "i learned",
            "i struggle",
            "remember",
            "my weakness",
            "my notes",
        ]

        user_input_lower = user_input.lower()

        # PDF Retrieval
        if any(
            keyword in user_input_lower
            for keyword in pdf_keywords
        ):

            retrieved_memories = search_memory(
                user_input,
                source="pdf"
            )

            retrieval_source = "PDF Knowledge"

        # Memory Retrieval
        elif any(
            keyword in user_input_lower
            for keyword in memory_keywords
        ):

            retrieved_memories = search_memory(
                user_input,
                source="memory"
            )

            retrieval_source = "Personal Memory"

        # Hybrid Retrieval
        else:

            retrieved_memories = search_memory(
                user_input
            )

            retrieval_source = "Hybrid Search"

        # -----------------------------------
        # RECENT CHAT HISTORY
        # -----------------------------------

        recent_history = "\n".join(
            conversation_history[-6:]
        )

        # -----------------------------------
        # AUGMENTED PROMPT
        # -----------------------------------

        augmented_prompt = f"""
You are an AI Learning Companion.

Conversation Summary:
{conversation_summary}

Recent Conversation:
{recent_history}

Relevant Past Memories:
{retrieved_memories}

User Question:
{user_input}
"""

        # -----------------------------------
        # GENERATE RESPONSE
        # -----------------------------------

        response = llm.invoke(
            augmented_prompt
        )

        print("\nAgent:")
        print(
            f"[Retrieval Source: {retrieval_source}]"
        )
        print(response.content)

        # -----------------------------------
        # SAVE AGENT RESPONSE
        # -----------------------------------

        conversation_history.append(
            f"Agent: {response.content}"
        )

        # -----------------------------------
        # AUTOMATIC MEMORY SAVING
        # -----------------------------------

        if should_save_memory(user_input):

            save_memory(user_input)

            print(
                "\n[Memory Automatically Saved]"
            )

    print("\n" + "-" * 50 + "\n")