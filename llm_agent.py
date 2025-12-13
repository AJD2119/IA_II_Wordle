# llm_agent.py
import os

# ✅ Importer la clé depuis config.py
try:
    from config import GEMINI_API_KEY
except ImportError:
    GEMINI_API_KEY = None
    print("⚠️ config.py not found or GEMINI_API_KEY not set.")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google.generativeai not installed, fallback to CSP")

# ---------- CSP helper ----------
def get_best_csp_suggestions(solver, k=5):
    """Récupère les meilleures suggestions du solver CSP."""
    return solver.suggest()[:k]

def choose_word(word: str):
    """Wrapper simple pour sélectionner un mot."""
    return {"chosen_word": word}

# ---------- Main LLM decision ----------
def llm_choose_next_guess(solver, previous_steps):
    """
    Sélectionne le prochain mot à deviner en utilisant Google Gemini.
    Si Gemini non disponible, retourne la suggestion CSP classique.
    """

    candidates = get_best_csp_suggestions(solver, k=5)

    if not candidates:
        return solver.suggest()[0]

    if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
        if not GEMINI_AVAILABLE:
            print("⚠️ Gemini API not available, using CSP fallback")
        if not GEMINI_API_KEY:
            print("⚠️ GEMINI_API_KEY not set in config.py, using CSP fallback")
        return candidates[0]

    try:
        # Configurer l'API Gemini avec la clé importée
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are a Wordle-solving agent.

Rules:
- You MUST choose exactly ONE word from the list below
- You are NOT allowed to invent a word
- Your goal is to minimize the expected number of remaining candidates

Previous guesses:
{previous_steps}

Remaining candidates: {len(solver.candidates)}

Candidate words:
{candidates}

Reply with ONLY the chosen word.
"""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.0,
                "max_output_tokens": 10
            }
        )

        chosen = response.text.strip().lower()

        # Vérification que le mot renvoyé est valide
        if chosen in candidates:
            return chosen

        print("⚠️ Gemini returned invalid word:", chosen)

    except Exception as e:
        print("⚠️ Gemini error, fallback to CSP:", e)

    # Fallback CSP
    return candidates[0]
