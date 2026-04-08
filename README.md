# 🎙️ Audio Transcriber

A beginner-friendly Python project that **records audio from your microphone** and **converts it to text** using the AssemblyAI API. Two simple scripts — record, then transcribe!

---

## 📌 What This Project Does
      
| Script | What it does |
|---|---|
| `record mic.py` | 🎤 Records audio from your mic and saves it as `output.wav` |
| `main.py` | 📝 Sends `output.wav` to AssemblyAI and saves the result to `output_transcript.txt` |

---

## 🧰 Requirements

Before you start, make sure you have:

- ✅ Python 3.7 or higher → [Download Python](https://www.python.org/downloads/)
- ✅ A working microphone
- ✅ A free AssemblyAI account → [Sign up here](https://www.assemblyai.com/)
- ✅ pip (comes installed with Python)

---


## 🔑 Step 1 — Get Your AssemblyAI API Key

1. Go to **[https://www.assemblyai.com/](https://www.assemblyai.com/)**
2. Click **"Sign Up"** — it's completely free, no credit card needed
3. After logging in, go to your **Dashboard**
4. Your **API Key** will be at the top of the page — it looks like this:
   ```
   a1b2c3d4e5f6g7h8i9j0...
   ```
5. **Copy it** — you'll need it in the next step

> ⚠️ Keep your API key private! Never share it or push it to GitHub.

---

## 🗂️ Step 2 — Clone & Install

```bash
git clone https://github.com/your-username/audio-transcriber.git
cd audio-transcriber
```

```bash
pip install -r requirements.txt
```

---

## 🔐 Step 3 — Add Your API Key

This project uses `apisecrets.py` to store your API key **locally and safely**.

### Instructions:

1. In the project folder, you'll see a file called **`apisecrets.example.py`**
2. Make a **copy** of it and rename the copy to **`apisecrets.py`**
3. Open `apisecrets.py` and paste your API key:

```python
# apisecrets.py
API_KEY = "paste_your_api_key_here"
```

**Example:**
```python
API_KEY = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
```

> ✅ `apisecrets.py` is listed in `.gitignore` — it will **never** be uploaded to GitHub.
>
> ✅ Only `apisecrets.example.py` (with no real key) is uploaded so others know the format.

---

## ▶️ Step 4 — Run the Project

### 🎤 Record your audio

```bash
python "record mic.py"
```

- Speak into your microphone when it starts recording
- When done, it saves your audio as `output.wav`

### 📝 Transcribe the audio

```bash
python main.py
```

- Sends `output.wav` to AssemblyAI
- The transcribed text is printed in the terminal **and** saved to `output_transcript.txt`

---

## 📁 Project Structure

```
PJ3/
│
├── record mic.py            # 🎤 Records audio → saves as output.wav
├── main.py                  # 📝 Transcribes audio → saves to output_transcript.txt
│
├── apisecrets.example.py    # ✅ Safe template — uploaded to GitHub
├── apisecrets.py            # 🔒 YOUR real API key — NOT uploaded to GitHub
│
├── output.wav               # Generated audio file (ignored by Git)
├── output_transcript.txt    # Generated transcript (ignored by Git)
│
├── requirements.txt         # Python packages needed
├── .gitignore               # Tells Git what NOT to upload
└── README.md                # This file
```

---

## 📄 What's in `apisecrets.example.py`?

This file is a **safe placeholder** so other developers know what `apisecrets.py` should look like:

```python
# apisecrets.example.py
# Copy this file, rename it to apisecrets.py, and add your real API key

API_KEY = "your_assemblyai_api_key_here"
```

---

## 📦 Dependencies

Install everything at once:

```bash
pip install -r requirements.txt
```

Main packages used:
- `pyaudio` — for recording audio from the microphone
- `assemblyai` — for sending audio to AssemblyAI and getting text back

---

## ❓ Common Issues

**`ModuleNotFoundError`**
→ Run `pip install -r requirements.txt` again

**`PyAudio` fails to install on Windows**
→ Download the correct `.whl` from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install manually

**`Invalid API Key` error**
→ Open `apisecrets.py` and make sure you pasted the key correctly with no extra spaces

**No audio is recorded**
→ Check that your microphone is plugged in and set as the default input device in your system settings

---

## 🛡️ Security Reminder

| File | Uploaded to GitHub? |
|---|---|
| `apisecrets.example.py` | ✅ Yes — it has no real key |
| `apisecrets.py` | ❌ No — your real key stays local |
| `output.wav` | ❌ No — audio files are ignored |
| `output_transcript.txt` | ❌ No — transcripts are ignored |

---

## 📄 License

MIT License — free to use and modify.

---

## 🙌 Author

Made by [senseihx4](https://github.com/senseihx4)  
If this helped you, give the repo a ⭐ on GitHub!
