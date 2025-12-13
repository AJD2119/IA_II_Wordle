import subprocess
import sys
import os
import webbrowser
import time
import threading
import http.server
import socketserver

# =========================================================
# CONFIGURABLE PORTS
# =========================================================
API_PORT = 5000       # Port for FastAPI backend
FRONTEND_PORT = 8081  # Port for frontend HTTP server

ROOT_DIR = os.getcwd()

# ---------- Install dependencies ----------
requirements_path = os.path.join(ROOT_DIR, "requirements.txt")
print("🔹 Installing dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

print("🔹 Starting Wordle Solver project...")

# ---------- Start FastAPI backend ----------
fastapi_cmd = [
    sys.executable,
    "-m",
    "uvicorn",
    "Api_wordle.main:app",
    "--host", "127.0.0.1",
    "--port", str(API_PORT),
    "--reload"
]

fastapi_proc = subprocess.Popen(
    fastapi_cmd,
    cwd=ROOT_DIR
)

# ---------- Start Frontend HTTP server ----------
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

# ---------- Wait a few seconds for servers to start ----------
time.sleep(3)

# ---------- Open frontend in browser ----------
frontend_url = f"http://127.0.0.1:{FRONTEND_PORT}/"
webbrowser.open(frontend_url)

print("\n✅ Project running!")
print(f"🌐 Frontend: {frontend_url}")
print(f"🚀 API: http://127.0.0.1:{API_PORT}")
print("🛑 Press CTRL+C to stop\n")

# ---------- Keep script alive ----------
try:
    fastapi_proc.wait()
except KeyboardInterrupt:
    print("\n❌ Shutting down...")
    fastapi_proc.terminate()
