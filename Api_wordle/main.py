import sys
import os
from llm_agent import llm_choose_next_guess  # ✅ Ici, on importe notre agent LLM

# =========================================================
# Make project root importable
# =========================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# =========================================================
# Imports FastAPI
# =========================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 🔹 utils.py is in the same folder
from .utils import (
    get_word_of_the_day,
    get_word_list,
    check_character,
    get_random_word as get_random_word_util,
)

from Solveur_wordle.Solveur_Wordle import WordleSolver

# =========================================================
# App setup
# =========================================================
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# GLOBAL GAME STATE
# =========================================================
word_of_the_day: str = get_word_of_the_day().upper()
current_random_word: str | None = None
word_list = get_word_list()

# =========================================================
# ROOT
# =========================================================
@app.get("/")
def read_root():
    return {"ping": "Pong!"}

# =========================================================
# WORD OF THE DAY — GAME API
# =========================================================
@app.get("/word-of-the-day")
def get_word_of_the_day_endpoint():
    return {"word": word_of_the_day}


@app.post("/word-of-the-day/{word}")
def send_guess_word(word: str):
    guess_word = word.upper()

    if guess_word.lower() not in word_list:
        return {"guess": guess_word, "is_correct": False, "is_word_in_list": False}

    if guess_word == word_of_the_day:
        return {"guess": guess_word, "is_correct": True, "is_word_in_list": True}

    guess_result = [
        check_character(c, word_of_the_day, i)
        for i, c in enumerate(guess_word)
    ]

    return {
        "guess": guess_word,
        "is_correct": False,
        "is_word_in_list": True,
        "character_info": guess_result,
    }

# =========================================================
# RANDOM WORD — GAME API
# =========================================================
@app.get("/random-word")
def get_random_word_endpoint():
    global current_random_word
    current_random_word = get_random_word_util().upper()
    return {"word": current_random_word}


@app.post("/random-word/{word}")
def guess_random_word(word: str):
    global current_random_word

    if current_random_word is None:
        return {"error": "No random word generated. Call GET /random-word first."}

    guess_word = word.upper()

    if guess_word.lower() not in word_list:
        return {"guess": guess_word, "is_correct": False, "is_word_in_list": False}

    if guess_word == current_random_word:
        current_random_word = None
        return {"guess": guess_word, "is_correct": True, "is_word_in_list": True}

    guess_result = [
        check_character(c, current_random_word, i)
        for i, c in enumerate(guess_word)
    ]

    return {
        "guess": guess_word,
        "is_correct": False,
        "is_word_in_list": True,
        "character_info": guess_result,
    }

# =========================================================
# SOLVER — DAILY WORD (CSP + LLM)
# =========================================================
@app.get("/run-daily")
def run_solver_daily():
    solver = WordleSolver(word_list)
    guess = "crane"
    steps = []
    step = 1

    while True:
        response = send_guess_word(guess)

        if not response["is_word_in_list"]:
            break

        if response["is_correct"]:
            steps.append({"step": step, "guess": guess, "feedback": "GGGGG"})
            break

        feedback = "".join(
            "G" if c["scoring"]["correct_idx"]
            else "Y" if c["scoring"]["in_word"]
            else "B"
            for c in response["character_info"]
        )

        steps.append({"step": step, "guess": guess, "feedback": feedback})

        solver.apply_feedback(guess, feedback)

        # ✅ Ici on utilise l'agent LLM pour choisir le prochain mot
        guess = llm_choose_next_guess(solver, steps)

        step += 1

    return {"steps": steps}

# =========================================================
# SOLVER — RANDOM WORD (CSP + LLM)
# =========================================================
@app.get("/run-random")
def run_solver_random():
    global current_random_word

    if current_random_word is None:
        current_random_word = get_random_word_util().upper()

    solver = WordleSolver(word_list)
    guess = "crane"
    steps = []
    step = 1

    while True:
        response = guess_random_word(guess)

        if not response["is_word_in_list"]:
            break

        if response["is_correct"]:
            steps.append({"step": step, "guess": guess, "feedback": "GGGGG"})
            break

        feedback = "".join(
            "G" if c["scoring"]["correct_idx"]
            else "Y" if c["scoring"]["in_word"]
            else "B"
            for c in response["character_info"]
        )

        steps.append({"step": step, "guess": guess, "feedback": feedback})

        solver.apply_feedback(guess, feedback)

        # ✅ LLM next guess
        guess = llm_choose_next_guess(solver, steps)

        step += 1

    return {"steps": steps}

# =========================================================
# START SERVER
# =========================================================
if __name__ == "__main__":
    uvicorn.run(
        "Api_wordle.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
