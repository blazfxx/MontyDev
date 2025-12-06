import streamlit as st
import ollama
import sqlite3
from database import get_db_connection, add_flashcard, get_user_flashcards
import datetime
import re



st.set_page_config(page_title="Flashcard AI", page_icon="📝")

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


st.title("Flashcard AI")
st.subheader(f"**Hey, {username}! By using this bot, you allow it to access this database**")


st.caption("Your data with the chatbot won't be saved for your own privacy.")
st.caption("This bot has access to your **Finance Database**, created at **Financial Tracker**, it can add data to it, but can't remove anything")



client = ollama.Client()
model = "blazfoxx-flashcard"
st.info("Current model: blazfoxx-flashcard")


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
        "what did flashcard did I make?",
        "help me study using",
        "use my",
        "use",
        "what flashcards did i make till now",
        "what flashcard did i make",
        "what flashcards did i make",
        "what flashcards did i make till now",
        "show my flashcards",
        "list my flashcards",
        "see my flashcards",
        "help me study using",
        "help me study my flashcards",
        "use my flashcards",
        "quiz me on my flashcards",
        "test me on my flashcards",
        "ask me questions from my flashcards",
    ]

    return any(phrase in q for phrase in db_keywords)


def add_database(question: str) -> bool:
    qu = question.lower()
    return "add" in qu

def yes(question: str) -> bool:
    que = question.lower()
    return "yes" in que

if "flashcard_messages" not in st.session_state:
    st.session_state.flashcard_messages = []

for message in st.session_state.flashcard_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.get('logged_in'):
    placeholder = f"Hey {st.session_state.get('username')}! what do you need help with today?"
else:
    st.warning("To use this feature, please log-in!")
    st.stop()

if user_question := st.chat_input(placeholder):
    st.session_state.flashcard_messages.append({"role": "user", "content": user_question})
    
    if "current_quiz_answer" in st.session_state:
        correct = st.session_state["current_quiz_answer"]
        user_ans = user_question.strip().lower()
        if user_ans == correct.lower():
            st.write("Correct! 🎉 Want another one?")
        else:
            st.write(f"Not quite. The correct answer was: **{correct}**")
        del st.session_state["current_quiz_answer"]
        st.stop()

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.write("Thinking...")
        
        username = st.session_state.get("username")
        q_lower = user_question.lower()
        date = datetime.datetime.now()



        use_database = bool(username) and needs_database(user_question)

        if use_database:
            status_placeholder.write("🔍 Checking your flashacrds")

            if "quiz" in q_lower or "test me" in q_lower or "ask me" in q_lower:
                user_cards = get_user_flashcards(username)
                if not user_cards:
                    st.write("You don't have any flashcards yet!")
                    st.stop()
                import random
                card = random.choice(user_cards)
                question_text = card["question"]
                answer_text = card["answer"]
                st.session_state["current_quiz_answer"] = answer_text
                st.write(f"**Question:**\n{question_text}\n\nType your answer:")
                st.stop()

            if "help me make better" in q_lower or "make better flashcards" in q_lower:
                get_user_flashcards()

                status_placeholder.write("Generating response...")

                def stream_response():
                    stream = client.generate(
                        model=model,
                        stream=True,
                        prompt=(
                            "You are an Ai that helps study\n"
                            f"The user asked: {user_question}\n\n"
                            "Here is their flaschards:\n"
                            f"{data}\n\n"
                            "Based on this, give **specific** advice:\n"
                            "help the user with his flashcards"
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
                        f"Available tables: get_user_flashcards(owner), "
                        f"flashcards(id, question, answer, source).\n"
                        """this is my sqlite thingy: def get_user_flashcards(owner):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, question, answer, source, created_at FROM flashcards WHERE owner = ? ORDER BY created_at DESC', (owner,))
    rows = cursor.fetchall()
    conn.close()
    return [{'id': r[0], 'question': r[1], 'answer': r[2], 'source': r[3], 'created_at': r[4]} for r in rows]"""
                        f"Filter only rows where username = '{username}'.\n\n"
                        f"RULES:\n"
                        f"- Output ONLY ONE SQL SELECT statement.\n"
                        f"- No explanations, no markdown, no comments.\n"
                        f"- First word MUST be SELECT.\n"
                        "DO NOT GIVE THE ANSWER"
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
                        "You are an Ai that helps study\n\n"
                        f"User question: {user_question}\n\n"
                        "Give clear, practical, short advice with their studying. "
                        "If the question is vague, give 2–3 simple suggestions.\n"
                        "assume they are middle/highschoolers"
                    )
                )
                for chunk in stream:
                    yield chunk["response"]
        status_placeholder.empty()
        response = st.write_stream(stream_response())
        st.session_state.flashcard_messages.append({"role": "assistant", "content": response})


#### memo for me: hwo does this work? -> we first connect to teh users database
# then, user asks prompt.
# ai checks if its a prompt about their databse or personal by checking the prompt, and comparing it to the given list
# the ai converst the SQLite data to SQL using hardcoded prompts
# then, when it gets teh answer, it sends it again to itself, and the user question, and uses that to answer the original question...</file>