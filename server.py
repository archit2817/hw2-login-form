#!/usr/bin/env python3
"""Local login page with the same checks in the browser and on the server."""

import hashlib
import hmac
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
HOST = "127.0.0.1"
PORT = 8765

DEMO_EMAIL = "student@example.com"
DEMO_SALT = bytes.fromhex("614793cd6fec17794e833235b07518e8")
DEMO_HASH = bytes.fromhex(
    "acb0aa09ffd44ce85751e26ab2e94bd44fc78c8b38307a314c5d40354d6f1378"
)
HASH_ROUNDS = 200_000

FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
}


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, HASH_ROUNDS
    )


def validation_errors(email, password):
    errors = []
    if not email.strip() or not password:
        errors.append("Email and password are required.")
    if email.strip() and "@" not in email:
        errors.append("Email must contain @.")
    if password and len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    return errors


def credentials_match(email, password):
    candidate = hash_password(password, DEMO_SALT)
    email_ok = hmac.compare_digest(email.strip().lower(), DEMO_EMAIL)
    password_ok = hmac.compare_digest(candidate, DEMO_HASH)
    return email_ok and password_ok


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def _send(self, status, body, content_type):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, status, payload):
        self._send(status, json.dumps(payload), "application/json; charset=utf-8")

    def do_GET(self):
        item = FILES.get(self.path.split("?", 1)[0])
        if not item:
            self._send(404, "Not found", "text/plain; charset=utf-8")
            return
        name, content_type = item
        self._send(200, (STATIC / name).read_bytes(), content_type)

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/login":
            self._json(404, {"ok": False, "message": "Not found."})
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json(400, {"ok": False, "message": "Send a JSON email and password."})
            return

        email = payload.get("email", "")
        password = payload.get("password", "")
        if not isinstance(email, str) or not isinstance(password, str):
            self._json(400, {"ok": False, "message": "Email and password must be text."})
            return

        errors = validation_errors(email, password)
        if errors:
            self._json(400, {"ok": False, "message": " ".join(errors)})
            return

        if not credentials_match(email, password):
            self._json(401, {"ok": False, "message": "Invalid email or password."})
            return

        self._json(200, {"ok": True, "message": "Signed in."})


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Login form at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
