import streamlit as st
from transformers import pipeline
import torch
import ollama
import numpy as np
import pandas as pd

st.set_page_config(page_title="coding AI", page_icon="🧠")

with st.sidebar:
    st.header("All-in-one Kit")
    st.session_state.setdefault('logged_in', False)
    st.session_state.setdefault('username', None)
    st.session_state.setdefault('is_student', False)
    st.session_state.setdefault('is_adult', False)
    
    if st.session_state.get('logged_in'):
        st.success(f"Signed in as {st.session_state.get('username')}")
        if st.button("Sign Out", key="signout_ai"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.rerun()
    else:
        st.write("Created by **Muhammad Khan**")
    



st.title("Coding AI")
st.caption("Helps you code :D")

tab1 = st.tabs(["Private AI"])

with st.container():
    st.subheader("Private Coding AI")
    st.caption("Your data with the chatbot won't be saved for your own privacy :D")
    

    client = ollama.Client()

    model = "blazfoxx-code"
    st.info("Current model: blazfoxx-code")

    if "messagescode" not in st.session_state:
        st.session_state.messagescode = []

    def stream_data():
        stream = client.generate(model=model, prompt=prompt, stream=True)
        for chunk in stream:
            yield chunk["response"]

    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messagescode:
            if message["content"]: 
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    if st.session_state.get('logged_in'):
        placeholder = f"Hey {st.session_state.get('username')}! What do you want to build now?"

    else:
        placeholder = " What do you want to build now?"

    if prompt := st.chat_input(placeholder):
        st.session_state.messagescode.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                    status = st.empty()
                    status.write("Thinking...")
                    response = st.write_stream(stream_data())
                    status.empty()        
        st.session_state.messagescode.append({"role": "assistant", "content": response})