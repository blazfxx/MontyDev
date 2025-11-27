import streamlit as st
from utils import safe_rerun
import random
import time
import pandas as pd
from ytmusicapi import YTMusic
from streamlit_chat_animated import message
import qrcode
import string
from io import BytesIO
from PIL import Image

with st.sidebar:
    st.info("Navigate using the menu above 👆")
    st.header("All-in-one Kit")
    st.session_state.setdefault('logged_in', False)
    st.session_state.setdefault('username', None)
    st.session_state.setdefault('is_student', False)
    st.session_state.setdefault('is_adult', False)
    if st.session_state.get('logged_in'):
        st.success(f"Signed in as {st.session_state.get('username')}")
        if st.button("Sign Out", key="signout_utils"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            safe_rerun()
    else:
        st.write("Created by **Muhammad Khan**")



st.set_page_config(page_title="Utilities", page_icon="🛠️")
st.title("Utilities 🛠️")
st.caption("Created by Muhammad Khan")

tab1, tab2 = st.tabs(["Random Password Generator", "QR Codes Generator"])

with tab1:
        st.subheader("🔐 Password Gen")
        st.write("Generate a strong and secure password now")
        
        length = st.slider("Length", 8, 32, 16, key="pwd_length1")
        use_special = st.checkbox("Include Symbols (@#$%)", value=True)
        
        if st.button("Generate Password", key="gen_pwd_btn"):
            # define allowed characters
            characters = string.ascii_letters + string.digits
            if use_special:
                characters += "!@#$%^&*"
            
            # Generate
            pwd = ''.join(random.choice(characters) for i in range(length))
            
            pwd_placeholder = st.empty()
            curreent_text = ""
            for char in pwd:
                curreent_text += char
                pwd_placeholder.code(curreent_text + "█")
                time.sleep(0.05)

            pwd_placeholder.code(curreent_text) 
            st.caption("Copy it instantly.")

with tab2:
    st.subheader("QR Code Generator")
    st.write("Generate QR codes for URLs or text")

    qr_data = st.text_input("Enter URL or text to encode:", "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLbpi6ZahtOH4SVczoTshjP05vUsysmMCz&index=1")

    if st.button("Generate QR Code", key="gen_qr_btn"):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buf = BytesIO()
        img.save(buf)
        byte_im = buf.getvalue()
        st.image(Image.open(BytesIO(byte_im)), caption="Your QR Code")

        st.caption(f"Points to: {qr_data}")


