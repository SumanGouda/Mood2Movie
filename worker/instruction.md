# 🎬 Mood2Movie — Worker Setup Guide

Hey! Follow these steps carefully and you'll be up and running in 10 minutes.

---

## Step 1 — Install Python

If you don't have Python installed:
- Go to `python.org/downloads`
- Download **Python 3.10 or above**
- During installation **check the box that says "Add Python to PATH"**
- Click Install

Verify it worked — open terminal and run:
```bash
python --version
```
You should see something like `Python 3.11.x`

---

## Step 2 — Extract the ZIP

- Extract the `worker.zip` file I sent you
- You'll get a folder called `worker/`
- Open that folder in VS Code or any editor

---

## Step 3 — Create a Virtual Environment

Open terminal inside the `worker/` folder and run:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python -m venv .venv
source .venv/bin/activate
```

You'll see `(.venv)` appear at the start of your terminal line — that means it worked.

---

## Step 4 — Install Dependencies

With the virtual environment active, run:

```bash
pip install -r requirements.txt
```

Wait for it to finish installing everything.

---

## Step 5 — Create Your Groq API Keys

You need your own free Groq API keys. Here's how:

**Account 1 (your main email):**
1. Go to `console.groq.com`
2. Click **Sign Up** → sign in with Google
3. Go to `console.groq.com/keys`
4. Click **Create API Key**
5. Give it any name → click **Submit**
6. **Copy the key immediately** — it's only shown once!

**Account 2 (a second email):**
- Repeat the same steps with a different Gmail account
- This gives you a second independent rate limit

**Account 3 (a third email):**
- Repeat again with a third Gmail account

> 💡 More keys = more rows processed per day. Even 1 key works fine if you don't have extras.

---

## Step 6 — Set Up Your .env File

Inside the `worker/` folder find the file called `.env.example`.

- **Copy** it and **rename the copy** to `.env`
- Open `.env` and fill in your values:

```
# Get these from your friend who runs the server
SERVER_URL=https://?????.ngrok-free.app
API_SECRET=????

# Your own Groq API keys from Step 5
GROQ_API_KEY_1=gsk_????
GROQ_API_KEY_2=gsk_????
GROQ_API_KEY_3=gsk_????
```

> 📲 Your friend will send you the `SERVER_URL` and `API_SECRET` via WhatsApp each session. The URL may change daily so always use the latest one.

---

## Step 7 — Run the Worker

Make sure your virtual environment is active (you see `(.venv)` in terminal), then run:

```bash
python api/worker.py
```

You'll see output like:
```
🚀 Worker started — connecting to https://?????.ngrok-free.app
🔄 Processing rowid 1 | A wealthy New York City investment...
  ✅ rowid 1 → lonely, powerless, ashamed
🔄 Processing rowid 2 | A Roman general is betrayed and...
  ✅ rowid 2 → angry, betrayed, determined
...
```

**Leave it running** — it will stop automatically when it hits the daily API limit and print:
```
🛑 Groq daily limit hit after XXXX rows — run again tomorrow!
```

---

## Step 8 — Daily Routine

Every day just:
1. Get the latest `SERVER_URL` from your friend via WhatsApp
2. Update it in your `.env` file
3. Activate virtual environment
4. Run `python api/worker.py`
5. Let it run until it stops

---

## ❗ Common Issues

**`ModuleNotFoundError`**
→ Make sure your virtual environment is active (`(.venv)` visible in terminal)
→ Run `pip install -r requirements.txt` again

**`Unauthorized` error**
→ Your `API_SECRET` in `.env` is wrong — ask your friend for the correct one

**`Connection refused` or URL error**
→ The `SERVER_URL` has changed — ask your friend for the new ngrok URL

**`429 Rate limit` stops early**
→ Normal! You've hit today's Groq limit. Run again tomorrow — it picks up where it left off automatically.

---

## 📁 Folder Structure (for reference)

```
worker/
├── core/
│   ├── __init__.py
│   └── emotion_extractor.py
├── api/
│   └── worker.py
├── .env              ← you create this from .env.example
├── .env.example      ← template
└── requirements.txt
```

---

*Thanks for helping! Every session you run gets us closer to finishing the dataset* 🙌