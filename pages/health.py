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



st.set_page_config(page_title="Entertainement", page_icon="🧰")
st.title("Check your health stats")
st.caption("Created by Muhammad Khan")




with st.container():
    st.header("📊 Life Stats Dashboard")
    st.caption("A tiny dashboard to see if you're actually surviving or just scrolling.")

    sleep_hours = st.slider("How many hours did you sleep last night?", 0, 12, 7, key="sleep")
    study_hours = st.slider("How many hours did you study/work today?", 0, 12, 2, key="study")
    screen_hours = st.slider("How many hours did you spend on screens today?", 0, 16, 6, key="screen")
    exercise_minutes = st.slider("How many minutes did you exercise today?", 0, 180, 20, key="exercise")

    st.subheader("Your Day in a Chart")

    stats_df = pd.DataFrame(
        {
            "Activity": [
                "Sleep (hrs)",
                "Study/Work (hrs)",
                "Screen Time (hrs)",
                "Exercise (hrs)",
            ],
            "Hours": [
                sleep_hours,
                study_hours,
                screen_hours,
                exercise_minutes / 60,
            ],
        }
    )

    st.dataframe(stats_df, hide_index=True)

    chart_df = stats_df.set_index("Activity")
    st.bar_chart(chart_df)

    score = 0

    if 7 <= sleep_hours <= 9:
        score += 30
    elif 5 <= sleep_hours < 7:
        score += 15

    if study_hours >= 3:
        score += 25
    elif study_hours >= 1:
        score += 10

    if screen_hours <= 4:
        score += 25
    elif screen_hours <= 7:
        score += 10
    elif screen_hours >= 8:
        score -= 15

    if exercise_minutes >= 45:
        score += 20
    elif exercise_minutes >= 15:
        score += 10

    st.subheader("🧬 Survival Score")
    st.progress(min(score, 100))
    st.write(f"Your survival score today: **{score}/100**")

    if score >= 75:
        st.success("You’re doing pretty well. Keep it up, main character energy ✅")
    elif score >= 50:
        st.warning("You’re surviving, but not thriving. Tweak one or two habits.")
    else:
        st.error("You’re speedrunning burnout. Touch grass, sleep, drink water 💀")


