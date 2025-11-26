import streamlit as st
import random
import time
import pandas as pd
from ytmusicapi import YTMusic
from streamlit_chat_animated import message
from utils import safe_rerun


with st.sidebar:
    st.info("Navigate using the menu above 👆")
    st.header("All-in-one Kit")
    st.session_state.setdefault('logged_in', False)
    st.session_state.setdefault('username', None)
    st.session_state.setdefault('is_student', False)
    st.session_state.setdefault('is_adult', False)
    if st.session_state.get('logged_in'):
        st.success(f"Signed in as {st.session_state.get('username')}")
        if st.button("Sign Out", key="signout_health"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            safe_rerun()
            st.rerun()
    else:
        st.write("Created by **Muhammad Khan**")


st.set_page_config(page_title="Other", page_icon="❓")
st.title("Check out my apps :D")
st.caption("Created by Muhammad Khan")





with st.container():
    st.caption("blazfoxx/WitheredAI are my usernames")


    st.divider()
    coll, col2 = st.columns([1, 4])

    with coll:
        st.image("/Users/muhammadkhan/Desktop/ProjectOhioSgmaRizz/GAZE.png", width=200)
    with col2:
        st.subheader("GAZE")
        st.write("Monitors your desktop, when active, and lets you revisit moments from the past")
        st.write("**Version:** 1.0 | **Size:** 1.5 MB")
        st.link_button("Download GAZE", "https://drive.google.com/uc?export=download&id=1mvNyIc8TQHp3FyteYw-Ah07BRri_kje8")

    st.divider()
    coll, col2 = st.columns([1, 4])

    with coll:
        st.image("/Users/muhammadkhan/Desktop/ProjectOhioSgmaRizz/ZapRequestDarkMode-NoBG.png", width=200)
    with col2:
        st.subheader("ZapRequest")
        st.write("Lets you send, and recieve from APIs")
        st.write("**Version:** 1.0 | **Size:** 2.5 MB")
        st.link_button("Download ZapRequest", "https://drive.google.com/uc?export=download&id=1hIcdtY6I3t3DmNK22NhImDhvEgBRomt4")

    st.divider()
    coll, col2 = st.columns([1, 4])

    with coll:
        st.image("/Users/muhammadkhan/Desktop/ProjectOhioSgmaRizz/AmbientFocusNOBG.png", width = 200)
    with col2:
        st.subheader("Ambient Focus")
        st.write("Lets you mix ambient noises together to help you study!")
        st.write("**Version:** 1.0 | **Size:** 674.5 MB")
        st.link_button("Download Ambient Focus from google drive", "https://drive.google.com/uc?export=download&id=1a_TgqmuyQWQxh7VvX9La7aYpABG__E0s")