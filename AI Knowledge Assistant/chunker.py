
def create_chunks(content, chunk_size, overlap):
    if overlap >= chunk_size:
        raise ValueError("Overlap is greater than or equal to chunk_size")
    elif overlap < 0:
        raise ValueError("Overlap is less than 0")
    elif chunk_size <= 0:
        raise ValueError("Chunk_size can't be zero or negative")
    else:
        chunks = []

        start = 0
        while start < len(content):
            end = start + chunk_size
            chunk = content[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks