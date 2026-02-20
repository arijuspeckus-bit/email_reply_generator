import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Užkraunam .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

st.set_page_config(page_title="AI El. laiškų įrankis", page_icon="✉️")

st.title("✉️ AI El. laiškų asistentas")

tab1, tab2 = st.tabs(["Generuoti nuo nulio", "Perrašyti mano juodraštį"])

# =====================================================
# TAB 1 – GENERATE FROM SCRATCH
# =====================================================

with tab1:

    st.subheader("Naujo laiško generavimas")

    gavėjas = st.text_input("Gavėjo vardas")
    tema = st.text_input("Laiško tema")
    kontekstas = st.text_area("Kontekstas")
    rezultatas = st.text_area("Norimas rezultatas")

    tonas = st.selectbox(
        "Tonas",
        ["Formalus", "Draugiškas", "Tiesus", "Mandagus"]
    )

    generuoti = st.button("Generuoti laišką")

    if generuoti:

        if not tema or not kontekstas or not rezultatas:
            st.warning("Užpildykite visus laukus.")
        else:

            system_prompt = """
Tu esi profesionalus komunikacijos specialistas.
Rašai aukštos kokybės el. laiškus lietuvių kalba.

Grąžink tik galutinį laiško tekstą.
Be komentarų.
"""

            user_prompt = f"""
Gavėjas: {gavėjas}
Tema: {tema}
Kontekstas: {kontekstas}
Tikslas: {rezultatas}
Tonas: {tonas}

Sugeneruok pilną el. laišką.
"""

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
            st.text_area("", laiskas, height=300)


# =====================================================
# TAB 2 – REWRITE MY DRAFT
# =====================================================

with tab2:

    st.subheader("Juodraščio perrašymas")

    draft = st.text_area("Įklijuok savo juodraštį", height=200)

    col1, col2 = st.columns(2)

    with col1:
        ilgis = st.selectbox(
            "Ilgio keitimas",
            ["Nekeisti", "Trumpinti", "Pailginti"]
        )

    with col2:
        tonas_rewrite = st.selectbox(
            "Stilius",
            ["Nekeisti", "Mandagesnis", "Tiesesnis"]
        )

    taisyti_gramatika = st.checkbox("Taisyti gramatiką")

    perrasyti = st.button("Perrašyti laišką")

    if perrasyti:

        if not draft:
            st.warning("Įklijuokite juodraštį.")
        else:

            instrukcijos = []

            if ilgis == "Trumpinti":
                instrukcijos.append("Sutrumpink tekstą, išlaikant esmę.")
            elif ilgis == "Pailginti":
                instrukcijos.append("Prailgink tekstą, pridėdamas aiškumo ir detalių.")

            if tonas_rewrite == "Mandagesnis":
                instrukcijos.append("Padaryk tekstą mandagesnį ir diplomatiškesnį.")
            elif tonas_rewrite == "Tiesesnis":
                instrukcijos.append("Padaryk tekstą tvirtesnį ir tiesesnį.")

            if taisyti_gramatika:
                instrukcijos.append("Ištaisyk gramatikos ir skyrybos klaidas.")

            system_prompt = """
Tu esi profesionalus redaktorius.
Perrašai el. laiškus lietuvių kalba.

Grąžink tik galutinį perrašytą laišką.
Be komentarų.
"""

            user_prompt = f"""
Originalus laiškas:
{draft}

Instrukcijos:
{chr(10).join(instrukcijos)}

Perrašyk laišką pagal nurodymus.
"""

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.5,
            )

            perrasytas = response.choices[0].message.content

            st.subheader("Palyginimas")

            col_before, col_after = st.columns(2)

            with col_before:
                st.markdown("### Prieš")
                st.text_area("", draft, height=250)

            with col_after:
                st.markdown("### Po")
                st.text_area("", perrasytas, height=250)