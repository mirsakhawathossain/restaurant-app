# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset .csv")
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
cuisine_counts = filtered_df['Cuisines'].value_counts().nlargest(10)
fig1 = px.bar(cuisine_counts, x=cuisine_counts.index, y=cuisine_counts.values,
              labels={'x': 'Cuisine', 'y': 'Count'}, title="Top 10 Cuisines")
st.plotly_chart(fig1)

# City Distribution
st.subheader("Top Cities by Restaurant Count")
city_counts = filtered_df['City'].value_counts().nlargest(10)
fig2 = px.bar(city_counts, x=city_counts.index, y=city_counts.values,
              labels={'x': 'City', 'y': 'Count'}, title="Top 10 Cities")
st.plotly_chart(fig2)

# Average Cost for Two
st.subheader("Average Cost for Two by Cuisine")
avg_cost = filtered_df.groupby('Cuisines')['Average Cost for two'].mean().nlargest(10)
fig3 = px.bar(avg_cost, x=avg_cost.index, y=avg_cost.values,
              labels={'x': 'Cuisine', 'y': 'Avg Cost for Two'}, title="Top 10 Expensive Cuisines")
st.plotly_chart(fig3)

# Ratings
st.subheader("Ratings Distribution")
fig4 = px.histogram(filtered_df, x='Aggregate rating', nbins=20, title="Aggregate Ratings Histogram")
st.plotly_chart(fig4)

# Map
st.subheader("Restaurant Locations")
fig5 = px.scatter_mapbox(filtered_df.dropna(subset=['Latitude', 'Longitude']),
                         lat="Latitude", lon="Longitude", hover_name="Restaurant Name",
                         color="Aggregate rating", size="Votes", zoom=1,
                         mapbox_style="carto-positron", title="Restaurants on Map")
st.plotly_chart(fig5)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

