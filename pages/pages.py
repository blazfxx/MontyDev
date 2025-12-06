import streamlit as st
import random
import time
import pandas as pd
from ytmusicapi import YTMusic


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_student" not in st.session_state:
    st.session_state.is_student = False
if "is_adult" not in st.session_state:
    st.session_state.is_adult = False


login_page = st.Page("sign.py", title="Sign In/Up", icon="🪧")
home_page = st.Page("Home.py", title="Home", icon="🏠")

serious_page = st.Page("1_Fun.py", title="Serious Zone", icon="📊")
music_page = st.Page("2_Music.py", title="Music", icon="🎵")      
health_page = st.Page("health.py", title="Health", icon="💪")
flashcards_page = st.Page("flashcards.py", title="Flashcards", icon="🃏")

utils_page = st.Page("Utilities.py", title="Utilities", icon="🛠️")
other_page = st.Page("other.py", title="Other", icon="❓")
settings_page = st.Page("settings.py", title="Settings", icon="⚙️")

income_page = st.Page("income.py", title="Finance Tracker", icon="💸")

flashcardai_page = st.Page("flashcardai.py", title ="Flashcard AI", icon="🃏")
ai_page = st.Page("ai.py", title="AI Tools", icon="🧠")
financeai_page = st.Page("financeai.py", title="Finance AI", icon="📝")
codeeai_page = st.Page("codingai.py", title="Coding AI", icon="🤖")

socials_page = st.Page("social.py", title="Socials", icon="🧑‍🧑‍🧒‍🧒")


if st.session_state.logged_in == False:
    pg = st.navigation({
        "Main": [home_page, health_page, serious_page, music_page,],
        "Tools": [utils_page, other_page, ai_page, financeai_page],
        "Account": [login_page],
    })

elif st.session_state.is_student:
    pg = st.navigation({
        "Main": [home_page],
        "Default Pages": [health_page, serious_page,],
        "Cill": [music_page],
        "Study":[flashcards_page, ai_page, flashcardai_page],
        "Tools": [utils_page, other_page],
        "Account": [settings_page],
    })

elif st.session_state.is_adult:
    pg = st.navigation({
        "Main": [home_page],
        "Default Pages": [health_page, serious_page],
        "Work": [income_page, financeai_page],
        "Chill": [music_page],
        "Tools": [utils_page, other_page, ai_page, codeeai_page],
        "Account": [settings_page],
    })

elif st.session_state.is_buisness:
    pg = st.navigation({
        "Main": [home_page],
        "Default Pages": [health_page, serious_page],
        "Work": [income_page, financeai_page, socials_page],
        "Chill": [music_page],
        "Tools": [utils_page, other_page, ai_page, codeeai_page],
        "Account": [settings_page],
    })

else:
    pg = st.navigation([home_page, login_page])

pg.run()