import streamlit as st
from utils import safe_rerun
import random
import time
import pandas as pd
from ytmusicapi import YTMusic

with st.sidebar:
    st.info("Navigate using the menu above 👆")
    st.header("All-in-one Kit")
    st.session_state.setdefault('logged_in', False)
    st.session_state.setdefault('username', None)
    st.session_state.setdefault('is_student', False)
    st.session_state.setdefault('is_adult', False)
    if st.session_state.get('logged_in'):
        st.success(f"Signed in as {st.session_state.get('username')}")
        if st.button("Sign Out", key="signout_music"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            safe_rerun()
            st.rerun()
    else:
        st.write("Created by **Muhammad Khan**")


st.set_page_config(page_title="Music", page_icon="🎵")
st.title("Chill Zone 🎵")
st.caption("Created by Muhammad Khan")

with st.container():
    st.header("Listen to Music")
    st.subheader("To cope with reaility 🥀")
    st.caption("It is better to open this page on another tab to listen to muisc while using other features of the app :)")

    song_name = st.text_input("Enter a song name or artist:", placeholder="e.g., Imagine dragons, Mozart, FatRat, Believer, etc..")
    
    if song_name:
        yt = YTMusic()

        results = yt.search(song_name, filter="songs", limit=5)

        if len(results) > 0:
            top_song = results[0]
            video_id = top_song['videoId']
            title = top_song['title']
            artist = top_song['artists'][0]['name']

            st.video(f"https://www.youtube.com/watch?v={video_id}")
        else:
            st.error("Song not found... Try another name?")

