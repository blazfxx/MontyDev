import streamlit as st
from utils import safe_rerun
import random
import time
import pandas as pd
from ytmusicapi import YTMusic
from streamlit_chat_animated import message
import sqlite3
import bcrypt
from database import add_user, verify_user





st.set_page_config(page_title="Sign In/Up", page_icon="🪧")
st.markdown("<h1 style='text-align: center;'>Sign In/Sign Up!</h1>", unsafe_allow_html=True)   
st.markdown("<p style='text-align: center;'>Created by Muhammad Khan</p>", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    st.subheader("Sign In")
    st.text_input("Username", placeholder="Enter your username", key="username_signin")
    st.text_input("Password", type="password", placeholder="Enter your password", key="password_signin")
    
    # Ensure session defaults exist (won't overwrite existing state)
    st.session_state.setdefault('logged_in', False)
    st.session_state.setdefault('username', None)
    st.session_state.setdefault('is_student', False)
    st.session_state.setdefault('is_adult', False)
    
# In your main file (under the Sign In button)

    if st.button("Sign In", key="signin_btn"):
        username = st.session_state.username_signin
        password = st.session_state.password_signin

        # We catch the dictionary in a variable (I called it auth_result)
        auth_result = verify_user(username, password)

        # We check the 'verified' key inside that dictionary
        if auth_result['verified'] == True:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            
            # THIS IS THE MAGICAL PART
            # We save the type of user into the session state for later use
            st.session_state['is_student'] = auth_result['is_student']
            st.session_state['is_adult'] = auth_result['is_adult']
            st.session_state['profession'] = auth_result.get('profession', '')

            st.success(f"Welcome back, {username}!")
            st.balloons()
            st.write("You are now signed in. Refresh the page to access features.")
            safe_rerun()
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")

with col2:
    st.subheader("Sign Up")
    st.text_input("Email", placeholder="Enter your email", key="email_signup")
    st.text_input("Username", placeholder="Enter your username", key="username_signup")
    paswd1 = st.text_input("Password", type="password", placeholder="Enter your password", key="password_signup")
    paswd2 = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", key="confirm_password_signup")
    st.selectbox("I am a:", options=["Student", "Adult"], key="user_type_signup")

    if paswd1 != paswd2:
        st.error("Passwords dont match")
    elif len(paswd1) < 6 and paswd1 != "":
        st.error("Password must be at least 6 characters long")
    elif " " in st.session_state.username_signup:
        st.error("Username cannot contain spaces")
    elif " " in st.session_state.email_signup:
        st.error("Email cannot contain spaces")
    elif "@" not in st.session_state.email_signup and st.session_state.email_signup != "":
        st.error("Please enter a valid email address")
    elif paswd1 == "" or st.session_state.username_signup == "" or st.session_state.email_signup == "":
        st.error("All fields are required")        
    elif st.button("Sign Up", key="signup_btn"):
        new_email = st.session_state.email_signup
        new_username = st.session_state.username_signup
        user_type = st.session_state.user_type_signup
        is_student = user_type == "Student"
        is_adult = user_type == "Adult"

        if add_user(new_username, new_email, paswd1, is_student, is_adult, profession_input or ''):
            st.success("Account created successfully! You can now sign in.")
            st.balloons()
            st.session_state['logged_in'] = True
            st.session_state['username'] = new_username
            st.experimental_rerun()
            st.rerun()
        else:
            st.error("Username or email already exists. Please try again with different credentials.")


