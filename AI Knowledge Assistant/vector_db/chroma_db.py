from config import get_db

def store_embeddings(document_id, chunks, embeddings, filename):
    ids = []
    metadata = []
    for i in range(len(chunks)):
        ids.append(f"{document_id}_chunk_{i}")
        metadata.append({"document_id" : document_id,"filename" : filename, "chunk" : i})

    client = get_db()

    collection = client.get_or_create_collection(name="my_collection")

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadata
    )

def search(query_embeddings, top_k = 3):
    client = get_db()
    collection = client.get_collection(name = 'my_collection')
    results = collection.query(
        query_embeddings = [query_embeddings.tolist()],
        n_results = top_k
    )
    return results

def document_exists(document_id):
    client = get_db()
    collection = client.get_or_create_collection(name = "my_collection")
    result = collection.get(ids=[f"{document_id}_chunk_0"])
    if result["ids"]:
        return True
    return False

def delete_document(document_id):
    client = get_db()
    collection = client.get_collection(name = "my_collection")
    collection.delete(
        where={"document_id":document_id}
    )


def get_documents():
    client = get_db()
    collection  = client.get_or_create_collection(name="my_collection")
    metadata = collection.get()['metadatas']

    documents = {}
    for data in metadata:
        documents[data["document_id"]] = data["filename"]

    return documents






