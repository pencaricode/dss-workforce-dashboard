import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.title("📈 Workforce Analytics")

if os.path.exists("history.csv"):

    history_df = pd.read_csv("history.csv")

    st.subheader("CF Trend")

    trend_fig = go.Figure()

    trend_fig.add_trace(go.Scatter(
        y=history_df["CF"],
        mode='lines+markers',
        name='CF Trend'
    ))

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

    st.subheader("Performance Distribution")

    category_count = history_df["Kategori"].value_counts()

    pie_fig = go.Figure(
        data=[
            go.Pie(
                labels=category_count.index,
                values=category_count.values,
                hole=0.4
            )
        ]
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )

else:
    st.warning("No analytics data available.")