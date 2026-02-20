import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Užkrauname .env
load_dotenv()

# DeepSeek klientas (OpenAI compatible)
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

st.set_page_config(page_title="DeepSeek Email Reply Generator", page_icon="📧")

st.title("📧 AI Email Reply Generator (DeepSeek)")
st.write("Sugeneruok profesionalų atsakymą į gautą laišką naudojant DeepSeek LLM.")

# Įvestis
email_content = st.text_area("Įklijuok gautą el. laišką:", height=200)

tone = st.selectbox(
    "Pasirink atsakymo toną:",
    ["Profesionalus", "Draugiškas", "Formalus", "Trumpas ir konkretus"]
)

language = st.selectbox(
    "Atsakymo kalba:",
    ["Lietuvių", "Anglų"]
)

if st.button("Sugeneruoti atsakymą"):
    if email_content.strip() == "":
        st.warning("Įvesk el. laiško tekstą.")
    else:
        with st.spinner("Generuojamas atsakymas..."):

            prompt = f"""
Tu esi profesionalus verslo asistentas.

Sugeneruok {tone.lower()} atsakymą {language.lower()} kalba.

Laiškas:
{email_content}

Atsakymas:
"""

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Tu esi profesionalus AI asistentas, kuris rašo aiškius ir profesionalius atsakymus į el. laiškus."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            reply = response.choices[0].message.content

        st.subheader("✉️ Sugeneruotas atsakymas:")
        st.text_area("Atsakymas:", reply, height=250)