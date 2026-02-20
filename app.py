import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Užkraunam .env failą
load_dotenv()

# Inicializuojam DeepSeek klientą
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

st.set_page_config(page_title="El. laiškų generatorius", page_icon="✉️")

st.title("✉️ AI El. laiškų atsakymų generatorius")
st.markdown("Greitai sugeneruok profesionalų el. laiško atsakymą.")

# -------------------------
# ĮVESTYS
# -------------------------

gavėjas = st.text_input("Gavėjo vardas")
tema = st.text_input("Laiško tema")
kontekstas = st.text_area("Kontekstas (apie ką šis laiškas?)")
rezultatas = st.text_area("Norimas rezultatas (ką nori pasiekti?)")

tonas = st.selectbox(
    "Pasirink toną",
    [
        "Formalus",
        "Draugiškas",
        "Trumpas",
        "Klientų aptarnavimas",
        "Primenantis (Follow-up)"
    ]
)

generuoti = st.button("Generuoti")

# -------------------------
# TONO INSTRUKCIJOS
# -------------------------

tono_instrukcijos = {
    "Formalus": "Rašyk profesionaliu, mandagiu ir struktūruotu tonu.",
    "Draugiškas": "Rašyk šiltu, natūraliu ir draugišku tonu.",
    "Trumpas": "Rašyk trumpai, aiškiai ir be nereikalingų detalių.",
    "Klientų aptarnavimas": "Rašyk kaip profesionalus klientų aptarnavimo specialistas. Būk aiškus, paslaugus ir užtikrinantis.",
    "Primenantis (Follow-up)": "Rašyk mandagų priminimo laišką. Gerbk gavėjo laiką ir švelniai paragink atsakyti."
}

# -------------------------
# GENERAVIMAS
# -------------------------

if generuoti:

    if not tema or not kontekstas or not rezultatas:
        st.warning("Prašome užpildyti temą, kontekstą ir norimą rezultatą.")
    else:

        system_prompt = """
Tu esi profesionalus komunikacijos specialistas,
kuris rašo aukštos kokybės el. laiškus lietuvių kalba.

Taisyklės:
- Visada laikykis pasirinkto tono.
- Laiškas turi būti aiškus ir struktūruotas.
- Įtrauk pasisveikinimą ir užbaigimą.
- Nepridėk paaiškinimų už laiško ribų.
- Grąžink tik galutinį laiško tekstą.
"""

        user_prompt = f"""
Gavėjo vardas: {gavėjas}
Tema: {tema}
Kontekstas: {kontekstas}
Norimas rezultatas: {rezultatas}

Tono instrukcija:
{tono_instrukcijos[tonas]}

Sugeneruok pilną el. laišką.
"""

        try:
            with st.spinner("Generuojamas laiškas..."):

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.7,
                )

                laiskas = response.choices[0].message.content

            st.subheader("Sugeneruotas laiškas")
            st.text_area("", laiskas, height=400)

        except Exception as e:
            st.error(f"Klaida generuojant laišką: {e}")