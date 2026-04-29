# 🎬 Mood2Movie — Server Machine Guide

Your personal cheatsheet for running the emotion extraction pipeline.

---

## 📁 Project Structure (quick reference)

```
MOOD2MOVIE/
├── api/
│   ├── server.py          ← Flask API server
│   └── worker.py          ← your local worker
├── core/
│   ├── emotion_extractor.py
│   └── emotion_processor.py
├── database/
│   └── imdb_movies.db
├── worker/                ← folder you share with friends
├── main.py                ← direct DB processing (no server)
├── ngrok.exe
└── .env
```

---

## 🚀 Daily Startup (API mode — with friends)

Open **3 terminals** in order:

**Terminal 1 — Start Flask server:**
```bash
python api/server.py
```
Wait until you see:
```
Running on http://0.0.0.0:5000
```

**Terminal 2 — Start ngrok tunnel:**
```bash
./ngrok http --domain=oxidation-imperfect-trouble.ngrok-free.dev 5000
```
Wait until you see:
```
Forwarding https://oxidation-imperfect-trouble.ngrok-free.dev -> http://localhost:5000
```

**Terminal 3 — Start your local worker:**
```bash
python api/worker.py
```

---

## 🖥️ Solo Mode (no friends, direct DB)

Just one terminal:
```bash
python main.py
```
> ⚠️ Never run main.py while server.py is also running — causes database locked error

---

## ✅ Check Progress

Open in browser anytime:
```
https://oxidation-imperfect-trouble.ngrok-free.dev/progress
```
Shows:
```json
{"done": 11852, "pending": 174106, "stuck": 0, "total": 185958}
```

Or run in Python:
```python
import sqlite3
conn  = sqlite3.connect(r"D:\IMP  ML PROJECTS\Mood2Movie\database\imdb_movies.db")
done  = conn.execute("SELECT COUNT(*) FROM movies WHERE emotion IS NOT NULL AND emotion != 'processing'").fetchone()[0]
total = conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
print(f"✅ {done}/{total} rows done ({done/total*100:.1f}%)")
conn.close()
```

---

## 🧹 Fix Stuck Rows

If any rows got stuck in 'processing' state after a crash:
```bash
curl -X POST https://oxidation-imperfect-trouble.ngrok-free.dev/reset_stuck \
  -H "X-API-Secret: YOUR_API_SECRET"
```

Or in Python:
```python
import sqlite3
conn = sqlite3.connect(r"D:\IMP  ML PROJECTS\Mood2Movie\database\imdb_movies.db")
fixed = conn.execute("UPDATE movies SET emotion = NULL WHERE emotion = 'processing'").rowcount
conn.commit()
conn.close()
print(f"✅ Reset {fixed} stuck rows")
```

---

## 🔑 Add New API Keys

1. Friend creates account at `console.groq.com`
2. They generate a key and send it to you privately
3. Add to `.env`:
```
GROQ_API_KEY_16=gsk_newkeyhere
```
4. Restart `main.py` or `worker.py` — picks up automatically

---

## 🗃️ Database Maintenance

**Remove duplicate rows:**
```python
import sqlite3
conn = sqlite3.connect(r"D:\IMP  ML PROJECTS\Mood2Movie\database\imdb_movies.db")
conn.execute("""
    DELETE FROM movies WHERE rowid NOT IN (
        SELECT MIN(rowid) FROM movies GROUP BY movie_name, year, month
    )
""")
conn.commit()
conn.close()
```

**Clean rows with missing storyline:**
```python
conn.execute("""
    DELETE FROM movies
    WHERE storyline = 'N/A' OR storyline IS NULL OR TRIM(storyline) = ''
""")
conn.commit()
```

**Reset empty emotion rows:**
```python
conn.execute("UPDATE movies SET emotion = NULL WHERE TRIM(emotion) = ''")
conn.commit()
```

---

## 📤 Share With Friends

1. Zip the worker folder:
```bash
python zip_worker.py
```
2. Send `worker.zip` to friend
3. Send these privately via WhatsApp:
```
SERVER_URL=https://oxidation-imperfect-trouble.ngrok-free.dev
API_SECRET=your_secret_here
```

---

## ⚡ Git Commands

```bash
# save work
git add .
git commit -m "your message here"
git push origin main

# check status
git status

# check what changed
git diff
```

---

## 🛑 Shutdown

```
Terminal 3 → Ctrl+C  (stop worker)
Terminal 1 → Ctrl+C  (stop server)
Terminal 2 → Ctrl+C  (stop ngrok)
```

> Always stop in this order — worker first, then server, then ngrok

---

*Keep this file handy — update it whenever something changes!*
