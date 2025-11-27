import streamlit as st
from transformers import pipeline
import torch
from database import save_summary, load_summaries, summary_db


summary_db()


st.set_page_config(page_title="AI Summarizer", page_icon="📝")

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
    
    st.divider()
    st.header("Technical Specs")
    st.info("Model: LaMini-Flan-T5-248M")


st.title("📝 AI Text Summarizer")
st.caption("Paste a long article below to get a quick summary.")

tab1, tab2 = st.tabs(["AI Text Summarizer", "Saved Summaries"])


with tab1:
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
                    
                    # GET RESULT
                    final_summary = response[0]['generated_text']

                    # CRITICAL FIX: Save to session state so we remember it
                    st.session_state['generated_summary'] = final_summary
                    st.session_state['original_text'] = text_input

                    st.subheader("Summary:")
                    st.success(final_summary)

                    # Metrics
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


            
        



with tab2:
    st.subheader("Saved Summaries")

    if st.session_state.get('logged_in'):
        username = st.session_state.get('username')
        rows = load_summaries(username)

        if rows:
            for row in rows:
                with st.expander(f"Summary from {row[2]}"):
                    st.write("**Original:**")
                    st.caption(row[0][:100] + "Read Rset?")
                    st.divider()
                    st.write("**Summary:**")
                    st.success(row[1])
        else:
            st.info("No saved summaries found.")
    else:
        st.warning("Login to view your saved summaries.")
