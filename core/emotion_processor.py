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
    os.getenv("GROQ_API_KEY_1"),
    os.getenv("GROQ_API_KEY_2"),
    os.getenv("GROQ_API_KEY_3"),
]
SLEEP_TIME = 2.0 / len(GROQ_KEYS)
key_pool   = cycle(GROQ_KEYS)

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
    print("✅ Connected!")

    cursor = conn.execute("""
        SELECT rowid, storyline FROM movies
        WHERE emotion IS NULL 
        OR emotion = 'processing'
        OR TRIM(emotion) = ''
    """)
    print("✅ Query executed!")

    saved  = 0
    failed = 0

    while True:
        row = cursor.fetchone()
        if row is None:
            break

        rowid, storyline = row
        print(f"🔄 Processing rowid {rowid}") 

        try:
            api_key = next(key_pool)
            result  = get_emotions_from_storyline(storyline, api_key)

            emotion = ", ".join(result['emotions'])
            reason  = result['reason']

            conn.execute("""
                UPDATE movies SET emotion = ?, reason = ?
                WHERE rowid = ?
            """, (emotion, reason, rowid))
            conn.commit() 

            saved += 1
            if saved % 100 == 0:
                print(f"  ✅ {saved} rows done...")

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