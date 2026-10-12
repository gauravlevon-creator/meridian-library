import sqlite3
import os
from datetime import date, timedelta

from seed_data import (
    ROOMS, BOOKS, EVENTS, LIBRARY_STATS, DEMO_MEMBER,
    TIME_SLOTS, ROOM_PREBOOKED_COUNT,
)
from auth_utils import hash_password

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


SCHEMA = """
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    member_since TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    level INTEGER NOT NULL,
    capacity INTEGER NOT NULL,
    status TEXT NOT NULL,
    icon TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    room_id INTEGER NOT NULL,
    booking_date TEXT NOT NULL,
    booking_time TEXT NOT NULL,
    guest_name TEXT,
    created_at TEXT NOT NULL,
    UNIQUE(room_id, booking_date, booking_time),
    FOREIGN KEY(room_id) REFERENCES rooms(id)
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    call_no TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL,
    genre TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL,
    due_date TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    member_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(member_id) REFERENCES members(id)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    event_date TEXT NOT NULL,
    event_time TEXT NOT NULL,
    type TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    registered_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS event_registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    UNIQUE(event_id, member_id),
    FOREIGN KEY(event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS stamps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    earned_at TEXT NOT NULL,
    FOREIGN KEY(member_id) REFERENCES members(id)
);

CREATE TABLE IF NOT EXISTS library_stats (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    total_books INTEGER NOT NULL,
    reading_rooms INTEGER NOT NULL,
    members INTEGER NOT NULL
);
"""


def init_db(reset: bool = False):
    if reset and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    first_time = not os.path.exists(DB_PATH)
    conn = get_connection()
    conn.executescript(SCHEMA)

    if first_time:
        seed(conn)

    conn.commit()
    conn.close()


def seed(conn: sqlite3.Connection):
    cur = conn.cursor()

    # library-wide stats
    cur.execute(
        "INSERT INTO library_stats (id, total_books, reading_rooms, members) VALUES (1, ?, ?, ?)",
        (LIBRARY_STATS["total_books"], LIBRARY_STATS["reading_rooms"], LIBRARY_STATS["members"]),
    )

    # demo member (password hashed, never stored in plain text)
    cur.execute(
        "INSERT INTO members (name, email, password, member_since) VALUES (?, ?, ?, ?)",
        (DEMO_MEMBER["name"], DEMO_MEMBER["email"], hash_password(DEMO_MEMBER["password"]), DEMO_MEMBER["member_since"]),
    )
    demo_member_id = cur.lastrowid

    # rooms
    room_ids = {}
    for room in ROOMS:
        cur.execute(
            "INSERT INTO rooms (slug, name, category, description, level, capacity, status, icon) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (room["slug"], room["name"], room["category"], room["description"],
             room["level"], room["capacity"], room["status"], room["icon"]),
        )
        room_ids[room["slug"]] = cur.lastrowid

    # pre-book some slots today, for realism, so free-slot counts match the reference design
    today = date.today().isoformat()
    for slug, count in ROOM_PREBOOKED_COUNT.items():
        room_id = room_ids[slug]
        for t in TIME_SLOTS[:count]:
            cur.execute(
                "INSERT OR IGNORE INTO bookings (member_id, room_id, booking_date, booking_time, guest_name, created_at) "
                "VALUES (NULL, ?, ?, ?, 'Reserved', datetime('now'))",
                (room_id, today, t),
            )

    # books (a Borrowed book gets a realistic 14-day due date)
    for i, book in enumerate(BOOKS):
        due = (date.today() + timedelta(days=3 + (i % 12))).isoformat() if book["status"] == "Borrowed" else None
        cur.execute(
            "INSERT INTO books (call_no, title, author, year, genre, description, status, due_date) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (book["call_no"], book["title"], book["author"], book["year"],
             book["genre"], book["description"], book["status"], due),
        )

    # events
    for event in EVENTS:
        cur.execute(
            "INSERT INTO events (title, description, event_date, event_time, type, capacity, registered_count) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (event["title"], event["description"], event["date"], event["time"],
             event["type"], event["capacity"], event["registered_count"]),
        )

    # a few starter stamps for the demo member
    for label in ["First room booked", "Catalogue explorer", "Event registered"]:
        cur.execute(
            "INSERT INTO stamps (member_id, label, earned_at) VALUES (?, ?, datetime('now'))",
            (demo_member_id, label),
        )
