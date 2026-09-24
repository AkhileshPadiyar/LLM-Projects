from config import get_sentence_transformer

def generate_embedding(chunks):
    model = get_sentence_transformer()
    embeddings = model.encode(chunks)
    return embeddings

def generate_query_embeddings(query):
    model = get_sentence_transformer()
    embeddings = model.encode(query)
    return embeddings