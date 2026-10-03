# Login form

A small login page for a web security homework. It copies the idea of the
OWASP Juice Shop login screen: an email field, a password field, and a
Log in button. The same checks run in the browser and on the Python server.

## What it does

- Email and password fields with a Log in button.
- Rejects an empty email or password.
- Requires an `@` in the email.
- Requires a password of at least 8 characters.
- Runs these three checks in the browser (`static/app.js`) and again on the
  server (`server.py`), so they still apply if the browser is bypassed.

## Security

- The server builds no SQL and runs no database query, so there is nothing
  to inject. The email is compared as a plain string and the password as a
  hash.
- The demo password is stored as a PBKDF2-HMAC-SHA256 hash with a salt.
  Comparison uses `hmac.compare_digest`.
- Messages are written with `textContent`, not `innerHTML`, so a typed tag
  shows as text and does not run (XSS defense).
- Every response sends `Content-Security-Policy: default-src 'self'` and
  `X-Content-Type-Options: nosniff`.
- The reply is one fixed sentence and never repeats the typed email or
  password.

## Project structure
server.py # Python server + server-side validation
static/index.html # the page
static/app.js # client-side validation
static/style.css # styling


## Run

Python 3 is enough. No extra packages.

```bash
python3 server.py
```

Open http://127.0.0.1:8765

## Demo account

- Email: `student@example.com`
- Password: `password123`
