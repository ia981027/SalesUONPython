import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.utils.mongodb import find


def write_summaries(df: pd.DataFrame, key: str):
    st.subheader(key)
    col1, col2 = st.columns(2)
    with col1:
        unique_values = df[key].unique()
        st.subheader(f"Unique {key}s")
        st.dataframe(unique_values, use_container_width=True)
    with col2:
        st.subheader("Bar Chart By Date")
        st.scatter_chart(df[[key, "SaleDate"]], y=key, x="SaleDate")


st.session_state.data = find()

st.session_state.df = pd.DataFrame(st.session_state.data)
st.session_state.df.dropna(inplace=True)
st.session_state.df["Make"] = pd.Categorical(st.session_state.df["Make"])
del st.session_state.df["_id"]

st.dataframe(st.session_state.df.tail(), use_container_width=True)
write_summaries(st.session_state.df, "Make")
write_summaries(st.session_state.df, "Model")
