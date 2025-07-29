import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommend Apartments")

# Load data with caching
@st.cache_data
def load_data():
    with open('location_df.pkl', 'rb') as file:
        location_df = pickle.load(file)
    cosine_sim1 = pickle.load(open('cosine_sim1.pkl', 'rb'))
    cosine_sim2 = pickle.load(open('cosine_sim2.pkl', 'rb'))
    cosine_sim3 = pickle.load(open('cosine_sim3.pkl', 'rb'))
    properties_df = pd.read_csv('appartments.csv')  # CSV with PropertyName, Link, Price, etc.
    return location_df, cosine_sim1, cosine_sim2, cosine_sim3, properties_df

location_df, cosine_sim1, cosine_sim2, cosine_sim3, properties_df = load_data()

@st.cache_data
def recommend_properties(property_name, top_n=5, min_score=0):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    idx = location_df.index.get_loc(property_name)
    sim_scores = cosine_sim_matrix[idx]
    # Create DataFrame for similarity scores
    sims_df = pd.DataFrame({
        'PropertyName': location_df.index,
        'SimilarityScore': sim_scores
    })
    # Exclude the selected property itself
    sims_df = sims_df[sims_df.PropertyName != property_name]
    # Filter by minimum similarity score
    sims_df = sims_df[sims_df.SimilarityScore >= min_score]
    # Sort and select top_n
    top_recommendations = sims_df.sort_values('SimilarityScore', ascending=False).head(top_n)
    # Merge with property details (links, price, etc.)
    merged = top_recommendations.merge(properties_df, on='PropertyName', how='left')
    return merged

# UI
st.title('Select Location and Radius')
location = st.selectbox('Location', sorted(location_df.columns.tolist()))
radius = st.number_input('Radius in kms', min_value=0.1, value=2.0, step=0.1)
if st.button('Search'):
    filtered = location_df[location_df[location] < radius * 1000][location].sort_values()
    st.subheader(f"Apartments within {radius} km of {location}:")
    for key, dist in filtered.items():
        st.text(f"{key} - {round(dist/1000, 2)} kms")

st.title('Recommend Apartments')
selected_apartment = st.selectbox('Select an apartment', sorted(location_df.index.to_list()))
top_n = st.slider("Number of Recommendations", 1, 20, 5)
min_score = st.slider("Minimum Similarity Score", 0.0, 1.0, 0.0, 0.05)

if st.button('Recommend'):
    recommendations = recommend_properties(selected_apartment, top_n=top_n, min_score=min_score)
    for _, row in recommendations.iterrows():
        st.markdown(
            f"**{row['PropertyName']}** - Score: {row['SimilarityScore']:.2f}  \n"
           
            f"[View Property]({row['Link']})"
        )
