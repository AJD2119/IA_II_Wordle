from flask import Flask, jsonify
from flask_cors import CORS
from Solveur_Wordle import WordleSolver, load_wordlist, get_feedback_from_api

app = Flask(__name__)
CORS(app)


@app.route("/run", methods=["GET"])
def run_solver():
    wordlist = load_wordlist()
    solver = WordleSolver(wordlist)

    guess = "crane"
    steps = []

    step_number = 1
    while True:
        fb = get_feedback_from_api(guess)

        steps.append({
            "step": step_number,
            "guess": guess,
            "feedback": fb
        })

        if fb == "GGGGG":
            break

        solver.apply_feedback(guess, fb)
        suggestions = solver.suggest()
        guess = suggestions[0]
        step_number += 1

    return jsonify({"steps": steps})


if __name__ == "__main__":
    print("API running on http://localhost:5000")
    app.run(debug=True)
