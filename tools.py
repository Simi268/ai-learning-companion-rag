from langchain.tools import tool
from memory import save_note, get_notes
from chroma_memory import (
    save_memory,
    search_memory,
)


@tool
def save_learning_note(note: str) -> str:
    """
    Save a learning note to memory.
    """

    save_note(note)

    return "Note saved successfully."


@tool
def recall_learning_notes(dummy: str = "") -> str:
    """
    Recall all saved learning notes.
    """

    return get_notes()


@tool
def concept_explainer(topic: str) -> str:
    """
    Explain a concept simply.
    """

    return f"""
Concept: {topic}

This concept is important in AI and software engineering.

Study it step-by-step and practice building projects around it.
"""

@tool
def save_semantic_memory(note: str) -> str:
    """
    Save semantic memory into ChromaDB.
    """

    return save_memory(note)


@tool
def search_semantic_memory(query: str) -> str:
    """
    Search semantic memory.
    """

    results = search_memory(query)

    return "\n".join(results)