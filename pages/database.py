
import sqlite3
import bcrypt

DATABASE_NAME = 'users.db'

def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            student BOOLEAN DEFAULT 0,
            adult BOOLEAN DEFAULT 0,
            profession TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'profession' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN profession TEXT DEFAULT ''")
    conn.commit()
    conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            source TEXT DEFAULT 'manual',
            created_at INTEGER DEFAULT (strftime('%s','now'))
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, email, password, student, adult, profession=''):
    password_bytes = password.encode('utf-8')
    hashed_psw = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashed_psw_str = hashed_psw.decode('utf-8')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password, student, adult, profession) VALUES (?, ?, ?, ?, ?, ?)', (username, email, hashed_psw_str, student, adult, profession))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT password, student, adult, profession FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        stored_hash = user_data[0].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return {
                "verified": True,
                "is_student": bool(user_data[1]),
                "is_adult": bool(user_data[2]),
                "profession": user_data[3] if len(user_data) > 3 else ''
            }
    
    return {"verified": False, "is_student": False, "is_adult": False}


def username_available(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    res = cursor.fetchone()
    conn.close()
    return not bool(res)


def update_username(old_username, new_username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, old_username))
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated
    except sqlite3.IntegrityError:
        return False


def update_password(username, current_password, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False
    if not bcrypt.checkpw(current_password.encode('utf-8'), row[0].encode('utf-8')):
        conn.close()
        return False
    new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_hash, username))
    conn.commit()
    conn.close()
    return True


def update_profession(username, profession):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET profession = ? WHERE username = ?', (profession, username))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def update_user_type(username, is_student, is_adult):
    """Set the user type flags for a given username.

    Accepts boolean flags for is_student and is_adult. Returns True if the
    update affected a row, False otherwise.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET student = ?, adult = ? WHERE username = ?', (int(bool(is_student)), int(bool(is_adult)), username))
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated
    except sqlite3.Error:
        return False


def add_flashcard(owner, question, answer, source='manual'):
    """Adds a new flashcard for a user."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO flashcards (owner, question, answer, source) VALUES (?, ?, ?, ?)', (owner, question, answer, source))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False


def get_user_flashcards(owner):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, question, answer, source, created_at FROM flashcards WHERE owner = ? ORDER BY created_at DESC', (owner,))
    rows = cursor.fetchall()
    conn.close()
    return [{'id': r[0], 'question': r[1], 'answer': r[2], 'source': r[3], 'created_at': r[4]} for r in rows]


def delete_flashcard(card_id, owner):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM flashcards WHERE id = ? AND owner = ?', (card_id, owner))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def init_finance_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_income (
            username TEXT PRIMARY KEY,
            monthly_income REAL DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            item TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def set_user_income(username, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO user_income (username, monthly_income) VALUES (?, ?)', (username, amount))
    conn.commit()
    conn.close()
    return True

def get_user_income(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT monthly_income FROM user_income WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0.0

def add_expense(username, category, item, amount, date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (username, category, item, amount, date) VALUES (?, ?, ?, ?, ?)', 
                   (username, category, item, amount, date))
    conn.commit()
    conn.close()
    return True

def get_user_expenses(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, category, item, amount, date FROM expenses WHERE username = ? ORDER BY date DESC', (username,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()