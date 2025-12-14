import subprocess
import sys
import os
import webbrowser
import time
import threading
import http.server
import socketserver
import socket

# =========================================================
# Fonction pour trouver un port libre
# =========================================================
def find_free_port(start=5000, end=5100):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("Aucun port libre trouvé")

# =========================================================
# CONFIGURABLE PORTS
# =========================================================
API_PORT = find_free_port(5000, 5100)       # Port for FastAPI backend
FRONTEND_PORT = find_free_port(8080, 8100)  # Port for frontend HTTP server
ROOT_DIR = os.getcwd()

# =========================================================
# CONFIG LLM
# =========================================================
CHOSEN_LLM = "gemini"  # "heuristic" / "ollama" / "gemini" / "openai"

# =========================================================
# Install dependencies
# =========================================================
requirements_path = os.path.join(ROOT_DIR, "requirements.txt")
print("🔹 Installing dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

print("🔹 Starting Wordle Solver project...")

# =========================================================
# Génère un fichier config.js pour le front avec le port backend
# =========================================================
config_js_path = os.path.join(ROOT_DIR, "frontend", "config.js")
with open(config_js_path, "w") as f:
    f.write(f"const API_HOST = 'http://127.0.0.1:{API_PORT}';\n")

# =========================================================
# Start FastAPI backend
# =========================================================
fastapi_cmd = [
    sys.executable,
    "-m",
    "uvicorn",
    "Api_wordle.main:app",
    "--host", "127.0.0.1",
    "--port", str(API_PORT),
    # "--reload"  # Décommente si tu veux rechargement auto
]

env = os.environ.copy()
env["CHOSEN_LLM"] = CHOSEN_LLM

fastapi_proc = subprocess.Popen(
    fastapi_cmd, cwd=ROOT_DIR,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    env=env
)

# =========================================================
# Thread to print backend logs in real time
# =========================================================
def print_backend_logs(proc):
    for line in proc.stdout:
        print(line, end="")

threading.Thread(target=print_backend_logs, args=(fastapi_proc,), daemon=True).start()

# =========================================================
# Start Frontend HTTP server
# =========================================================
def serve_frontend():
    os.chdir(os.path.join(ROOT_DIR, "frontend"))

    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            # Redirect "/" to "/index.html"
            if self.path == "/":
                self.path = "/index.html"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    with socketserver.TCPServer(("", FRONTEND_PORT), MyHandler) as httpd:
        print(f"Frontend HTTP server running at http://127.0.0.1:{FRONTEND_PORT}")
        httpd.serve_forever()

threading.Thread(target=serve_frontend, daemon=True).start()

# =========================================================
# Wait a few seconds for servers to start
# =========================================================
time.sleep(3)

# =========================================================
# Open frontend in browser
# =========================================================
frontend_url = f"http://127.0.0.1:{FRONTEND_PORT}/"
webbrowser.open(frontend_url)

print("\n✅ Project running!")
print(f"🌐 Frontend: {frontend_url}")
print(f"🚀 API: http://127.0.0.1:{API_PORT}")
print("🛑 Press CTRL+C to stop\n")

# =========================================================
# Keep script alive
# =========================================================
try:
    fastapi_proc.wait()
except KeyboardInterrupt:
    print("\n❌ Shutting down...")
    fastapi_proc.terminate()
    fastapi_proc.wait()
