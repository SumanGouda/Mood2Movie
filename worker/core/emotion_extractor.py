from groq import Groq
import json
from dotenv import load_dotenv
import os

load_dotenv()


EMOTIONS = [
    # Painful / Heavy
    "heartbroken", "grieving", "lonely", "empty", "hopeless",
    "devastated", "ashamed", "guilty", "rejected", "abandoned",
    "betrayed", "humiliated",

    # Anxious / Overwhelmed
    "anxious", "burnt-out", "overwhelmed", "restless", "trapped",
    "lost", "confused", "powerless",

    # Angry / Frustrated
    "angry", "bitter", "resentful", "jealous", "vengeful",
    "frustrated", "misunderstood",

    # Searching / Transitional
    "directionless", "nostalgic", "homesick", "disconnected",
    "unfulfilled", "stuck", "yearning", "curious",

    # Hopeful / Rising
    "hopeful", "healing", "motivated", "determined", "courageous",
    "inspired", "rebuilding", "rediscovering",

    # Warm / Connected
    "loved", "grateful", "content", "sentimental", "playful",
    "joyful", "proud", "accepted",

    # Dark / Existential
    "numb", "existential", "disillusioned", "cynical",
    "isolated", "invisible", "miserable"
]

def get_emotions_from_storyline(storyline, api_key):
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an emotion analysis expert for a movie recommendation system. You only return valid JSON. No extra text, no markdown, no explanation outside the JSON."
            },
            {
                "role": "user",
                "content": f"""Given this movie storyline, identify 2-4 emotions a person should 
be feeling RIGHT NOW in their life to deeply connect with this movie.

You MUST choose ONLY from this exact list — do not use any other words:
{EMOTIONS}

Think about: what pain, mood, or life situation would make someone relate to this story?

Return ONLY a valid JSON object in this exact format:
{{"emotions": ["emotion1", "emotion2"], "reason": "one line explanation"}}

Storyline: {storyline}"""
            }
        ]
    )

    text = response.choices[0].message.content.strip()
    text = text.replace('```json', '').replace('```', '').strip()
    
    result    = json.loads(text)
     
    # Validate emotions against the predefined list
    valid     = [e for e in result['emotions'] if e in EMOTIONS]
    result['emotions'] = valid
    
    return result

