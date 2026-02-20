import streamlit as st
import requests
from llm_clients.deepseek_client import DeepSeekClient
from llm_clients.ollama_client import OllamaClient

st.set_page_config(page_title="AI El. laiškų asistentas", page_icon="✉️")

st.title("✉️ AI El. laiškų asistentas")

# =====================================================
# MODELIO PASIRINKIMAS (be sidebar)
# =====================================================

col1, col2 = st.columns(2)

with col1:
    provider = st.selectbox(
        "Modelio tiekėjas",
        ["DeepSeek", "Ollama"]
    )

with col2:
    if provider == "DeepSeek":
        model = st.selectbox(
            "Modelis",
            ["deepseek-chat"]
        )
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

# =====================================================
# TABAI (TAVO SENAS DIZAINAS)
# =====================================================

tab1, tab2 = st.tabs(["Generuoti nuo nulio", "Perrašyti mano juodraštį"])

# =====================================================
# TAB 1 – GENERATE
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
"""

            user_prompt = f"""
Gavėjas: {gavėjas}
Tema: {tema}
Kontekstas: {kontekstas}
Tikslas: {rezultatas}
Tonas: {tonas}

Sugeneruok pilną el. laišką.
"""

            tekstas = llm.generate(system_prompt, user_prompt)

            st.subheader("Sugeneruotas laiškas")
            st.text_area("", tekstas, height=300)


# =====================================================
# TAB 2 – REWRITE
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
                instrukcijos.append("Prailgink tekstą, pridėdamas aiškumo.")

            if tonas_rewrite == "Mandagesnis":
                instrukcijos.append("Padaryk tekstą mandagesnį.")
            elif tonas_rewrite == "Tiesesnis":
                instrukcijos.append("Padaryk tekstą tvirtesnį ir tiesesnį.")

            if taisyti_gramatika:
                instrukcijos.append("Ištaisyk gramatikos klaidas.")

            system_prompt = """
Tu esi profesionalus redaktorius.
Perrašai el. laiškus lietuvių kalba.
Grąžink tik galutinį tekstą.
"""

            user_prompt = f"""
Originalus laiškas:
{draft}

Instrukcijos:
{chr(10).join(instrukcijos)}
"""

            perrasytas = llm.generate(system_prompt, user_prompt)

            st.subheader("Palyginimas")

            col_before, col_after = st.columns(2)

            with col_before:
                st.markdown("### Prieš")
                st.text_area("", draft, height=250)

            with col_after:
                st.markdown("### Po")
                st.text_area("", perrasytas, height=250)