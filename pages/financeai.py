import streamlit as st
import ollama
import sqlite3
from database import init_finance_db, get_user_income, get_user_expenses, get_db_connection, add_expense
import re
import datetime
init_finance_db()

st.set_page_config(page_title="Finance AI", page_icon="📝")

with st.sidebar:
    st.header("All-in-one Kit")
    st.session_state.setdefault('logged_in', False)
    st.session_state.setdefault('username', None)
    st.session_state.setdefault('is_student', False)
    st.session_state.setdefault('is_adult', False)
    st.session_state.setdefault('awaiting_approval', False)
    
    
    if st.session_state.get('logged_in'):
        st.success(f"Signed in as {st.session_state.get('username')}")
        if st.button("Sign Out", key="signout_ai"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.rerun()
    else:
        st.write("Created by **Muhammad Khan**")

username = st.session_state.get("username")


st.title("Finance AI")
st.subheader(f"**Hey, {username}! By using this bot, you allow it to access this database**")


st.caption("Your data with the chatbot won't be saved for your own privacy.")
st.caption("This bot has access to your **Finance Database**, created at **Financial Tracker**, it can add data to it, but can't remove anything")



client = ollama.Client()
model = "blazfoxx-financialhelper"
st.info("Current model: blazfoxx-financialhelper")


def fetch_db(sql: str):
    """Extract a SELECT statement from model output and run it safely."""
    match = re.search(r"(SELECT\s.+)", sql, re.IGNORECASE | re.DOTALL)
    if not match:
        return f"SQL ERROR: Could not find a SELECT query in: {sql}"

    real_sql = match.group(1).strip()

    sql_clean = real_sql.upper()
    if not sql_clean.startswith("SELECT"):
        return f"SQL ERROR: Only SELECT queries are allowed. Got: {real_sql}"

    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute(real_sql)
        rows = c.fetchall()
    except Exception as e:
        rows = f"SQL ERROR: {e}"
    conn.close()
    return rows



def needs_database(question: str) -> bool:
    q = question.lower()

    db_keywords = [
        "how much did i spend",
        "my expenses",
        "my spending",
        "what did i spend",
        "what is my income",
        "my income",
        "show my expenses",
        "where does my money go",
        "how can i save money",
        "how do i save money",
        "what should i stop spending my money on",
        "stop spending",
        "spend less",
    ]

    return any(phrase in q for phrase in db_keywords)


def add_database(question: str) -> bool:
    qu = question.lower()
    return "add" in qu

def yes(question: str) -> bool:
    que = question.lower()
    return "yes" in que

if "financial_messages" not in st.session_state:
    st.session_state.financial_messages = []

for message in st.session_state.financial_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.get('logged_in'):
    placeholder = f"Hey {st.session_state.get('username')}! what do you need help with today?"
else:
    st.warning("To use this feature, please log-in!")
    st.stop()

if user_question := st.chat_input(placeholder):
    st.session_state.financial_messages.append({"role": "user", "content": user_question})
    
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.write("Thinking...")
        
        username = st.session_state.get("username")
        q_lower = user_question.lower()
        date = datetime.datetime.now()

        if username and add_database(user_question):
            def stream_add():
                text_parts = []
                stream = client.generate(
                    model=model,
                    stream=True,
                    prompt=(
                        "The user wants to add something to their finance database.\n"
                        f"Username: {username}\n"
                        f"User message: {user_question}\n\n"
                        "Don’t write SQL. Just tell me the pieces: amount, category, date, note.\n"
                        "Return the answer in this exact format (one item per line):\n"
                        "for the category, return only one of these: Housing, Food, Transportation, Utilities, Insurance, Healthcare, Savings/Investing, Entertainment, Debt Payments\n"
                        "the capital letter is important, if the users category inst any of these, try to clasify their put the requested category under one of the ones we can use \n"
                        "amount: <number only>,\n"
                        "category: <one or more words>,\n"
                        "date: <YYYY-MM-DD>\n"
                        "note: <one word text about what they are adding/spending the money on, like robux>"
                        "if the user donest specify with enough info, please ask it for more details\n"
                        "ALWAYS ONE ITEM PER LINE\n"
                        f"If the user ask for today, use the first part of this: {date}\n"
                    )
                )
                for chunk in stream:
                    part = chunk["response"]
                    text_parts.append(part)
                    yield part
                response = "".join(text_parts).replace("*", " ").replace("_", " ").replace("$", "")
                st.session_state['info_to_add'] = response
            response = st.write_stream(stream_add())
            status_placeholder.empty()
            st.write("Confirm yes/no")
            st.session_state['awaiting_approval'] = True
            st.stop()
        
        
        if st.session_state['awaiting_approval'] == True:
            q_lower = user_question.lower()
            username = st.session_state.get("username")
            response = st.session_state.get('info_to_add', "")

            st.info("Awaiting = True")

            # Only handle the confirmation here; no DB insert yet.
            if "yes" in q_lower:
                st.info("found 'yes'")

                # 1) Split the previous AI output into comma-separated chunks
                parts = response.split(",")

                # 2) Build a dictionary like {"amount": "...", "category": "...", "date": "...", "note": "..."}
                parsed = {}
                for part in parts:
                    part = part.strip()
                    if not part:
                        # Skip empty strings
                        continue
                    if ":" not in part:
                        # Skip malformed pieces
                        continue

                    key, value = part.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip()
                    parsed[key] = value

                # 3) Pull out the formatted pieces
                amount_str = parsed.get("amount")
                category = parsed.get("category")
                date_str = parsed.get("date")
                note = parsed.get("note")

                # 4) Show what we parsed, so you can debug / use it later
                st.info(f"amount_str = {amount_str}")
                st.info(f"category   = {category}")
                st.info(f"date_str   = {date_str}")
                st.info(f"note       = {note}")

                # 5) At this point, you can later add your own DB insert logic using these variables.
                # For now, just exit confirmation mode so the app doesn't get stuck here.

                amount = float(amount_str)
                item = note

                add_expense(username, category, item, amount, date)

                st.session_state.pop('info_to_add', None)
                st.session_state['awaiting_approval'] = False
                st.stop()


        use_database = bool(username) and needs_database(user_question)

        if use_database:
            status_placeholder.write("🔍 Checking your financial data...")

            if "save money" in q_lower or "stop spending" in q_lower or "spend less" in q_lower:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT category, SUM(amount) AS total
                    FROM expenses
                    WHERE username = ?
                    GROUP BY category
                    ORDER BY total DESC
                    """,
                    (username,)
                )
                rows = cursor.fetchall()
                conn.close()

                sql_q = "MANUAL: category totals per user"
                data = rows

                with st.expander("Debug: SQL & Data"):
                    st.code(sql_q, language="sql")
                    st.write(data)

                status_placeholder.write("Generating response...")

                def stream_response():
                    stream = client.generate(
                        model=model,
                        stream=True,
                        prompt=(
                            "You are a personal finance coach.\n"
                            f"The user asked: {user_question}\n\n"
                            "Here is their spending by category (category, total_amount):\n"
                            f"{data}\n\n"
                            "Based on this, give **specific** advice:\n"
                            "- Point out the 2–3 biggest spending categories by name and amount.\n"
                            "- Suggest realistic ways to reduce those categories.\n"
                            "- Keep it short and use the numbers.\n"
                        )
                    )
                    for chunk in stream:
                        yield chunk["response"]

            else:
                sql_q = client.generate(
                    model=model,
                    prompt=(
                        f"You are a strict SQL generator.\n"
                        f"User question: {user_question}\n\n"
                        f"Available tables: user_income(username, monthly_income), "
                        f"expenses(id, username, category, item, amount, date).\n"
                        f"Filter only rows where username = '{username}'.\n\n"
                        f"RULES:\n"
                        f"- Output ONLY ONE SQL SELECT statement.\n"
                        f"- No explanations, no markdown, no comments.\n"
                        f"- First word MUST be SELECT.\n"
                    )
                )["response"].strip()

                sql_q = sql_q.replace("```sql", "").replace("```", "").strip()

                data = fetch_db(sql_q)

                with st.expander("Debug: SQL & Data"):
                    st.code(sql_q, language="sql")
                    st.write(data)

                status_placeholder.write("Generating response...")

                def stream_response():
                    stream = client.generate(
                        model=model,
                        stream=True,
                        prompt=(
                            f"User asked: {user_question}\n"
                            f"SQL query used: {sql_q}\n"
                            f"Database result: {data}\n\n"
                            "Answer the user's question using this data. "
                            "If there is an SQL error or no data, explain it kindly and suggest what they can do next."
                        )
                    )
                    for chunk in stream:
                        yield chunk["response"]

        else:
            status_placeholder.write("Thinking about your question...")

            def stream_response():
                stream = client.generate(
                    model=model,
                    stream=True,
                    prompt=(
                        "You are a helpful financial advisor.\n\n"
                        f"User question: {user_question}\n\n"
                        "Give clear, practical, short advice. "
                        "Assume all money is in US dollars. "
                        "If the question is vague, give 2–3 simple suggestions.\n"
                    )
                )
                for chunk in stream:
                    yield chunk["response"]
        status_placeholder.empty()
        response = st.write_stream(stream_response())
        st.session_state.financial_messages.append({"role": "assistant", "content": response})


#### memo for me: hwo does this work? -> we first connect to teh users database
# then, user asks prompt.
# ai checks if its a prompt about their databse or personal by checking the prompt, and comparing it to the given list
# the ai converst the SQLite data to SQL using hardcoded prompts
# then, when it gets teh answer, it sends it again to itself, and the user question, and uses that to answer the original question...