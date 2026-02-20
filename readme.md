# ✉️ AI El. laiškų asistentas (v2.0)

Streamlit aplikacija, leidžianti generuoti naujus el. laiškus arba profesionaliai perrašyti jau turimus juodraščius naudojant skirtingus LLM tiekėjus.

---

## 🚀 Nauja v2.0 architektūra

Aplikacija dabar palaiko kelis modelių tiekėjus:

- 🧠 **DeepSeek (per API key)**
- 💻 **Ollama (lokaliai)**

Tas pats UI veikia su abiem tiekėjais – nereikia keisti kodo.

Modelio pasirinkimas atliekamas aplikacijos viduje.

---

## 🔹 Funkcionalumas

### 1️⃣ Generuoti nuo nulio

Sukurk profesionalų el. laišką pagal:
- Gavėjo vardą
- Temą
- Kontekstą
- Norimą rezultatą
- Pasirinktą toną

Modelis sugeneruoja pilną, struktūruotą laišką lietuvių kalba.

---

### 2️⃣ Perrašyti mano juodraštį

Įklijuok savo tekstą ir pasirink:

- ✂️ Trumpinti
- ➕ Pailginti
- 🙂 Padaryti mandagesnį
- 💪 Padaryti tiesesnį
- ✅ Ištaisyti gramatiką

Rodomas „Prieš / Po“ palyginimas.

Išvestis visada pateikiama kaip:
> Tik galutinis el. laiško tekstas (be papildomų komentarų).

---

## 🏗 Architektūra

Naudojama atskira LLM sąsaja:

```
llm_clients/
│
├── base.py
├── deepseek_client.py
└── ollama_client.py
```

Visi klientai turi vienodą metodą:

```python
generate(system_prompt, user_prompt) -> text
```

Dėl to UI gali veikti su skirtingais tiekėjais nepakeitus aplikacijos logikos.

---

## 🛠 Naudojamos technologijos

- Python 3.10+
- Streamlit
- DeepSeek API
- Ollama
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

## 2️⃣ Sukurk virtualią aplinką (rekomenduojama)

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
pip install -r requirements.txt
```

Jei nėra requirements.txt:

```bash
pip install streamlit openai python-dotenv requests
```

---

# 🔐 Paleidimas su DeepSeek

## 1️⃣ Sukurk `.env` failą

Projekto kataloge:

```
DEEPSEEK_API_KEY=your_api_key_here
```

⚠️ `.env` turi būti įtrauktas į `.gitignore`.

---

## 2️⃣ Paleisk aplikaciją

```bash
python -m streamlit run app.py
```

Aplikacijoje pasirink:
- Provider → **DeepSeek**
- Model → deepseek-chat

---

# 💻 Paleidimas su Ollama

## 1️⃣ Įsitikink, kad Ollama įdiegta

Patikrink:

```bash
ollama list
```

Jei neturi modelio:

```bash
ollama pull llama3
```

---

## 2️⃣ Paleisk Ollama serverį

```bash
ollama run llama3
```

Palik terminalą aktyvų.

---

## 3️⃣ Paleisk Streamlit

```bash
python -m streamlit run app.py
```

Aplikacijoje pasirink:
- Provider → **Ollama**
- Model → (automatiškai aptiktas lokalus modelis)

---

## 📂 Projekto struktūra

```
email_reply_generator/
│
├── app.py
├── llm_clients/
│   ├── __init__.py
│   ├── base.py
│   ├── deepseek_client.py
│   └── ollama_client.py
│
├── README.md
├── requirements.txt
├── .env (neįtraukiamas į Git)
└── venv/
```

---

## 🎯 Projekto tikslas

Sukurti lankstų AI el. laiškų įrankį, kuris:

- veikia tiek su lokaliu modeliu (Ollama),
- tiek su API pagrįstu modeliu (DeepSeek),
- leidžia lengvai išplėsti palaikomų modelių skaičių,
- turi švarią, modulinę architektūrą.

---

## 📌 Versijos

### v1.0
- Paprastas laiškų generatorius

### v1.1
- Tonų pasirinkimas
- UI patobulinimai

### v1.2
- 2 tab’ai (Generate / Rewrite)
- Before / After palyginimas

### v2.0
- Multi-provider palaikymas (Ollama + DeepSeek)
- Modelio pasirinkimas UI
- Atskira `llm_clients` architektūra
- Vienoda `generate()` sąsaja

---

## 👤 Autorius

Arijus Peckus  
Projektas sukurtas mokymosi ir praktikos tikslais.