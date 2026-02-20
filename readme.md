# ✉️ AI El. laiškų asistentas

Streamlit aplikacija, leidžianti generuoti naujus el. laiškus arba profesionaliai perrašyti jau turimus juodraščius naudojant AI.

---

## 🚀 Funkcionalumas

### 🔹 1. Generuoti nuo nulio
Sukurk profesionalų el. laišką pagal:
- Gavėjo vardą
- Temą
- Kontekstą
- Norimą rezultatą
- Pasirinktą toną

Modelis sugeneruoja pilną, struktūruotą laišką lietuvių kalba.

---

### 🔹 2. Perrašyti mano juodraštį

Įklijuok savo tekstą ir pasirink:

- ✂️ **Trumpinti**
- ➕ **Pailginti**
- 🙂 **Padaryti mandagesnį**
- 💪 **Padaryti tiesesnį**
- ✅ **Ištaisyti gramatiką**

Rodomas „Prieš / Po“ palyginimas.

Išvestis visada pateikiama kaip:
> Tik galutinis el. laiško tekstas (be papildomų komentarų).

---

## 🛠 Naudojamos technologijos

- Python 3.10+
- Streamlit
- DeepSeek API
- python-dotenv

---

## ⚙️ Diegimas

### 1️⃣ Klonuok repozitoriją

```bash
git clone https://github.com/tavo-vartotojas/email_reply_generator.git
cd email_reply_generator
```

---

### 2️⃣ Sukurk virtualią aplinką (rekomenduojama)

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

### 3️⃣ Įdiek priklausomybes

Jei turi `requirements.txt`:
```bash
pip install -r requirements.txt
```

Arba rankiniu būdu:
```bash
pip install streamlit openai python-dotenv
```

---

### 4️⃣ Sukurk `.env` failą

Projekto kataloge sukurk `.env` failą:

```
DEEPSEEK_API_KEY=your_api_key_here
```

⚠️ Niekada nekelk `.env` failo į GitHub.

Rekomenduojama `.gitignore` faile turėti:
```
.env
venv/
```

---

## ▶️ Paleidimas

```bash
python -m streamlit run app.py
```

Aplikacija atsidarys naršyklėje automatiškai.

---

## 📂 Projekto struktūra

```
email_reply_generator/
│
├── app.py
├── README.md
├── requirements.txt
├── .env (neįtraukiamas į Git)
└── venv/
```

---

## 🎯 Projekto tikslas

Sukurti paprastą, bet profesionalų AI įrankį, kuris:
- taupo laiką
- pagerina komunikacijos kokybę
- padeda rašyti aiškiau ir efektyviau

---

## 📌 Versijos

### v1.0
- Paprastas laiškų generatorius

### v1.1
- Tonų pasirinkimas
- UI patobulinimai

### v1.2
- 2 tab’ai (Generate / Rewrite)
- Juodraščio redagavimas
- Before / After palyginimas
- Gramatikos taisymas
- Teksto trumpinimas / ilginimas
- Mandagesnis / tiesesnis tonas

---

## 👤 Autorius

Arijus Peckus  
Projektas sukurtas mokymosi ir praktikos tikslais.