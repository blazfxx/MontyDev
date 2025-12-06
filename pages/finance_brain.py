from database import get_db_connection, get_user_income

def get_total_spent(username: str) -> float:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(sum(amount), 0) FROM expenses WHERE username = ?", (username,))
    
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else 0.0

def get_total_last_30days(username: str) -> float:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(sum(amount), 0) FROM expenses WHERE username = ? AND date >= date('now' - '30 day')", (username,))
    row = cursor.fetchone()
    conn.close
    return row[0] if row and row[0] is not None else 0.0

def total_spent_by_cat(username: str) -> float:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) AS total FROM expenses WHERE username = ? GROUP by category ORDER by total DESC LIMIT ?", (username, limit))

def get_savings(username: str) -> float:
    conn = get_db_connection()
    cursor = conn.cursor()
    income = get_user_income(username)
    if income is None or income == 0:
        return None
    total_spent = get_total_spent(username)
    return(income - total_spent) / income

def rule_based_answer(question: str, username: str | None) -> str | None:
    if not username:
        return None
    question = question.lower().strip()

    if "how much" in question and "spend" in question and "sum" in question:
        total = get_total_spent(username)
        return f"You have spent **{total}** in total"
    
    if "how much" in question and "spend" in question and ("this month" in question or "last 30 days" in question):
        total_30 = get_total_last_30days
        return f"In the past 30 days, you have spent **{total_30}**"
    
    if "how much" in question and "spend" in question and "on" in question:
        try:
            category = q.split("on", 1)[1].strip().rstrip("?!. ")
            if category:
                cat_total = total_spent_by_cat(username, category)
                return f"You have spent **{cat_total}** on **{category}**"
        except:
            pass
    
    if ("what" in question or "how much" in question) and ("income" in question or "salary" in question):
        income = get_user_income(username)
        return f"You total monthly income is **{income}**"
    
    if "savings rate" in q or ("save" in q and "how" in q) or "is my spending" in q:
        rate = get_savings(username)

        if rate is None:
            return "I don't have your income saved, so I can't calculate your savings rate yet."

        percent = rate * 100

        # simple interpretation
        if percent < 0:
            msg = "You are spending more than you earn. This is risky."
        elif percent < 10:
            msg = "You are saving less than 10%. That's really low."
        elif percent < 20:
            msg = "You are saving between 10% and 20%. Goog, but it could be better."
        else:
            msg = "You are saving more than 20%. Nice!"

        return (
            f"Your estimated savings rate is **{percent:.1f}%**.\n\n"
            f"{msg}"
        )
    
    return None
    
    


# FROM AI:



from database import get_db_connection, get_user_income


# ============ LOW LEVEL HELPERS ============

def get_total_spent(username: str) -> float:
    """Total money spent by this user in ALL expenses."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else 0.0


def get_total_last_30_days(username: str) -> float:
    """Total spent in the last 30 days."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # NOTE: SQLite syntax: date('now','-30 day') NOT date('now' - '30 day')
    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE username = ?
          AND date >= date('now','-30 day')
        """,
        (username,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else 0.0


def get_total_spent_by_category(username: str, category: str) -> float:
    """Total spent for ONE category, e.g. 'food'."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE username = ?
          AND LOWER(category) = LOWER(?)
        """,
        (username, category)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else 0.0


def get_savings(username: str):
    """Savings rate = (income - total_spent) / income."""
    income = get_user_income(username)
    if income is None or income == 0:
        return None
    total_spent = get_total_spent(username)
    return (income - total_spent) / income


# ============ MAIN BRAIN FUNCTION ============

def rule_based_answer(question: str, username: str | None) -> str | None:
    """Return a text answer if we can, otherwise None."""
    if not username:
        return None

    q = question.lower().strip()

    # 1) "how much did i spend in total?"
    if "how much" in q and "spend" in q and "total" in q:
        total = get_total_spent(username)
        return f"You have spent **${total:.2f}** in total."

    # 2) "how much did i spend this month / last 30 days?"
    if "how much" in q and "spend" in q and ("this month" in q or "last 30 days" in q):
        total_30 = get_total_last_30_days(username)
        return f"In the past 30 days, you have spent **${total_30:.2f}**."

    # 3) "how much did i spend on food/games/etc?"
    if "how much" in q and "spend" in q and "on" in q:
        try:
            category = q.split("on", 1)[1].strip().rstrip("?!. ")
            if category:
                cat_total = get_total_spent_by_category(username, category)
                return f"You have spent **${cat_total:.2f}** on **{category}**."
        except Exception:
            pass

    # 4) "what is my income / salary?"
    if ("what" in q or "how much" in q) and ("income" in q or "salary" in q):
        income = get_user_income(username)
        return f"Your total monthly income is **${income:.2f}**."

    # 5) "what is my savings rate / is my spending healthy?"
    if "savings rate" in q or ("save" in q and "how" in q) or "is my spending" in q:
        rate = get_savings(username)
        if rate is None:
            return "I don't have your income saved, so I can't calculate your savings rate yet."

        percent = rate * 100
        if percent < 0:
            msg = "You are spending more than you earn. This is risky."
        elif percent < 10:
            msg = "You are saving less than 10%. That's really low."
        elif percent < 20:
            msg = "You are saving between 10% and 20%. Good, but it could be better."
        else:
            msg = "You are saving more than 20%. Nice!"

        return f"Your estimated savings rate is **{percent:.1f}%**.\n\n{msg}"

    # If no rule matched, return None so we can fall back to the LLM
    return None