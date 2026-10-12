# Meridian Library

A full-stack library management web app: room booking, a searchable catalogue
(with a lightweight local AI search), events, and member stamps — matching the
reference screens in the PDF.

## Stack

- **Backend**: Python, FastAPI, SQLite (no external services, no API keys needed)
- **Auth**: bcrypt-hashed passwords + server-issued bearer session tokens
  (see "Security" below) — not plaintext, not client-trusted IDs.
- **AI search**: a local TF‑IDF + cosine-similarity model (`backend/ai_assistant.py`)
  trained on the catalogue's own text, so natural-language queries like *"a book
  about building good habits"* surface *Atomic Habits* even without an exact
  keyword match. It's a genuine small ML model, runs instantly, and needs no
  internet connection or API key — see the note at the top of that file for how
  to swap in a hosted LLM later without changing the API or frontend.
- **Frontend**: plain HTML/CSS/vanilla JS single-page app (no build step), served
  by the same FastAPI process. Sessions persist in `localStorage`, so refreshing
  the page keeps you signed in.
- **Dataset**: `backend/seed_data.py` — 4 reading rooms, 76 books across 13
  genres, 5 upcoming events, and a demo member account. Book metadata was
  pulled from Open Library's public catalogue and cross-checked against
  standard bibliographic references (Open Library's crowd-sourced data had a
  handful of wrong publication years — e.g. it listed *Macbeth* as 1508 — which
  were corrected by hand rather than carried over). All seeded into SQLite on
  first run.

## Run it

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000**.

Demo sign-in: `gaurav@gmail.com` / `demo1234` — or use "Browse as Guest".

The database (`backend/library.db`) is created and seeded automatically the
first time the server starts. Delete that file to reset all data.

## What's implemented

- **Sign in / Register / Guest** — real accounts in SQLite, bcrypt-hashed
  passwords, token-based sessions. Guest mode skips stamps and bookings.
- **Home dashboard** — greeting, live stats, six quick-action cards.
- **Rooms** — all 4 rooms with live open/closed status and free-slot counts.
- **Book a Slot** — 3-step wizard (room → time → details), hourly slots 9am–7pm,
  already-booked slots are greyed out and disabled, booking conflicts are
  rejected server-side, and a booking can only be cancelled by the member who
  made it.
- **Catalogue** — search by title/author/call number, filter by genre and
  status, due dates shown for borrowed titles, plus an "Ask the Librarian"
  toggle that switches to the local AI search.
- **Events** — register / full-capacity logic, earns a stamp.
- **My Stamps / Account** — bookings list (with cancel), stamp history.

## Security — what's now fixed vs. what's still demo-grade

**Fixed, and genuinely production-reasonable:**
- Passwords are bcrypt-hashed, never stored or compared in plain text.
- Login/register issue a random, server-side session token (`/api/auth/*`);
  every protected endpoint (bookings, events, account) requires it as
  `Authorization: Bearer <token>` and derives the member from it server-side —
  the client can no longer just claim to be `member_id=5`.
- A member can only cancel their *own* bookings (checked server-side, not just
  hidden in the UI).
- Register validates email format and a minimum password length.

**Still demo-grade — do these before a real public deployment:**
1. **Move off SQLite to Postgres** for concurrent multi-user traffic. The code
   is plain SQL (no ORM lock-in), so this is a connection-string-level change,
   not a rewrite.
2. **Real hosting**: HTTPS, a real domain, environment-based secrets (there
   currently isn't a secret to rotate since tokens are random and stored
   server-side, but a production deploy still wants proper env config, CORS
   locked to your real domain instead of `*`, etc.)
3. **Rate limiting / brute-force protection** on `/api/auth/login`.
4. **Token expiry** — sessions currently never expire; add a `created_at`
   check (the column already exists) and reject old tokens.
5. **Pagination** on `/api/catalogue` once the real catalogue is larger than a
   few hundred rows.
6. Real room photos instead of icon placeholders.

## API

All endpoints are under `/api` — see `backend/main.py`. Everything the
frontend does goes through this REST API, so you can drive it with `curl` or
build another frontend against it.
