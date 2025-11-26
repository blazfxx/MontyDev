import streamlit as st
from utils import safe_rerun
import random
import time
import pandas as pd
from ytmusicapi import YTMusic
from streamlit_chat_animated import message
from database import verify_user, username_available, update_username, update_password, update_profession, update_user_type

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



st.set_page_config(page_title="Settings", page_icon="⚙️")
st.title("Settinsg page ⚙️")
st.caption("Manage your account settings here.")






with st.container():
    if not st.session_state.get('logged_in'):
        st.warning("You must be signed in to manage your account. Go to Sign In/Up page.")
    else:
        st.subheader("Account Settings")
        st.markdown("Manage your username, password, and account type here.")
        current_username = st.session_state.get('username')
        current_profession = st.session_state.get('profession', '')

col1, col2 = st.columns(2)

with col1:
        # Change Username
        st.markdown("### Change Username")
        new_username = st.text_input("New username", value="", key="new_username_setting")
        confirm_password_for_username = st.text_input("Current password", type="password", key="curpwd_username_setting")
        if st.button("Change Username"):
            if not new_username:
                st.error("Please provide a new username.")
            elif not confirm_password_for_username:
                st.error("Please enter your current password for confirmation.")
            else:
                # Verify current password
                auth = verify_user(current_username, confirm_password_for_username)
                if not auth['verified']:
                    st.error("Current password is incorrect.")
                elif not username_available(new_username):
                    st.error("Username not available. Pick another.")
                else:
                    if update_username(current_username, new_username):
                        st.success("Username updated successfully.")
                        st.session_state['username'] = new_username
                        safe_rerun()
                    else:
                        st.error("Failed to update username. Try a different one.")

with col2:
        # Change Password
        st.markdown("### Change Password")
        cur_pwd = st.text_input("Current password", type="password", key="curpwd_setting")
        new_pwd = st.text_input("New password", type="password", key="newpwd_setting")
        confirm_new_pwd = st.text_input("Confirm new password", type="password", key="confirmnewpwd_setting")
        if st.button("Change Password"):
            if not cur_pwd or not new_pwd:
                st.error("Please fill out both current and new password fields.")
            elif new_pwd != confirm_new_pwd:
                st.error("New passwords do not match.")
            elif len(new_pwd) < 6:
                st.error("New password must be at least 6 characters long.")
            else:
                if update_password(current_username, cur_pwd, new_pwd):
                    st.success("Password updated successfully.")
                else:
                    st.error("Current password is incorrect or update failed.")

with st.container():
        # Change user type (Student/Adult)
        st.markdown("### User Type")
        current_type = "Student" if st.session_state.get('is_student') else ("Adult" if st.session_state.get('is_adult') else "Student")
        index = 0 if st.session_state.get('is_student') else (1 if st.session_state.get('is_adult') else 0)
        type_choice = st.selectbox("I am a:", options=["Student", "Adult"], index=index, key="type_choice_setting")
        confirm_password_type = st.text_input("Confirm current password", type="password", key="curpwd_type_setting")
        if st.button("Change User Type"):
            # Ensure user entered the current password for confirmation
            if not confirm_password_type:
                st.error("Please confirm your current password.")
            else:
                auth = verify_user(current_username, confirm_password_type)
                if not auth['verified']:
                    st.error("Current password is incorrect.")
                else:
                    is_student_flag = (type_choice == "Student")
                    is_adult_flag = (type_choice == "Adult")
                    if update_user_type(current_username, is_student_flag, is_adult_flag):
                        st.success("Updated user type successfully.")
                        st.session_state['is_student'] = is_student_flag
                        st.session_state['is_adult'] = is_adult_flag
                        safe_rerun()
                    else:
                        st.error("Failed to update user type. Try again.")

