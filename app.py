import streamlit as st
import requests
import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

# ===============================
# ENV
# ===============================

load_dotenv()

# ===============================
# LLM CLIENTS
# ===============================

class DeepSeekClient:
    def __init__(self, model="deepseek-chat"):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.model = model

    def generate(self, system_prompt, user_prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content


class OllamaClient:
    def __init__(self, model="llama3"):
        self.model = model
        self.base_url = "http://localhost:11434/api/chat"

    def generate(self, system_prompt, user_prompt):

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False
        }

        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()

        return response.json()["message"]["content"]


# ===============================
# RAG LOGIC
# ===============================

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_documents(docs_path="docs"):
    documents = []
    if not os.path.exists(docs_path):
        return documents

    for filename in os.listdir(docs_path):
        path = os.path.join(docs_path, filename)
        if filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                documents.append({
                    "filename": filename,
                    "text": f.read()
                })
    return documents


def chunk_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def build_index(documents):
    chunks = []
    metadata = []

    for doc in documents:
        split = chunk_text(doc["text"])
        for i, chunk in enumerate(split):
            chunks.append(chunk)
            metadata.append({
                "filename": doc["filename"],
                "chunk_id": i
            })

    if not chunks:
        return [], None, []

    embeddings = embedding_model.encode(chunks)
    return chunks, embeddings, metadata


def retrieve(query, chunks, embeddings, metadata, k=3):
    query_embedding = embedding_model.encode([query])[0]
    similarities = np.dot(embeddings, query_embedding)
    top_indices = np.argsort(similarities)[-k:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "text": chunks[idx],
            "filename": metadata[idx]["filename"],
            "chunk_id": metadata[idx]["chunk_id"]
        })
    return results


# ===============================
# STREAMLIT UI
# ===============================

st.set_page_config(page_title="AI El. laiškų asistentas", page_icon="✉️")
st.title("✉️ AI El. laiškų asistentas")

# ===============================
# MODELIO PASIRINKIMAS
# ===============================

col1, col2 = st.columns(2)

with col1:
    provider = st.selectbox(
        "Modelio tiekėjas",
        ["DeepSeek", "Ollama"]
    )

with col2:
    if provider == "DeepSeek":
        model = st.selectbox("Modelis", ["deepseek-chat"])
        llm = DeepSeekClient(model=model)
    else:
        try:
            response = requests.get("http://localhost:11434/api/tags")
            models = [m["name"] for m in response.json()["models"]]
        except:
            models = ["llama3"]
        model = st.selectbox("Modelis", models)
        llm = OllamaClient(model=model)

st.divider()

# ===============================
# RAG SETTINGS
# ===============================

st.subheader("📚 Dokumentacijos kontekstas")

use_docs = st.checkbox("Naudoti dokumentacijos kontekstą")
k_value = st.slider("Kiek fragmentų įtraukti (k)", 1, 5, 3)

if use_docs:
    documents = load_documents()
    chunks, embeddings, metadata = build_index(documents)

st.divider()

# ===============================
# TABAI
# ===============================

tab1, tab2 = st.tabs(["Generuoti nuo nulio", "Perrašyti mano juodraštį"])

# ===============================
# TAB 1 – GENERATE
# ===============================

with tab1:

    st.subheader("Naujo laiško generavimas")

    tema = st.text_input("Tema")
    kontekstas = st.text_area("Kontekstas")
    tikslas = st.text_area("Tikslas")

    if st.button("Generuoti laišką"):

        system_prompt = """
Tu esi profesionalus komunikacijos specialistas.
Grąžink tik galutinį el. laiško tekstą.
"""

        user_prompt = f"""
Tema: {tema}
Kontekstas: {kontekstas}
Tikslas: {tikslas}
Sugeneruok pilną el. laišką.
"""

        sources = []

        if use_docs and chunks:
            results = retrieve(user_prompt, chunks, embeddings, metadata, k=k_value)
            context_text = "\n\n".join([r["text"] for r in results])

            user_prompt = f"""
Naudok šią dokumentaciją kaip kontekstą:

{context_text}

---

{user_prompt}
"""
            sources = results

        tekstas = llm.generate(system_prompt, user_prompt)

        st.subheader("Rezultatas")
        st.text_area("", tekstas, height=300)

        if use_docs and sources:
            st.markdown("### 📚 Sources")
            for s in sources:
                st.markdown(f"- {s['filename']} (chunk {s['chunk_id']})")


# ===============================
# TAB 2 – REWRITE
# ===============================

with tab2:

    st.subheader("Juodraščio perrašymas")

    draft = st.text_area("Įklijuok savo juodraštį", height=200)

    trumpinti = st.checkbox("Trumpinti")
    pailginti = st.checkbox("Pailginti")
    mandagesnis = st.checkbox("Mandagesnis")
    tiesesnis = st.checkbox("Tiesesnis")
    gramatika = st.checkbox("Taisyti gramatiką")

    if st.button("Perrašyti laišką"):

        instrukcijos = []

        if trumpinti:
            instrukcijos.append("Sutrumpink tekstą.")
        if pailginti:
            instrukcijos.append("Prailgink tekstą.")
        if mandagesnis:
            instrukcijos.append("Padaryk tekstą mandagesnį.")
        if tiesesnis:
            instrukcijos.append("Padaryk tekstą tiesesnį.")
        if gramatika:
            instrukcijos.append("Ištaisyk gramatiką.")

        system_prompt = """
Tu esi profesionalus redaktorius.
Grąžink tik galutinį el. laiško tekstą.
"""

        user_prompt = f"""
Originalus tekstas:
{draft}

Instrukcijos:
{chr(10).join(instrukcijos)}
"""

        sources = []

        if use_docs and chunks:
            results = retrieve(user_prompt, chunks, embeddings, metadata, k=k_value)
            context_text = "\n\n".join([r["text"] for r in results])

            user_prompt = f"""
Naudok šią dokumentaciją kaip kontekstą:

{context_text}

---

{user_prompt}
"""
            sources = results

        tekstas = llm.generate(system_prompt, user_prompt)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Prieš")
            st.text_area("", draft, height=250)

        with col2:
            st.markdown("### Po")
            st.text_area("", tekstas, height=250)

        if use_docs and sources:
            st.markdown("### 📚 Sources")
            for s in sources:
                st.markdown(f"- {s['filename']} (chunk {s['chunk_id']})")