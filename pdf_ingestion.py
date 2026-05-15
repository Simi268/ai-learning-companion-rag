from pypdf import PdfReader
import uuid

from chroma_memory import (
    collection,
    embedding_model,
)


def ingest_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    full_text = ""

    # -----------------------------------
    # EXTRACT TEXT
    # -----------------------------------

    for page in reader.pages:

        text = page.extract_text()

        if text:

            full_text += text

    # -----------------------------------
    # CHUNK TEXT
    # -----------------------------------

    chunk_size = 500

    chunks = [

        full_text[i:i + chunk_size]

        for i in range(
            0,
            len(full_text),
            chunk_size
        )
    ]

    # -----------------------------------
    # STORE CHUNKS
    # -----------------------------------

    for idx, chunk in enumerate(chunks):

        embedding = (
            embedding_model
            .encode(chunk)
            .tolist()
        )

        collection.add(

            documents=[chunk],

            embeddings=[embedding],

            ids=[str(uuid.uuid4())],

            metadatas=[
                {
                    "source": "pdf",
                    "file_name": pdf_path
                }
            ]
        )

    return f"{len(chunks)} chunks stored successfully."