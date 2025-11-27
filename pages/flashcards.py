import streamlit as st
from utils import safe_rerun
from database import add_flashcard, get_user_flashcards, delete_flashcard
import time

st.set_page_config(page_title="Flashcards", page_icon="🃏")
st.title("Flashcards")
st.caption("Create and manage your study flashcards")

st.session_state.setdefault('logged_in', False)
st.session_state.setdefault('username', None)
st.session_state.setdefault('is_student', False)
st.session_state.setdefault('is_adult', False)

with st.sidebar:
    st.info("Navigate using the menu above 👆")
    st.header("All-in-one Kit")
    st.session_state.setdefault('logged_in', False)
    st.session_state.setdefault('username', None)
    st.session_state.setdefault('is_student', False)
    st.session_state.setdefault('is_adult', False)
    if st.session_state.get('logged_in'):
        st.success(f"Signed in as {st.session_state.get('username')}")
        if st.button("Sign Out", key="signout_utils"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            safe_rerun()
            st.rerun()
    else:
        st.write("Created by **Muhammad Khan**")

if not st.session_state.get('logged_in') or not st.session_state.get('is_student'):
    st.warning("Flashcards are only available for students. Please sign in as a Student to use this page.")
else:
    tab1, tab2 = st.tabs(["Create flashcard", "My flashcards"])

    with tab1:
        st.header("Create a flashcard")
        q = st.text_input("Question", key='flash_q')
        a = st.text_area("Answer", key='flash_a')
        if st.button("Save flashcard"):
            if not q or not a:
                st.error("Both question and answer are required")
            else:
                ok = add_flashcard(st.session_state.get('username'), q, a, source='manual')
                if ok:
                    st.success("Saved flashcard")
                    safe_rerun()
                else:
                    st.error("Failed to save flashcard")
    with tab2:
        st.header("My flashcards")
        cards = get_user_flashcards(st.session_state.get('username'))
        if not cards:
            st.info("You have no flashcards yet. Create some above!")
        else:
            for c in cards:
                with st.expander(c['question']):
                    st.write(c['answer'])
                    if st.button("Delete", key=f"del_{c['id']}"):
                        if delete_flashcard(c['id'], st.session_state.get('username')):
                            st.success("Deleted flashcard")
                            safe_rerun()
                        else:
                            st.error("Failed to delete flashcard")
