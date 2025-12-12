import subprocess
import sys
import os
import webbrowser
import time

# Chemin vers requirements.txt
requirements_path = os.path.join(os.getcwd(), "requirements.txt")

print("🔹 Installation des dépendances depuis requirements.txt...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

print("🔹 Lancement du projet Wordle complet...")

# Lancer l'API Wordle (FastAPI)
api_path = os.path.join("Api_wordle", "main.py")
fastapi_proc = subprocess.Popen([sys.executable, api_path])

# Lancer le solveur Flask (frontend)
solveur_path = os.path.join("Solveur_wordle", "server.py")
flask_proc = subprocess.Popen([sys.executable, solveur_path])

# Attendre que les serveurs démarrent
time.sleep(3)

# Ouvrir le frontend
frontend_path = os.path.join(os.getcwd(), "frontend", "index.html")
webbrowser.open(f"file://{frontend_path}")

print("✅ Le frontend devrait s'ouvrir dans le navigateur.")
print("💡 API Wordle: http://localhost:8000")
print("💡 Solveur Flask: http://localhost:5000/run")

# Garder les serveurs actifs
try:
    fastapi_proc.wait()
    flask_proc.wait()
except KeyboardInterrupt:
    print("\n❌ Arrêt des serveurs...")
    fastapi_proc.terminate()
    flask_proc.terminate()
