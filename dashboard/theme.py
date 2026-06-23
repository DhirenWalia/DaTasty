def apply_theme():
    import streamlit as st

    st.markdown(
        """
        <style>
        .main {
            background-color: #0F172A;
            color: white;
        }
        .stMetric {
            background-color: #1E293B;
            padding: 20px;
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )