import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout="wide")

census = pd.read_csv("census_filtered_data.csv")

# Sidebar
st.sidebar.title("📊 Indian Census Data Analysis (2011)")
st.sidebar.subheader("Visualize different aspects of the Census")

# Unique states
list_of_states = list(census["State"].unique())
list_of_states.insert(0, "Overall India")


selected_state = st.sidebar.selectbox(
    "Select the State", options=list_of_states)


primary_cols = [
    "Population", "Literate", "Literacy Rate", "Rural Households", "Urban Households",
    "Housholds With Electricity", "Households With Internet", "Male", "Female", "Sex Ratio",
    "Hindus", "Muslims"
]


secondary_cols = [
    "Literacy Rate", "Male Literate", "Female Literate", "Urban Households",
    "Housholds With Electricity", "Households With Internet", "Sex Ratio", "Population",
    "Hindus", "Muslims"
]

primary = st.sidebar.selectbox("Select Primary Parameter", options=primary_cols)

secondary = st.sidebar.selectbox("Select Secondary Parameter", options=secondary_cols)


st.title("🇮🇳 Indian Census 2011 Dashboard")
st.markdown("### Explore population, literacy, and other parameters across states and districts")


if selected_state == "Overall India":
    df = census.groupby("State").sum().reset_index()
else:
    df = census[census["State"] == selected_state]

# metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Population", f"{df['Population'].sum()}")
col2.metric("Average Literacy Rate", f"{df['Literacy Rate'].mean():.2f}%")
col3.metric("Sex Ratio per 1000 Males",
            f"{(df['Female'].sum() / df['Male'].sum())*1000:.0f}")


plot = st.sidebar.button("Generate Plots")


if plot:
    st.text(f"Size of the bubble represents the {primary}")
    st.text(f"Color of the bubble represents the {secondary}")
    if selected_state == "Overall India":
        fig = px.scatter_mapbox(
            census,
            lat="Latitude",
            lon="Longitude",
            size=primary,
            color=secondary,
            color_continuous_scale="viridis",
            size_max=30,
            hover_name="State",
            hover_data={"District": True},
            zoom=3,
            mapbox_style="carto-positron",
            width=1200, height=800,
            title="Census Data Across India"
        )
    else:
        fig = px.scatter_mapbox(
            census[census["State"] == selected_state],
            lat="Latitude",
            lon="Longitude",
            size=primary,
            color=secondary,
            hover_name="State",
            hover_data={"District": True},
            color_continuous_scale="viridis",
            size_max=30,
            zoom=4,
            mapbox_style="carto-positron",
            width=800, height=600,
            title=f"Census Data Across {selected_state}"
        )
    st.plotly_chart(fig, use_container_width=True)


