import os
from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, field_validator

from database import init_db, get_connection
from seed_data import TIME_SLOTS
from ai_assistant import assistant
from auth_utils import hash_password, verify_password, new_token

app = FastAPI(title="Meridian Library API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")


# ---------- startup ----------

@app.on_event("startup")
def on_startup():
    init_db()
    conn = get_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    assistant.fit(books)
    conn.close()


# ---------- schemas ----------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError("Name is required.")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v


class BookingRequest(BaseModel):
    room_id: int
    date: str
    time: str
    guest_name: Optional[str] = None


# ---------- auth dependency ----------

def _member_from_token(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.removeprefix("Bearer ").strip()
    conn = get_connection()
    row = conn.execute(
        "SELECT m.id, m.name, m.email, m.member_since FROM sessions s "
        "JOIN members m ON m.id = s.member_id WHERE s.token = ?",
        (token,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_optional_member(authorization: Optional[str] = Header(default=None)):
    """Used where a guest is allowed too (e.g. booking a room)."""
    return _member_from_token(authorization)


def require_member(authorization: Optional[str] = Header(default=None)):
    """Used where only a signed-in member may proceed."""
    member = _member_from_token(authorization)
    if not member:
        raise HTTPException(status_code=401, detail="Sign in required.")
    return member


# ---------- helpers ----------

def room_free_slots(conn, room_id: int, for_date: str):
    if for_date != date.today().isoformat():
        booked = set()
    else:
        rows = conn.execute(
            "SELECT booking_time FROM bookings WHERE room_id = ? AND booking_date = ?",
            (room_id, for_date),
        ).fetchall()
        booked = {r["booking_time"] for r in rows}
    return [{"time": t, "available": t not in booked} for t in TIME_SLOTS]


def award_stamp(conn, member_id: int, label: str):
    if not member_id:
        return
    conn.execute(
        "INSERT INTO stamps (member_id, label, earned_at) VALUES (?, ?, datetime('now'))",
        (member_id, label),
    )


# ---------- stats ----------

@app.get("/api/stats")
def get_stats():
    conn = get_connection()
    row = conn.execute("SELECT total_books, reading_rooms, members FROM library_stats WHERE id = 1").fetchone()
    conn.close()
    return dict(row)


# ---------- auth ----------

def _issue_session(conn, member_id: int) -> str:
    token = new_token()
    conn.execute(
        "INSERT INTO sessions (token, member_id, created_at) VALUES (?, ?, datetime('now'))",
        (token, member_id),
    )
    conn.commit()
    return token


@app.post("/api/auth/login")
def login(payload: LoginRequest):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, name, email, member_since, password FROM members WHERE email = ?",
        (payload.email,),
    ).fetchone()
    if not row or not verify_password(payload.password, row["password"]):
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    token = _issue_session(conn, row["id"])
    conn.close()
    return {"id": row["id"], "name": row["name"], "email": row["email"], "member_since": row["member_since"], "token": token}


@app.post("/api/auth/register")
def register(payload: RegisterRequest):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM members WHERE email = ?", (payload.email,)).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=409, detail="An account with that email already exists.")
    cur = conn.execute(
        "INSERT INTO members (name, email, password, member_since) VALUES (?, ?, ?, date('now'))",
        (payload.name, payload.email, hash_password(payload.password)),
    )
    member_id = cur.lastrowid
    conn.commit()
    member = conn.execute(
        "SELECT id, name, email, member_since FROM members WHERE id = ?", (member_id,)
    ).fetchone()
    token = _issue_session(conn, member_id)
    conn.close()
    return {**dict(member), "token": token}


@app.post("/api/auth/guest")
def guest_login():
    return {"id": None, "name": "Guest", "email": None, "member_since": None, "guest": True}


# ---------- rooms ----------

@app.get("/api/rooms")
def list_rooms(for_date: str = Query(default_factory=lambda: date.today().isoformat())):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM rooms ORDER BY id").fetchall()
    result = []
    for r in rows:
        room = dict(r)
        slots = room_free_slots(conn, room["id"], for_date)
        room["free_slots"] = sum(1 for s in slots if s["available"]) if room["status"] == "Open" else 0
        result.append(room)
    conn.close()
    return result


@app.get("/api/rooms/{room_id}")
def get_room(room_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Room not found.")
    return dict(row)


@app.get("/api/rooms/{room_id}/slots")
def get_room_slots(room_id: int, for_date: str = Query(default_factory=lambda: date.today().isoformat())):
    conn = get_connection()
    room = conn.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
    if not room:
        conn.close()
        raise HTTPException(status_code=404, detail="Room not found.")
    if room["status"] != "Open":
        conn.close()
        return []
    slots = room_free_slots(conn, room_id, for_date)
    conn.close()
    return slots


# ---------- bookings ----------

@app.post("/api/bookings")
def create_booking(payload: BookingRequest, authorization: Optional[str] = Header(default=None)):
    member = get_optional_member(authorization)
    conn = get_connection()
    room = conn.execute("SELECT * FROM rooms WHERE id = ?", (payload.room_id,)).fetchone()
    if not room:
        conn.close()
        raise HTTPException(status_code=404, detail="Room not found.")
    if room["status"] != "Open":
        conn.close()
        raise HTTPException(status_code=400, detail="This room is currently closed.")
    if payload.time not in TIME_SLOTS:
        conn.close()
        raise HTTPException(status_code=400, detail="Not a valid time slot.")
    if not member and not (payload.guest_name and payload.guest_name.strip()):
        conn.close()
        raise HTTPException(status_code=400, detail="A name is required for a guest booking.")

    existing = conn.execute(
        "SELECT id FROM bookings WHERE room_id = ? AND booking_date = ? AND booking_time = ?",
        (payload.room_id, payload.date, payload.time),
    ).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=409, detail="That slot was just taken. Pick another time.")

    member_id = member["id"] if member else None
    cur = conn.execute(
        "INSERT INTO bookings (member_id, room_id, booking_date, booking_time, guest_name, created_at) "
        "VALUES (?, ?, ?, ?, ?, datetime('now'))",
        (member_id, payload.room_id, payload.date, payload.time, payload.guest_name),
    )
    booking_id = cur.lastrowid  # captured immediately, before any other INSERT can change it
    if member_id:
        award_stamp(conn, member_id, f"Booked {room['name']}")
    conn.commit()
    booking = conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
    conn.close()
    return dict(booking)


@app.get("/api/bookings")
def list_bookings(authorization: Optional[str] = Header(default=None)):
    member = require_member(authorization)
    conn = get_connection()
    rows = conn.execute(
        "SELECT b.*, r.name AS room_name FROM bookings b "
        "JOIN rooms r ON r.id = b.room_id "
        "WHERE b.member_id = ? ORDER BY b.booking_date, b.booking_time",
        (member["id"],),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.delete("/api/bookings/{booking_id}")
def cancel_booking(booking_id: int, authorization: Optional[str] = Header(default=None)):
    member = require_member(authorization)
    conn = get_connection()
    row = conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Booking not found.")
    if row["member_id"] != member["id"]:
        conn.close()
        raise HTTPException(status_code=403, detail="That booking doesn't belong to you.")
    conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
    return {"cancelled": True}


# ---------- catalogue ----------

@app.get("/api/catalogue")
def search_catalogue(q: Optional[str] = None, genre: Optional[str] = None, status: Optional[str] = None):
    conn = get_connection()
    sql = "SELECT * FROM books WHERE 1=1"
    params = []
    if q:
        sql += " AND (title LIKE ? OR author LIKE ? OR call_no LIKE ?)"
        like = f"%{q}%"
        params += [like, like, like]
    if genre and genre != "All Genres":
        sql += " AND genre = ?"
        params.append(genre)
    if status and status != "All":
        sql += " AND status = ?"
        params.append(status)
    sql += " ORDER BY title"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/genres")
def list_genres():
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT genre FROM books ORDER BY genre").fetchall()
    conn.close()
    return [r["genre"] for r in rows]


@app.get("/api/assistant/search")
def assistant_search(q: str, top_k: int = 5):
    results = assistant.search(q, top_k=top_k)
    return {"query": q, "results": results}


# ---------- events ----------

@app.get("/api/events")
def list_events():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM events ORDER BY event_date, event_time").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/api/events/{event_id}/register")
def register_event(event_id: int, authorization: Optional[str] = Header(default=None)):
    member = require_member(authorization)
    conn = get_connection()
    event = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    if not event:
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found.")
    if event["registered_count"] >= event["capacity"]:
        conn.close()
        raise HTTPException(status_code=400, detail="This event is full.")

    existing = conn.execute(
        "SELECT id FROM event_registrations WHERE event_id = ? AND member_id = ?",
        (event_id, member["id"]),
    ).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=409, detail="Already registered.")

    conn.execute(
        "INSERT INTO event_registrations (event_id, member_id) VALUES (?, ?)",
        (event_id, member["id"]),
    )
    conn.execute(
        "UPDATE events SET registered_count = registered_count + 1 WHERE id = ?",
        (event_id,),
    )
    award_stamp(conn, member["id"], f"Registered: {event['title']}")
    conn.commit()
    conn.close()
    return {"registered": True}


# ---------- members / account ----------

@app.get("/api/me")
def get_my_profile(authorization: Optional[str] = Header(default=None)):
    member = require_member(authorization)
    conn = get_connection()
    stamps = conn.execute(
        "SELECT * FROM stamps WHERE member_id = ? ORDER BY earned_at DESC", (member["id"],)
    ).fetchall()
    bookings = conn.execute(
        "SELECT COUNT(*) AS n FROM bookings WHERE member_id = ?", (member["id"],)
    ).fetchone()
    conn.close()
    data = dict(member)
    data["stamps"] = [dict(s) for s in stamps]
    data["stamps_count"] = len(stamps)
    data["bookings_count"] = bookings["n"]
    return data


@app.post("/api/auth/logout")
def logout(authorization: Optional[str] = Header(default=None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ").strip()
        conn = get_connection()
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
        conn.close()
    return {"signed_out": True}


# ---------- serve frontend ----------

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
