import streamlit as st
from transformers import pipeline
import torch
from database import save_summary, load_summaries, summary_db
import ollama
import numpy as np
import pandas as pd
import time
from database import init_db
import sqlite3

summary_db()

st.set_page_config(page_title="AI Tools", page_icon="🤖")

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
    



st.title("AI Tools")
st.caption("Helpful AI tools :D")

tab1, tab2, tab3 = st.tabs(["Private AI", "AI Text Summarizer", "Saved Summaries"])

with tab1:
    st.subheader("Private AI")
    st.caption("Your data with the chatbot won't be saved for your own privacy :D")
    

    client = ollama.Client()
    
    think = st.checkbox("Think Longer", key="think")

    if think == True:
        model = "blazfoxx-plus"
        st.info("Current model: blazfoxx-plus")
    else:
        model = "blazfoxx"
        st.info("Current model: blazfoxx")

    st.caption("To switch to a **thinking model**, please scroll up and tick the checkbox!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def stream_data():
        stream = client.generate(model=model, prompt=prompt, stream=True)
        for chunk in stream:
            yield chunk["response"]

    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            if message["content"]: 
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    if st.session_state.get('logged_in'):
        placeholder = f"Hey {st.session_state.get('username')}! What's on your mind today?"
        if think == True:
            placeholder = f"Hey {st.session_state.get('username')}! Using 'Think Longer'? I'm warning you, this one thinks longer about EVERYTHING"
    else:
        placeholder = "What's on your mind?"
        if think == True:
            placeholder = f"Hey! Using 'Think Longer'? I'm warning you, this one thinks longer about EVERYTHING"

    if prompt := st.chat_input(placeholder):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                if think == True:
                    status = st.empty()
                    status.write("Thinking...")
                    response = st.write_stream(stream_data())
                    status.empty()
                else:
                    response = st.write_stream(stream_data())
        
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.subheader("AI Text Summarizer")
    @st.cache_resource
    def load_model():
        pipe = pipeline(
            "text2text-generation", 
            model="MBZUAI/LaMini-Flan-T5-248M", 
            torch_dtype=torch.float32
        )
        return pipe

    with st.spinner("Initializing Summarization Engine..."):
        ai_pipe = load_model()

    text_input = st.text_area("Enter Text to Summarize:", height=300)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Summarize Text"):
            if text_input:
                with st.spinner("Reading and Summarizing..."):
                    instruction = "Summarize this text: " + text_input
                    response = ai_pipe(instruction, max_length=512, min_length=50, do_sample=False)
                    
                    final_summary = response[0]['generated_text']

                    st.session_state['generated_summary'] = final_summary
                    st.session_state['original_text'] = text_input

                    st.subheader("Summary:")
                    st.success(final_summary)

                    orig_len = len(text_input.split())
                    new_len = len(final_summary.split())
                    reduction = 100 - ((new_len / orig_len) * 100) if orig_len > 0 else 0
                
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Original", orig_len)
                    m2.metric("Summary", new_len)
                    m3.metric("Reduction", f"{reduction:.1f}%")
            else:
                st.warning("Please enter some text first.")

    with col2:
        if st.session_state.get('logged_in'):
            if st.button("Save Summary", key="save_summary_btn"):
                username = st.session_state.get('username')
                if 'generated_summary' in st.session_state:
                    username = st.session_state.get('username')
                    orig = st.session_state.get('original_text')
                    summ = st.session_state.get('generated_summary')
                    save_summary(username, orig, summ)
                    st.success("✅ Summary saved to database!")
                else:
                    st.error("You need to generate a summary first!")
        else:
            st.markdown('<h5 style="text-align: right;">Log In to Save!</h5>', unsafe_allow_html=True)

with tab3:
    st.subheader("Saved Summaries")

    if st.session_state.get('logged_in'):
        username = st.session_state.get('username')
        rows = load_summaries(username)

        if rows:
            for row in rows:
                with st.expander(f"Summary from {row[2]}"):
                    st.write("**Original:**")
                    st.caption(row[0][:100] + "...")
                    st.divider()
                    st.write("**Summary:**")
                    st.success(row[1])
        else:
            st.info("No saved summaries found.")
    else:
        st.warning("Login to view your saved summaries.")