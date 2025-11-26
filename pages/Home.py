import streamlit as st
from utils import safe_rerun
import random
import time
import pandas as pd
from ytmusicapi import YTMusic
from database import init_db, init_finance_db

import streamlit as st
import time

init_db()
init_finance_db()

st.session_state.setdefault('logged_in', False)
st.session_state.setdefault('username', None)
st.session_state.setdefault('is_student', False)
st.session_state.setdefault('is_adult', False)

with st.sidebar:
    st.info("Navigate using the menu above 👆")
    st.header("All-in-one Kit")
    if st.session_state.get('logged_in'):
        st.success(f"Signed in as {st.session_state.get('username')}")
        if st.button("Sign Out"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            safe_rerun()
            st.rerun()
    else:
        st.write("Created by **Muhammad Khan**")

st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .fade-in {
        animation: fadeIn 3s ease-in forwards;
    }
    </style>
""", unsafe_allow_html=True)


title_text = "All-in-one Kit"

title_placeholder = st.empty()

displayed_text = ""
for char in title_text:
    displayed_text += char
    title_placeholder.markdown(f"<h1 style='text-align: center; color: red'>{displayed_text}</h1>", unsafe_allow_html=True)
    time.sleep(0.09)





st.markdown('<h2 class="fade-in" style="text-align: center;">Main Dashboard</h2>', unsafe_allow_html=True)
st.markdown('<p class="fade-in" style="text-align: center;">"Live your life, it doesn\'t matter what others think..." - Someone</p>', unsafe_allow_html=True)

if st.session_state.get('logged_in'):
    st.markdown(
    f"<h5 class='fade-in' style='text-align: center;'>Welcome {st.session_state.get('username')}!</h5>", unsafe_allow_html=True)
else:
    st.markdown('<p class="fade-in" style="text-align: center;">Sign In/Sign Up to get access to a personal panel, wth more options for students/adults!</p>', unsafe_allow_html=True)



