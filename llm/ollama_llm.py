import requests
from .base import BaseLLM

class OllamaLLM(BaseLLM):
    def __init__(self, model="llama3"):
        self.model = model

    def choose_next_guess(self, solver, steps):
        prompt = f"""
Tu joues à Wordle.
Candidats possibles : {solver.candidates[:50]}
Donne UN mot de 5 lettres.
"""

        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        return r.json()["response"].strip().lower()
