import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.emotion_processor import setup_columns, process_batch

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'imdb_movies.db')

if __name__ == "__main__":
    print("Starting emotion extraction process...")
    setup_columns(db_path)
    process_batch(db_path)