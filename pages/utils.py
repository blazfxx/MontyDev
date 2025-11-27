
import time
import streamlit as st


def safe_rerun():

    try:
        # Supported on many streamlit versions
        st.experimental_rerun()
        return
    except Exception:
        pass

    try:
        # Changing query params using the supported `st.query_params` setter
        # forces a rerun in many contexts. Use a copy to avoid mutating
        # the object in-place if it's read-only in this Streamlit version.
        params = dict(st.query_params) if hasattr(st, 'query_params') else {}
        params['_rerun'] = int(time.time())
        st.query_params = params
        return
    except Exception:
        pass

    # Last-resort: stop the script and rely on user actions to re-render.
    try:
        st.stop()
    except Exception:
        # If even stop isn't available, give up silently.
        return
