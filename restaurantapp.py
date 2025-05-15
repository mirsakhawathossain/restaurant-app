# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/mirsakhawathossain/restaurant-app/refs/heads/main/Dataset%20.csv")
    return df

df = load_data()

# Title
st.title("🍽️ Restaurant Cuisine Classification Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
city = st.sidebar.multiselect("Select City", df['City'].unique())
cuisine = st.sidebar.multiselect("Select Cuisine", df['Cuisines'].dropna().unique())

filtered_df = df.copy()
if city:
    filtered_df = filtered_df[filtered_df['City'].isin(city)]
if cuisine:
    filtered_df = filtered_df[filtered_df['Cuisines'].isin(cuisine)]

# Show data summary
st.subheader("Data Overview")
st.dataframe(filtered_df.head(20))

# Cuisine Distribution
st.subheader("Cuisine Distribution")
top_cuisines = filtered_df['Cuisines'].value_counts().nlargest(10)
fig, ax = plt.subplots()
sns.barplot(x=top_cuisines.values, y=top_cuisines.index, ax=ax)
ax.set_xlabel("Count")
ax.set_title("Top 10 Cuisines")
st.pyplot(fig)

# City Distribution
st.subheader("Top Cities by Restaurant Count")
top_cities = filtered_df['City'].value_counts().nlargest(10)
fig, ax = plt.subplots()
sns.barplot(x=top_cities.values, y=top_cities.index, ax=ax)
ax.set_xlabel("Count")
ax.set_title("Top 10 Cities")
st.pyplot(fig)

# Average Cost for Two by Cuisine
st.subheader("Average Cost for Two by Cuisine")
avg_cost = filtered_df.groupby('Cuisines')['Average Cost for two'].mean().nlargest(10)
fig, ax = plt.subplots()
sns.barplot(x=avg_cost.values, y=avg_cost.index, ax=ax)
ax.set_xlabel("Average Cost for Two")
ax.set_title("Top 10 Expensive Cuisines")
st.pyplot(fig)

# Ratings Distribution
st.subheader("Ratings Distribution")
fig, ax = plt.subplots()
sns.histplot(filtered_df['Aggregate rating'], bins=20, kde=False, ax=ax)
ax.set_xlabel("Aggregate Rating")
ax.set_title("Aggregate Ratings Histogram")
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, Matplotlib & Seaborn")
