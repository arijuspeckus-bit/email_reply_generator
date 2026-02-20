# ✉️ AI El. laiškų asistentas (v2.1)

AI pagrįsta Streamlit aplikacija, leidžianti:

- Generuoti el. laiškus nuo nulio
- Perrašyti esamus juodraščius
- Naudoti kelis LLM tiekėjus (DeepSeek arba Ollama)
- Naudoti dokumentacijos RAG kontekstą su šaltinių citavimu

---

# 🚀 Nauja v2.1 – Dokumentacijos RAG

Aplikacija gali „pasikrauti“ dokumentaciją iš `docs/` aplanko ir:

- Suskaidyti dokumentus į chunk’us
- Sugeneruoti embeddings
- Atrinkti top-k fragmentus
- Įtraukti juos į prompt kaip kontekstą
- Parodyti panaudotus šaltinius („Sources“)

Jei „Naudoti dokumentacijos kontekstą“ išjungta – atsakymas generuojamas be šaltinių.

---

# 🧠 Palaikomi modelių tiekėjai

## 🔹 DeepSeek (per API key)

Naudoja `.env` failą:

```
DEEPSEEK_API_KEY=your_api_key_here
```

## 🔹 Ollama (lokaliai)

Naudoja lokalų serverį:

```
http://localhost:11434
```

Modeliai aptinkami automatiškai.

---

# 🔹 Funkcionalumas

## 1️⃣ Generuoti nuo nulio

- Tema
- Kontekstas
- Tikslas
- Modelio pasirinkimas
- (Pasirinktinai) Dokumentacijos kontekstas

Grąžinamas tik galutinis el. laiško tekstas.

---

## 2️⃣ Perrašyti juodraštį

Galima:

- ✂️ Trumpinti
- ➕ Pailginti
- 🙂 Padaryti mandagesnį
- 💪 Padaryti tiesesnį
- ✅ Taisyti gramatiką

Rodomas „Prieš / Po“ palyginimas.

---

# 📚 RAG veikimo principas

1. Dokumentai laikomi `docs/`
2. Tekstas suskaidomas į ~500 simbolių chunk’us
3. Generuojami embeddings (`sentence-transformers`)
4. Skaičiuojamas panašumas (cosine similarity per dot product)
5. Top-k fragmentai įtraukiami į prompt
6. UI rodo „Sources“ (failo pavadinimas + chunk id)

---

# 🏗 Projekto struktūra

```
email_reply_generator/
│
├── app.py
├── docs/
│   ├── streamlit_docs.txt
│   └── ollama_api.txt
│
├── .env
├── requirements.txt
└── README.md
```

---

# 🛠 Naudojamos technologijos

- Python 3.10+
- Streamlit
- DeepSeek API
- Ollama
- sentence-transformers
- numpy
- requests
- python-dotenv

---

# ⚙️ Diegimas

## 1️⃣ Klonuok repozitoriją

```bash
git clone https://github.com/tavo-vartotojas/email_reply_generator.git
cd email_reply_generator
```

---

## 2️⃣ Sukurk virtualią aplinką

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Įdiek priklausomybes

```bash
pip install streamlit openai python-dotenv requests sentence-transformers numpy
```

---

# 🔐 Paleidimas su DeepSeek

1️⃣ Sukurk `.env` failą:

```
DEEPSEEK_API_KEY=your_api_key_here
```

2️⃣ Paleisk aplikaciją:

```bash
python -m streamlit run app.py
```

3️⃣ UI pasirink:
- Provider → DeepSeek

---

# 💻 Paleidimas su Ollama

1️⃣ Patikrink ar Ollama įdiegta:

```bash
ollama list
```

2️⃣ Jei reikia modelio:

```bash
ollama pull llama3
```

3️⃣ Paleisk modelį:

```bash
ollama run llama3
```

4️⃣ Paleisk Streamlit:

```bash
python -m streamlit run app.py
```

5️⃣ UI pasirink:
- Provider → Ollama

---

# 📂 Dokumentacijos naudojimas (RAG)

1️⃣ Įdėk `.txt` dokumentus į `docs/` aplanką  
2️⃣ Pažymėk „Naudoti dokumentacijos kontekstą“  
3️⃣ Pasirink k (kiek fragmentų naudoti)  
4️⃣ Generuok atsakymą  

Atsakyme bus rodomi panaudoti šaltiniai.

---

# 📌 Versijos

### v1.0
- Paprastas laiškų generatorius

### v1.1
- Tonų pasirinkimas
- UI patobulinimai

### v1.2
- 2 tab’ai
- Rewrite funkcionalumas
- Before / After

### v2.0
- Multi-provider (DeepSeek + Ollama)
- Dinaminis modelio pasirinkimas
- Vienoda LLM sąsaja

### v2.1
- Dokumentacijos RAG
- Chunking
- Embeddings
- Top-k retrieval
- „Sources“ rodymas

---

# 🎯 Projekto tikslas

Sukurti moduliniu principu veikiantį AI el. laiškų įrankį su:

- Kelių modelių palaikymu
- Išplėstine architektūra
- Dokumentacijos konteksto integracija
- Aiškiu šaltinių citavimu

---

## 👤 Autorius

Arijus Peckus  
Projektas sukurtas mokymosi ir praktikos tikslais.