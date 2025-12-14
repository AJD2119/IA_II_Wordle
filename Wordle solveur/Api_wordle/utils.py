import random
import datetime
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORD_FILE = os.path.join(PROJECT_ROOT, "word_list.txt")

def get_word_of_the_day():
    """Return a deterministic word based on the current date."""
    with open(WORD_FILE, "r", encoding="utf-8") as f:
        words = [w.strip() for w in f if len(w.strip()) == 5]

    random.seed(int(datetime.datetime.now().strftime("%Y%m%d")))
    return random.choice(words).upper()

def get_word_list():
    """Return a sorted list of words from the local file."""
    with open(WORD_FILE, "r", encoding="utf-8") as f:
        return sorted(w.strip().lower() for w in f if len(w.strip()) == 5)

def get_random_word():
    """Return a random word from the list (for replay mode)."""
    return random.choice(get_word_list()).upper()

def check_character(guess_character, answer, idx):
    """Return feedback for a single character (green/yellow/gray)."""
    return {
        "char": guess_character,
        "scoring": {
            "in_word": guess_character in answer,
            "correct_idx": guess_character == answer[idx],
        },
    }
