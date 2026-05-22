import streamlit as st
import pandas as pd
import os

st.title("📁 Evaluation History")

if os.path.exists("history.csv"):

    history_df = pd.read_csv("history.csv")

    st.dataframe(
        history_df,
        use_container_width=True
    )

    with open("history.csv", "rb") as file:

        st.download_button(
            label="⬇️ Download History CSV",
            data=file,
            file_name="history.csv",
            mime="text/csv"
        )

else:
    st.info("No history available.")