from vector_store import document_exists, store_chunks
from chunking import generate_chunks




def ingest_document(pdf, document_id, model, status_container):
    if document_exists(document_id):
        return False

    status_container.write("Chunking the data in the file...")
    chunks = generate_chunks(pdf)

    embeddings = model.encode(chunks)

    store_chunks(chunks, embeddings, document_id)
    return True