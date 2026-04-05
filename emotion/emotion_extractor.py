from groq import Groq
import json
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_emotions_from_storyline(storyline):  
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
    You are an emotion analysis expert for a movie recommendation system.

    Given this movie storyline, identify 4-6 specific emotions a person should 
    be feeling RIGHT NOW in their life to deeply connect with this movie.

    Think about: what pain, mood, or life situation would make someone 
    relate to this story?

    Return ONLY a valid JSON object like this:
    {{"emotions": ["heartbroken", "lonely", "overwhelmed", "hopeful"], 
    "reason": "one line explanation"}}

    Be specific — avoid generic emotions like 'happy' or 'sad'.

    Storyline: {storyline}
    """
            }
        ]
    )
    text = response.choices[0].message.content.strip()
    text = text.replace('```json', '').replace('```', '')
    return json.loads(text)


# storyline = """
# This story based on the best selling novel by Terry McMillan follows the lives 
# of four African-American women as they try to deal with their very lives. 
# Friendship becomes the strongest bond between these women as men, careers, and 
# families take them in different directions. Often light-hearted this movie speaks 
# about some of the problems and struggles the modern women face in today's world.
# """

# result = get_emotions_from_storyline(storyline)

# print("🎭 Emotions:", result['emotions'])
# print("📝 Reason:", result['reason'])