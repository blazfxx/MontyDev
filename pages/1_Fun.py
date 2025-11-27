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
        if st.button("Sign Out", key="signout_fun"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            safe_rerun()
            st.rerun()
    else:
        st.write("Created by **Muhammad Khan**")



st.set_page_config(page_title="Buisness", page_icon="🧰")
st.title("🧰 Serious Zone")
st.caption("Created by Muhammad Khan")
st.caption("THIS IS FOR FUN, DON'T TAKE IT SERIOUSLY")



tab1, tab2 = st.tabs([ "Reality Check", 'Excuse generator [to "save" your life]'])

with tab1:
    st.header("Can you sruvive any longer???")

    job_title = st.text_input("Whats ur job title?", placeholder="e.g., Software Engineer, Youtuber, Student, Vlogger, CEO")
    income = st.number_input("What's your income?", min_value=0, value=0)

    if st.button("Judge Me!"):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.005)
            progress.progress(i + 1)

        st.subheader("THE Verdict")

        job_lower = job_title.lower()
        
        if "dev" in job_lower or "programmer" in job_lower:
            st.error(f"Ah, a {job_title}. So you just copy-paste code all day and call it a job? Gotchu.")
        elif "youtuber" in job_lower or "vlogger" in job_lower:
            st.error(f"...{job_title}?! So you just beg for views and money? Dind't see that coming...")
        elif "ceo" in job_lower or "founder" in job_lower or "owner" in job_lower:
            st.error(f"A {job_title}? So you just exploit others for profit? Classic.")
        elif "engineer" in job_lower:
            st.error(f"{job_title}? So you just build things, but worse? Cool, cool")
        elif "student" in job_lower:
            st.error(f"You a {job_title}??? Brother, just drop out already and save us both the trouble.")
        elif "teacher" in job_lower or "professor" in job_lower:
            st.error(f"A {job_title}? One of the only actual jobs in here 🤣.")
        elif "dad" in job_lower or "mom" in job_lower:
            st.error(f"{job_title}??? When did you come back 😳")
        elif "mom" in job_lower:
            st.error(f"Hey there")
        else:
            st.write(f"'{job_title}'??? Never heard of that before, prob cause my brain is cooked...")


        if income == 0:
            st.header("💀 BROKE.")
            st.info("Put the fries in the bag or smth man")
        elif income < 1000:
            st.header("📉 POVERTY LINE GAMING.")
            st.info("Bro... BRO, whats happening???")
        elif income < 3000:
            st.header("😐 MEH.")
            st.info("You can afford rent OR food. Pick one.")
        else:
            st.header("💰 You are fine.")
            st.info(":( Lucky you..."
            "Oh, yea, gimme ur money too while you're at it.")


with tab2:
    st.header("100% Perfect, Working Excuse Generator")
    st.caption("Are you sure you should use this tool to save yourself tho?")

    recipient = st.selectbox("Who do you need an excuse for?", ["Boss", "Teacher", "Parent", "Friend", "Coach", "Mom"])
    severty = st.slider("How bad is it?", 1, 10, 5, key="severity_slider")

    issue = [
    "the WiFi router",
    "the cloud server",
    "my pet",
    "my alarm clock",
    "the cell tower",
    "my laptop",
    "my car",
    "my phone",
    "the power in my area",
    "the heating system",
    "my apartment building",
    "my work PC",
    "the home security system",
    "my internet connection",
    "the elevators in my building"
    ]

    action = [
    "stopped working",
    "crashed unexpectedly",
    "shut down",
    "malfunctioned",
    "stopped responding",
    "had a critical error",
    "failed this morning",
    "went offline",
    "locked me out",
    "started rebooting on its own",
    "lost connection",
    "required immediate troubleshooting",
    "had a system fault",
    "is under maintenance",
    "is being inspected"
    ]

    consequence = [
    "so I'm handling it right now",
    "so I might be delayed",
    "so I need some extra time",
    "so I can't step away yet",
    "so I'm waiting for support to respond",
    "so I need to resolve this first",
    "so I'm stuck for the moment",
    "so I'm trying to get everything back online",
    "so I may need to reschedule",
    "so I have to stay here until it’s fixed",
    "so I'm running diagnostics right now",
    "so I need to sort this out before I leave",
    "so I'm working on getting access again",
    "so I’m dealing with the situation on priority",
    "so I’ll update you as soon as it’s stable again"
    ]

    techinal_issue = [
    "the electrical subsystem",
    "the processor’s thermal core",
    "the network transmission layer",
    "the internal voltage regulator",
    "the quantum-level charge distribution",
    "the system’s main capacitor bank",
    "the motherboard’s micro-circuits",
    "the data integrity module",
    "the device’s magnetic field alignment",
    "the power-delivery pathway",
    "the computational cell structure",
    "the wireless signal lattice",
    "the hardware stability matrix",
    "the digital memory clusters",
    "the primary operational node"
    ]

    techinal_action = [
    "lost atomic stability",
    "dropped its electron flow unexpectedly",
    "fell out of thermal equilibrium",
    "entered a recursive fault state",
    "collapsed under voltage drift",
    "depolarized at the micro level",
    "stopped maintaining charge balance",
    "began oscillating outside safe thresholds",
    "failed to realign its magnetic pathways",
    "started looping during system excitation",
    "triggered a chain of integrity warnings",
    "went into uncontrolled energy dissipation",
    "lost synchronization with its core cycle",
    "began producing unstable charge gradients",
    "experienced molecular-level interference"
    ]

    techinal_consequence = [
    "so I have to stabilize the system before it causes further damage",
    "so I'm running emergency diagnostics to prevent data loss",
    "so I need time to safely discharge the affected components",
    "so the device is stuck in a recovery loop until I can intervene",
    "so I can't leave until the energy levels normalize",
    "so I have to isolate the fault to avoid a full system failure",
    "so I'm waiting for the system to re-establish charge balance",
    "so the hardware needs immediate recalibration",
    "so I need to send it in for controlled repair procedures",
    "so I'm manually restoring operational stability right now",
    "so the system is offline until the fault cycle breaks",
    "so I'm monitoring it closely before powering anything else up",
    "so I'm preventing a full shutdown by staying on-site",
    "so I have to bring it back into acceptable operating parameters",
    "so it’s unsafe to disconnect until the energy settles"
    ]


    techinal = st.checkbox("Make it more technical...")

    if st.button("Generate Excuse"):
        part1 = random.choice(issue)
        part2 = random.choice(action)
        part3 = random.choice(consequence)

        if severty > 8:
            st.error("🛑 This is serious. Use this:")
            excuse = f"EMERGENCY: {part1} {part2} dangerously. I am speaking to the FBI, the Police, AND the SWAT Team."
        elif techinal == False and recipient == "Mom":
            excuse = ("Nah bro, your cooked, we cant help. The slipper never misses its target...")
        elif techinal == True and recipient != "Mom":
            part1 = random.choice(techinal_issue)
            part2 = random.choice(techinal_action)
            part3 = random.choice(techinal_consequence)
            st.text("Here is your technical excuse:")
            excuse = f"I apologize, but unfortunately, {part1} {part2} {part3}"
        elif techinal == True and recipient == "Mom":
            excuse = ("Unfortunately, intervention is no longer possible — the kinetic-precision footwear delivery system of a mother has a 100% target-acquisition rate.")
        else:
            st.text("Here is your professional excuse:")
            excuse = f"I apologize, but unfortunately, {part1} {part2} {part3}"

        st.info(excuse)

        st.caption("Highlight the text, and either right-click and copy, or press Ctrl+C/Cmd+C to copy...")

    col1, col2 = st.columns(2)

    with col1:
        st.info("**LazyDev_99** ⭐⭐⭐⭐⭐\n\nUsed the 'WiFi' excuse. Boss bought it. I've been sleeping for 4 hours.")
        st.info("**Not_A_Robot** ⭐⭐⭐⭐⭐\n\nThis protocol is efficient for human deception.")

    with col2:
        st.info("**Elon M.** ⭐⭐⭐⭐⭐\n\nI should have used this instead of buying Twitter.")

    st.write("### 🗳️ Add your own Vouch")
    st.caption("We value your feedback (as long as it's good).")

    user_review = st.text_input("Type your review here:", placeholder="e.g. This app saved my life...")

    if st.button("Submit Review"):
        if user_review:
            st.balloons()
            
            st.success("✅ Review Submitted Successfully!")
            st.write("Your Review:")
            st.warning(f"**You** ⭐⭐⭐⭐⭐\n\n\"This is the greatest piece of software ever written. I will donate all my money to the creator.\"")
            st.caption("(Note: Our AI 'corrected' your review for clarity.)")
        else:
            st.error("You didn't type anything. Just like you didn't do your work.")



