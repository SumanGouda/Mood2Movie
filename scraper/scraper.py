import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from emotion.emotion_extractor import get_emotions_from_storyline

print("Hello Neemo")