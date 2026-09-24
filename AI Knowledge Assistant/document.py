
def extract_text(f):
    content = f.read().decode('utf-8')
    filename = f.name
    return content, filename
