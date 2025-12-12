import random
import datetime
import os


def get_word_of_the_day():
    # Get maximum lines
    # TODO: https://stackoverflow.com/questions/32607370/python-how-to-get-the-number-of-lines-in-a-text-file
    with open(os.path.join(os.path.dirname(__file__), "word_list.txt"), "r") as f:
        words = f.readlines()
        file_length = len(words) - 1
        random.seed(int(datetime.datetime.now().strftime("%Y%m%d")))
        return words[random.randint(1 if words[0].startswith("#") else 0, file_length)].strip().upper()


def get_word_list():
    with open(os.path.join(os.path.dirname(__file__), "word_list.txt"), "r") as f:
        return sorted(f.read().split("\n")[1:])


def check_character(guess_character, answer, idx):
    return {
        "char": guess_character,
        "scoring": {
            "in_word": guess_character in answer,
            "correct_idx": guess_character == answer[idx]
        }
    }
