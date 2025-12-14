import google.generativeai as genai
from .base import BaseLLM

class GeminiLLM(BaseLLM):
    def __init__(self, model="gemini-1.5-flash"):
        self.model = model
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    def choose_next_guess(self, solver, steps):
        model = genai.GenerativeModel(self.model)

        prompt = f"""
Tu joues à Wordle.
Candidats possibles : {solver.candidates[:50]}
Donne UN mot de 5 lettres.
"""

        r = model.generate_content(prompt)
        return r.text.strip().lower()
