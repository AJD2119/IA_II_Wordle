from openai import OpenAI
from .base import BaseLLM

class OpenAILLM(BaseLLM):
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def choose_next_guess(self, solver, steps):
        candidates = solver.candidates[:50]

        prompt = f"""
Tu joues à Wordle.
Candidats possibles : {candidates}
Donne UN mot de 5 lettres.
Réponds uniquement par le mot.
"""

        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return r.choices[0].message.content.strip().lower()
