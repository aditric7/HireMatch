
import os
import re
import hmac
import json
import sqlite3
import hashlib
import secrets

from pathlib import Path
from datetime import datetime, timezone


# --------------------------------------------------
# Database configuration
# --------------------------------------------------

DEFAULT_DB_PATH = Path(__file__).with_name("hirematch.db")
DB_PATH = Path(os.getenv("HIREMATCH_DB_PATH", str(DEFAULT_DB_PATH)))


def get_connection():
    """Open a database connection with foreign-key support."""
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    """Create database tables if they do not already exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                full_name TEXT NOT NULL,
                headline TEXT DEFAULT '',
                education TEXT DEFAULT '',
                target_role TEXT DEFAULT '',
                skills TEXT DEFAULT '',
                experience_level TEXT DEFAULT 'Student',
                bio TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                job_title TEXT NOT NULL,
                semantic_score REAL,
                ats_score INTEGER,
                matched_skills TEXT DEFAULT '[]',
                missing_skills TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_history_user_date
            ON analysis_history(user_id, created_at DESC)
        """)


# --------------------------------------------------
# Password security
# --------------------------------------------------

def hash_password(password, salt=None):
    """Hash a password using PBKDF2-HMAC-SHA256."""
    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310_000,
    )

    return salt.hex(), password_hash.hex()


def verify_password(password, salt_hex, expected_hash):
    """Check a password without comparing hashes insecurely."""
    try:
        salt = bytes.fromhex(salt_hex)
        _, actual_hash = hash_password(password, salt)

        return hmac.compare_digest(actual_hash, expected_hash)
    except (ValueError, TypeError):
        return False


# --------------------------------------------------
# Registration and login
# --------------------------------------------------

def create_user(email, password, full_name):
    email = (email or "").strip().lower()
    full_name = (full_name or "").strip()

    if not full_name:
        return False, "Please enter your full name."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Please enter a valid email address."

    if len(password or "") < 8:
        return False, "Your password must contain at least 8 characters."

    if len(password) > 1024:
        return False, "Password is too long."

    salt, password_hash = hash_password(password)

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (
                    email, password_hash, password_salt,
                    full_name, created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    email,
                    password_hash,
                    salt,
                    full_name,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

        return True, "Your account has been created."

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."


def authenticate_user(email, password):
    """Return safe user details when the credentials are valid."""
    email = (email or "").strip().lower()

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    if row is None:
        return None

    if not verify_password(
        password or "",
        row["password_salt"],
        row["password_hash"],
    ):
        return None

    return get_profile(row["id"])


# --------------------------------------------------
# Profile management
# --------------------------------------------------

def get_profile(user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, email, full_name, headline, education,
                   target_role, skills, experience_level, bio, created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    return dict(row) if row else None


def update_profile(
    user_id,
    full_name,
    headline,
    education,
    target_role,
    skills,
    experience_level,
    bio,
):
    full_name = (full_name or "").strip()

    if not full_name:
        return False, "Full name cannot be empty."

    if len(full_name) > 120:
        return False, "Full name is too long."

    fields = {
        "headline": (headline or "").strip(),
        "education": (education or "").strip(),
        "target_role": (target_role or "").strip(),
        "skills": (skills or "").strip(),
        "experience_level": (experience_level or "Student").strip(),
        "bio": (bio or "").strip(),
    }

    if any(len(value) > 3000 for value in fields.values()):
        return False, "One of your profile fields is too long."

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE users
            SET full_name = ?,
                headline = ?,
                education = ?,
                target_role = ?,
                skills = ?,
                experience_level = ?,
                bio = ?
            WHERE id = ?
            """,
            (
                full_name,
                fields["headline"],
                fields["education"],
                fields["target_role"],
                fields["skills"],
                fields["experience_level"],
                fields["bio"],
                user_id,
            ),
        )

    if cursor.rowcount == 0:
        return False, "Profile not found."

    return True, "Your profile has been updated."


# --------------------------------------------------
# Analysis history
# --------------------------------------------------

def save_analysis(
    user_id,
    job_title,
    semantic_score,
    ats_score,
    matched_skills,
    missing_skills,
):
    """Save scores and skill summaries, not the full resume."""
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO analysis_history (
                user_id, job_title, semantic_score, ats_score,
                matched_skills, missing_skills, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                (job_title or "Untitled role")[:200],
                semantic_score,
                ats_score,
                json.dumps(matched_skills or []),
                json.dumps(missing_skills or []),
                datetime.now(timezone.utc).isoformat(),
            ),
        )


def get_history(user_id, limit=30):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, job_title, semantic_score, ats_score,
                   matched_skills, missing_skills, created_at
            FROM analysis_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, max(1, min(int(limit), 100))),
        ).fetchall()

    history = []

    for row in rows:
        item = dict(row)

        for key in ("matched_skills", "missing_skills"):
            try:
                item[key] = json.loads(item[key] or "[]")
            except (ValueError, TypeError):
                item[key] = []

        history.append(item)

    return history
