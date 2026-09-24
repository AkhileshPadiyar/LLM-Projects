import fitz

def extract_text(f):
    filename = f.name
    if filename.lower().endswith(".txt"):
        content = f.read().decode('utf-8')
        return content, filename
    elif filename.lower().endswith('.pdf'):
        pdf_bytes = f.read()
        doc = fitz.open(stream=pdf_bytes,filetype='pdf')
        content = "\n".join(page.get_text() for page in doc)
        doc.close()
        return content, filename
    else:
        return "", filename