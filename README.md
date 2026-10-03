# Login form

A small login page for a web security homework. It copies the idea of the OWASP Juice Shop login screen: an email field, a password field, and a log in button. The browser and the Python server both reject an empty form, an email with no `@`, and a password shorter than 8 characters.

The demo account is `student@example.com` / `password123`. The server stores that password as a PBKDF2-HMAC-SHA256 hash with a salt. It never writes the typed email or password into the HTML it sends back.

## Run

Python 3 is enough. No extra packages.

```bash
python3 server.py
```

Open http://127.0.0.1:8765
