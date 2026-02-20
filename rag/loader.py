import os

def load_documents(docs_path="docs"):
    documents = []

    for filename in os.listdir(docs_path):
        path = os.path.join(docs_path, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "filename": filename,
            "text": text
        })

    return documents