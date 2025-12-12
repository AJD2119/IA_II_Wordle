from utils import *

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

word_of_the_day: str = get_word_of_the_day()


@app.get("/")
def read_root():
    return {"ping": "Pong!"}


@app.get("/answer")
def read_root():
    return {"word": word_of_the_day}


@app.post("/{word}")
def send_guess_word(word: str):
    guess_word = word.upper()
    if guess_word == word_of_the_day:
        return {
            "guess": guess_word,
            "is_correct": True,
            "is_word_in_list": True,
        }

    # Check if the word in the word list
    word_list = get_word_list()
    if not guess_word.lower() in word_list:
        return {
            "guess": guess_word,
            "is_correct": False,
            "is_word_in_list": False,
        }

    # Check the word against the answer
    guess_result = []
    # Calculate guess_word
    for idx, char in enumerate(guess_word):
        guess_result.append(check_character(char, word_of_the_day, idx))
    return {
        "guess": guess_word,
        "is_correct": False,
        "is_word_in_list": True,
        "character_info": guess_result,
    }


if __name__ == '__main__':
    # uvicorn main:app --reload --port 8000
    uvicorn.run("main:app", port=8000, reload=True)

