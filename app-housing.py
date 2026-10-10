from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(Path(__file__).parent / "housing.csv")


df = load_data()

st.title("California Housing Data (1990) by Minyang")

minimum_value = st.slider(
    "Minimal Median House Value", min_value=0, max_value=500001, value=200000
)
st.subheader("See more filters in the sidebar:")

location_types = df["ocean_proximity"].unique().tolist()
selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types,
)
income_level = st.sidebar.radio(
    "Choose income level", options=["Low", "Medium", "High"]
)

filtered_df = df[
    (df["median_house_value"] >= minimum_value)
    & (df["ocean_proximity"].isin(selected_locations))
]

if income_level == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered_df = filtered_df[
        (filtered_df["median_income"] > 2.5)
        & (filtered_df["median_income"] < 4.5)
    ]
else:
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]

st.map(filtered_df)

fig, ax = plt.subplots()
ax.hist(filtered_df["median_house_value"], bins=30)
ax.set_xlabel("Median house value (US dollars)")
ax.set_ylabel("Number of districts")
st.pyplot(fig)
plt.close(fig)
