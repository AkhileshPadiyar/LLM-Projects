import chromadb

client = chromadb.PersistentClient(
    path = './chromadb'
)

collection = client.get_or_create_collection(
    name = 'documents'
)

def document_exists(document_id):
    result = collection.get(
        where = {
            "document_id" : document_id
        },
        limit = 1
    )

    return len(result['ids']) > 0

def store_chunks(chunks, embedding, document_id):
    ids = []

    for i in range(len(chunks)):
        ids.append(f"{document_id}_chunk_{i}")

    collection.add(
        ids = ids,
        documents=chunks,
        embeddings= embedding.tolist(),
        metadatas = [
            {
                "document_id" : document_id,
                "chunk_index" : i
            }
            for i in range(len(chunks))
        ]
    )

def search(query, top_k=3):
    result = collection.query(
        query_embeddings = [query.tolist()],
        n_results = top_k
    )
    return result['documents'][0]



































