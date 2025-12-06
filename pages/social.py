import streamlit as st
from utils import safe_rerun
import random
import time
import pandas as pd
from ytmusicapi import YTMusic
from streamlit_chat_animated import message

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
        st.write("The scoials realted pages where not built by me, I edited the databse to implement them, but the pages were built by AI")
        st.write("I was bored, so I decided to add this")
        st.write("But I did write everything, and dindt just copy paste...")



st.set_page_config(page_title="Socials", page_icon="🧑‍🧑‍🧒‍🧒")
st.title("Connect, Share!")
st.subheader("Connect your social media accounts, and post to all of them in ONE click")
st.caption("Created by Muhammad Khan")




if "social_posts" not in st.session_state:
    st.session_state["social_posts"] = []

st.divider()
st.header("Create a new post")

if not st.session_state.get("logged_in"):
    st.info("Please sign in to create and share posts")
else:
    col1, col2 = st.columns([2,1])

    with col1:
        platforms = st.multiselect(" Where do you want to post?", ["Instagram", "TikTok", "YouTube Shorts", "YouTube", "X / Twitter", "Discord"], help="Later, a REAL API will be added")
        post_text = st.text_area("Post caption/text", placeholder="Write your caption here...", height=150,)
        video_file = st.file_uploader("Attack a video (optional)", type=["mp4", "mov", "webm", "mkv"], help="Short vertical videos will work best for TikTok, Reels, Shorts, etc.")
        post_button = st.button("Post to seletced platforms", type="primary")


    with col2:
        st.subheader("Preview")
        if video_file is not None:
            st.video(video_file)
        if post_text.strip():
            st.write("**Caption:**")
            st.write(post_text)
        if not post_text.strip() and video_file is None:
            st.caption("Your preview will be shown once you add text or a video")

        if post_button:
            if not platforms:
                st.error("Choose at least one platfrom")
            elif not post_text and video_file is None:
                st.error("Please add text or a video file")
            else:
                st.session_state["social_posts"].append({
                    "username": st.session_state.get("username"),
                    "platfroms": platforms,
                    "text": post_text,
                    "has_video": video_file is not None,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                })
                st.success("Post prepared (simulated)")

st.divider()
st.subheader("Recent Posts (Beta)")

if st.session_state["social_posts"]:
    df = pd.DataFrame(st.session_state["social_posts"])
    st.dataframe(df)
else:
    st.caption("Nothin to display yet 😴")