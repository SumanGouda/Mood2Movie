import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import requests
from itertools import cycle
from dotenv import load_dotenv
from core.emotion_extractor import get_emotions_from_storyline
 
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

SERVER_URL = os.getenv("SERVER_URL")
API_SECRET = os.getenv("API_SECRET")
 
print(f"🌐 SERVER_URL : {SERVER_URL}")
print(f"🔑 API_SECRET : {API_SECRET[:6]}..." if API_SECRET else "❌ API_SECRET is None!")

GROQ_KEYS = [
    os.getenv("GROQ_API_KEY_1"),
    os.getenv("GROQ_API_KEY_2"),
    os.getenv("GROQ_API_KEY_3"),
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
key_pool   = cycle(GROQ_KEYS)

print(f"🔑 Loaded {len(GROQ_KEYS)} Groq keys | Sleep: {SLEEP_TIME:.2f}s")

HEADERS = {
    "X-API-Secret"              : API_SECRET,
    "ngrok-skip-browser-warning": "true",
    "User-Agent"                : "python-requests/2.31.0"
}

# ------------------------------------------------------------------ #
#  Worker loop                                                        #
# ------------------------------------------------------------------ #
def run_worker():
    print(f"\n🚀 Worker started — connecting to {SERVER_URL}")
    saved  = 0
    failed = 0

    while True:
        try:
            # Step 1 — get a row from server
            response = requests.get(f"{SERVER_URL}/get_row", headers=HEADERS)

            if response.status_code == 401:
                print("❌ Unauthorized — check your API_SECRET")
                break

            data = response.json()

            if data.get("done"):
                print("✅ All rows processed — nothing left to do!")
                break

            rowid     = data["rowid"]
            storyline = data["storyline"]
            print(f"🔄 Processing rowid {rowid} | {storyline[:50]}...")

            # Step 2 — process with Groq
            api_key = next(key_pool)
            result  = get_emotions_from_storyline(storyline, api_key)

            emotion = ", ".join(result["emotions"])
            reason  = result["reason"]

            # Step 3 — send result back to server
            save_response = requests.post(
                f"{SERVER_URL}/save_emotion",
                headers=HEADERS,
                json={"rowid": rowid, "emotion": emotion, "reason": reason}
            )

            if save_response.status_code == 200:
                print(f"  ✅ rowid {rowid} → {emotion}")
                saved += 1
            else:
                print(f"  ❌ Failed to save rowid {rowid} — response: {save_response.text}")
                failed += 1

            time.sleep(SLEEP_TIME)

        except Exception as e:
            if "429" in str(e) or "rate_limit" in str(e).lower():
                print(f"\n🛑 Groq daily limit hit after {saved} rows — run again tomorrow!")
                break
            else:
                print(f"  ❌ Error: {e}")
                failed += 1
                time.sleep(2)
                continue

    print(f"\n✅ Worker done — {saved} saved | {failed} failed")


if __name__ == "__main__":
    run_worker()