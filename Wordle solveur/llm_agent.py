# llm_agent.py
import os
import logging
# Assurez-vous d'avoir installé google-generativeai : pip install google-generativeai

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ---------- API Google Gemini ----------
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    logging.info("google.generativeai available")
except ImportError:
    GEMINI_AVAILABLE = False
    logging.info("google.generativeai not installed, fallback to CSP")

# ✅ Importer la clé depuis config.py
try:
    from config import GEMINI_API_KEY
    logging.info("GEMINI_API_KEY loaded from config.py")
except ImportError:
    GEMINI_API_KEY = None
    logging.info("config.py not found or GEMINI_API_KEY not set.")

if GEMINI_AVAILABLE and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logging.info("Gemini API configured")

# ---------- CSP helper ----------
def get_best_csp_suggestions(solver, k=5):
    """Récupère les meilleures suggestions du solver CSP."""
    suggestions = solver.suggest()[:k]
    logging.info(f"CSP suggestions (top {k}): {suggestions}")
    return suggestions

def choose_word(word: str):
    """Wrapper simple pour sélectionner un mot."""
    return {"chosen_word": word}

# ---------- Main LLM decision ----------
def llm_choose_next_guess(solver, previous_steps):
    """
    Sélectionne le prochain mot à deviner en utilisant Google Gemini.
    Si Gemini non disponible, retourne la suggestion CSP classique.
    """

    logging.info("\n================ LLM DECISION STEP ================")

    candidates = get_best_csp_suggestions(solver, k=5)

    if not candidates:
        logging.info("No CSP candidates available, using solver default")
        return solver.suggest()[0]

    if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
        logging.info("CSP fallback triggered (API not available or configured)")
        logging.info(f"Chosen word (CSP): {candidates[0]}")
        return candidates[0]

    try:
        logging.info("Calling Gemini LLM...")

        prompt = f"""
You are a Wordle-solving agent.

Rules:
- Choose exactly ONE word from the list below
- Do NOT invent a word
- Minimize expected number of remaining candidates

Previous guesses:
{previous_steps}

Remaining candidates: {len(solver.candidates)}

Candidate words:
{candidates}

Reply with ONLY the chosen word.
"""

        # Instanciation du modèle (correction pour ancienne API)
        model = genai.GenerativeModel("gemini-2.5-flash")

        # CORRECTION DÉFINITIVE : Appel minimaliste (uniquement le prompt)
        response = model.generate_content(prompt)

        # Accès au résultat via .text (correction pour ancienne API)
        chosen = response.text.strip().lower()

        logging.info(f"Gemini raw response: '{chosen}'")

        if chosen in candidates:
            logging.info(f"Gemini choice accepted: {chosen}")
            return chosen

        logging.info(f"Gemini returned invalid word: '{chosen}', fallback to CSP")

    except Exception as e:
        logging.info(f"Gemini error, fallback to CSP: {e}")

    # Fallback CSP
    logging.info(f"Chosen word (CSP fallback): {candidates[0]}")
    return candidates[0]