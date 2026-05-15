import chromadb

from sentence_transformers import SentenceTransformer

# Create persistent Chroma client
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="learning_memory"
)

# Embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def save_memory(text):

    embedding = embedding_model.encode(text).tolist()

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(hash(text))],
        metadatas=[
    {
        "source": "memory"
    }
]
        
    )

    return "Semantic memory saved."

def search_memory(query, source=None):

    try:

        query_embedding = (
            embedding_model
            .encode(query)
            .tolist()
        )

        # -----------------------------------
        # FILTERED SEARCH
        # -----------------------------------

        if source:

            results = collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=5,
                where={
                    "source": source
                }
            )

        # -----------------------------------
        # HYBRID SEARCH
        # -----------------------------------

        else:

            results = collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=5
            )

        # -----------------------------------
        # EXTRACT DOCUMENTS
        # -----------------------------------

        documents = results["documents"][0]

        if not documents:

            return "No relevant memories found."

        return "\n\n".join(documents)

    except Exception as e:

        return f"Memory search error: {str(e)}"

