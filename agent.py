
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from chroma_memory import (
    save_memory,
    search_memory,
)

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

# -----------------------------------
# CREATE LLM
# -----------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

# -----------------------------------
# GLOBAL MEMORY
# -----------------------------------

conversation_history = []

conversation_summary = ""

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
# MAIN AI CHAT FUNCTION
# -----------------------------------

def chat_with_agent(user_input):

    global conversation_history
    global conversation_summary

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

        conversation_summary = (
            summarize_conversation(
                conversation_history
            )
        )

        conversation_history = (
            conversation_history[-4:]
        )

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
        print("\nDEBUG RETRIEVED:\n")
        print(retrieved_memories)

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

Use the retrieved context below to answer the user's question.

IMPORTANT:
- Base your answer on the retrieved context
- If information exists in context, summarize it clearly
- Do NOT say you lack information if context is provided
- Explain concepts in simple language

Retrieved Context:
{retrieved_memories}

Conversation Summary:
{conversation_summary}

Recent Conversation:
{recent_history}

User Question:
{user_input}
"""

    # -----------------------------------
    # GENERATE RESPONSE
    # -----------------------------------

    response = llm.invoke(
        augmented_prompt
    )

    final_response = response.content

    # -----------------------------------
    # SAVE AGENT RESPONSE
    # -----------------------------------

    conversation_history.append(
        f"Agent: {final_response}"
    )

    # -----------------------------------
    # AUTO MEMORY SAVE
    # -----------------------------------

    if should_save_memory(user_input):

        save_memory(user_input)

    # -----------------------------------
    # RETURN DATA
    # -----------------------------------

    return {
        "response": final_response,
        "retrieval_source": retrieval_source,
    }
