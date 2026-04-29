import os 
import time
import sqlite3
from itertools import cycle
from dotenv import load_dotenv
from .emotion_extractor import get_emotions_from_storyline

load_dotenv()

# ------------------------------------------------------------------ #
#  Config                                                             #
# ------------------------------------------------------------------ #
GROQ_KEYS = [
    os.getenv("GROQ_API_KEY_4"),
    os.getenv("GROQ_API_KEY_5"),
    os.getenv("GROQ_API_KEY_6"),
    os.getenv("GROQ_API_KEY_7"),
    os.getenv("GROQ_API_KEY_8"),
    os.getenv("GROQ_API_KEY_9"),
    os.getenv("GROQ_API_KEY_10"),
    os.getenv("GROQ_API_KEY_11"),
    os.getenv("GROQ_API_KEY_12"),
    os.getenv("GROQ_API_KEY_13"),
    os.getenv("GROQ_API_KEY_14"),
    os.getenv("GROQ_API_KEY_15"),
] 
GROQ_KEYS  = [k for k in GROQ_KEYS if k]
SLEEP_TIME = 2.0 / len(GROQ_KEYS)

print(f"🔑 Loaded {len(GROQ_KEYS)} API keys | Sleep: {SLEEP_TIME:.2f}s between requests")

key_pool = cycle(GROQ_KEYS)

# ------------------------------------------------------------------ #
#  Setup columns                                                      #
# ------------------------------------------------------------------ #
def setup_columns(db_path):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("ALTER TABLE movies ADD COLUMN emotion TEXT")
        conn.execute("ALTER TABLE movies ADD COLUMN reason  TEXT")
        conn.commit()
        print("✅ Added emotion and reason columns")
    except:
        print("ℹ️  Columns already exist — skipping")
    conn.close()

# ------------------------------------------------------------------ #
#  Process batch                                                      #
# ------------------------------------------------------------------ #
def process_batch(db_path):
    print("🔌 Connecting to database...")
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")  # ✅ wait 5s if DB is locked
    print("✅ Connected!")

    cursor = conn.execute("""
        SELECT rowid, storyline FROM movies
        WHERE emotion IS NULL 
           OR emotion = 'processing'
           OR TRIM(emotion) = ''
    """)
    print("✅ Query executed!")

    # ✅ count pending rows upfront
    total_pending = conn.execute("""
        SELECT COUNT(*) FROM movies
        WHERE emotion IS NULL 
           OR emotion = 'processing'
           OR TRIM(emotion) = ''
    """).fetchone()[0]
    print(f"📦 Total pending rows: {total_pending}")

    saved  = 0
    failed = 0

    while True:
        row = cursor.fetchone()
        if row is None:
            break

        rowid, storyline = row
        print(f"🔄 Processing rowid {rowid} | {storyline[:50]}...")

        try:
            api_key = next(key_pool)
            result  = get_emotions_from_storyline(storyline, api_key)

            emotion = ", ".join(result['emotions'])
            reason  = result['reason']

            # ✅ print what was saved
            print(f"  ✅ rowid {rowid} → {emotion}")

            conn.execute("""
                UPDATE movies SET emotion = ?, reason = ?
                WHERE rowid = ?
            """, (emotion, reason, rowid))
            conn.commit()

            saved += 1
            if saved % 100 == 0:
                print(f"\n📊 Progress: {saved} saved | {failed} failed | {total_pending - saved} remaining\n")

            time.sleep(SLEEP_TIME)

        except Exception as e:
            if "429" in str(e) or "rate_limit" in str(e).lower():
                print(f"\n🛑 Daily limit hit after {saved} rows — run again tomorrow!")
                break
            else:
                print(f"  ❌ Failed rowid {rowid}: {e}")
                failed += 1
                time.sleep(2)
                continue

    conn.close()
    print(f"\n✅ Done — {saved} saved | {failed} failed")