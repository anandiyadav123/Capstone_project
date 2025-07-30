import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import seaborn as sns
import io

st.set_page_config(page_title="Dynamic Real Estate Analytics", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("data_viz1.csv")
    return df

df = load_data()

# --- SIDEBAR: DYNAMIC MULTI-FILTER PANEL ---
st.sidebar.header("🔎 Dynamic Filtering Panel")

sectors = ['All'] + sorted(df['sector'].dropna().unique().tolist())
bedroom_options = ['All'] + sorted(df['bedRoom'].dropna().astype(str).unique())
age_possession_options = ['All'] + sorted(df['agePossession'].dropna().astype(str).unique())

selected_sector = st.sidebar.selectbox("Sector", sectors, key="filter_sector")
selected_bedroom = st.sidebar.selectbox("Bedroom", bedroom_options, key="filter_bedroom")
selected_possession = st.sidebar.selectbox("Possession Status", age_possession_options, key="filter_possession")

# --- FILTER DATA ACCORDING TO SELECTION (except price) ---
filtered_df = df.copy()
if selected_sector != 'All':
    filtered_df = filtered_df[filtered_df['sector'] == selected_sector]
if selected_bedroom != 'All':
    filtered_df = filtered_df[filtered_df['bedRoom'].astype(str) == selected_bedroom]
if selected_possession != 'All':
    filtered_df = filtered_df[filtered_df['agePossession'].astype(str) == selected_possession]

# --- Handle empty DataFrame before showing price slider ---
if filtered_df.empty:
    st.warning("No results for selected filters. Please widen your criteria.")
    st.stop()

# --- Price Range Slider (dynamically from filtered data) ---
price_min = int(filtered_df['price'].min())
price_max = int(filtered_df['price'].max())
selected_price = st.sidebar.slider(
    "Price Range", min_value=price_min, max_value=price_max,
    value=(price_min, price_max), step=int((price_max - price_min) / 100) or 1, key="filter_price"
)

# --- Final filter with price applied ---
filtered_df = filtered_df[(filtered_df['price'] >= selected_price[0]) & (filtered_df['price'] <= selected_price[1])]

if filtered_df.empty:
    st.warning("No results for selected filters and price range. Please widen your criteria.")
    st.stop()

# --- MAIN DASHBOARD ---
st.title("🏡 Dynamic Real Estate Analytics Dashboard")
# --- SUMMARY METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Properties", len(filtered_df))
with col2:
    st.metric("Avg Price", f"{filtered_df['price'].mean():,.0f}")
with col3:
    st.metric("Median Area", f"{filtered_df['built_up_area'].median():.0f} sqft")
with col4:
    st.metric("Distinct Societies", filtered_df['society'].nunique())

# --- GEO MAP ---
st.subheader("📍 Map of Average Price per Sector")
with st.expander("ℹ️ About this map"):
    st.markdown(
        """
        - Each marker on the map represents a sector.
        - The marker's hover tooltip (appears when you put your mouse over the dot) displays:
        -->   Sector name
        --> Average property price in that sector
        -->  Average price per sqft
        -->  Average built-up area
        - Bubble size shows average built-up area.
        """
    )
if not filtered_df.empty and "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:
    group_df = filtered_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean().reset_index()
    fig_map = px.scatter_mapbox(
        group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
        mapbox_style="open-street-map", text='sector', hover_name='sector', width=1200, height=600)
    st.plotly_chart(fig_map, use_container_width=True)

# --- WORDCLOUD ---
st.subheader("🔤 Feature Wordcloud")
with st.expander("ℹ️ About this wordcloud"):
    st.markdown(
        """
        This word cloud shows the most frequent words from the selected data’s key features:
        - Property Type (e.g., house, flat)
        - Society names (residential complexes)
        - Possession status (property age/ownership)
        - Larger words appear more often. The cloud updates dynamically with your filters, helping you spot popular attributes quickly.
        """
    )
all_text = (
    filtered_df['property_type'].astype(str) + " " +
    filtered_df['society'].astype(str) + " " +
    filtered_df['agePossession'].astype(str)
).str.cat(sep=" ")

if all_text.strip():
    wordcloud = WordCloud(
        width=800, height=400, background_color="white",
        colormap="viridis", stopwords=STOPWORDS, min_font_size=10
    ).generate(all_text)
    fig_wc, ax = plt.subplots(figsize=(12, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    st.pyplot(fig_wc)

    buf = io.BytesIO()
    fig_wc.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
    st.download_button(
        label="Download Wordcloud Image",
        data=buf.getvalue(),
        file_name="wordcloud.png",
        mime="image/png"
    )
else:
    st.info("Not enough text data in the filtered results for wordcloud.")

# --- IMPROVED AREA vs PRICE SCATTERPLOT with property type distinction ---
# --- PROPERTY TYPE FILTER ---
st.subheader("🔵 Area vs Price Scatter Plot")
with st.expander("ℹ️ How to use this scatter plot"):
    st.markdown(
        """
        - Shows each property's built-up area and price, filtered by property type.
        - Hover for details: sector, society, bedrooms, and possession.
        - Use filters to change property type and other criteria.
        """
    )

property_type_options = ["Both", "House", "Flat"]
selected_property_type = st.selectbox(
    "Property Type (for Area vs Price Plot)", property_type_options, key="scatter_property_type"
)

if selected_property_type == "Both":
    df_scatter = filtered_df.copy()
elif selected_property_type == "House":
    df_scatter = filtered_df[filtered_df["property_type"].str.lower() == "house"]
else:  # "Flat"
    df_scatter = filtered_df[filtered_df["property_type"].str.lower() == "flat"]


if df_scatter.empty:
    st.info("No properties match the selected filters for this property type.")
else:
    fig_scatter = px.scatter(
        df_scatter,
        x="built_up_area", 
        y="price",
        color="bedRoom",
        labels={
            "built_up_area": "Area (sqft)",
            "price": "Price (INR)",
            "bedRoom": "Bedrooms"
        },
        hover_data={
            "sector": True,
            "society": True,
            "bedRoom": True,
            "agePossession": True,
            "property_type": True,
            "price": ":.0f",
            "built_up_area": ":.0f"
        },
        title=f"Area vs Price: {selected_property_type}" if selected_property_type != "Both" else "Area vs Price: Flat and House",
        opacity=0.7,
        height=600
    )
    fig_scatter.update_traces(
        marker=dict(size=13, line=dict(width=1, color='#555'))
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- PIE CHART: BEDROOM DISTRIBUTION ---
st.subheader("🥧 Bedroom (BHK) Distribution")
with st.expander("ℹ️ About this pie chart"):
    st.markdown(
        """
        This pie chart shows the proportion of properties by bedroom count (BHK) in your current selection.  
        See which home sizes are most common with your chosen filters.
        """
    )
fig_pie = px.pie(
    filtered_df, names='bedRoom', title="Bedroom Distribution", hole=0.5,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_pie, use_container_width=True)

# --- BOX PLOT: PRICE DISTRIBUTION BY BEDROOM (User Friendly) ---
st.subheader("📊 Price Distribution by Bedroom (BHK)")
with st.expander("ℹ️ What does this plot show?"):
    st.markdown(
        """
        - **Each box** visualizes the spread of property prices for each bedroom (BHK) count.
        - **Dots** show individual property prices—hover to see sector, society, area, and more.
        - **The middle line** in the box is the median price.
        - **Whiskers** cover most typical prices; dots outside are outlier properties.
        """
    )

fig_box = px.box(
    filtered_df, 
    x="bedRoom", 
    y="price", 
    color="bedRoom",
    title="Price Range by Bedroom (BHK)",
    points="all",              # Show all datapoints (outliers + inliers)
    labels={
        "bedRoom": "No. of Bedrooms (BHK)",
        "price": "Price (INR)",
    },
    hover_data=["sector", "society", "built_up_area", "agePossession", "property_type"]
)

fig_box.update_traces(jitter=0.3, marker_opacity=0.4)
fig_box.update_layout(showlegend=False, boxmode='group')
st.plotly_chart(fig_box, use_container_width=True)

# --- DISTRIBUTION PLOT (HOUSE/FLAT) ---
if "property_type" in filtered_df.columns:
    st.subheader("📈 Price Distribution: House vs Flat")
    with st.expander("ℹ️ About this plot"):
        st.markdown(
            """
            - Shows price distribution for each property type (House/Flat) in the filtered data.
            - Blue for House, Orange for Flat.
            """
        )
    fig_distplot = plt.figure(figsize=(10, 4))
    for ptype, color in zip(['house', 'flat'], ['blue', 'orange']):
        subset = filtered_df[filtered_df['property_type'] == ptype]
        if not subset.empty:
            sns.histplot(subset['price'], color=color, label=ptype.capitalize(), kde=True, stat="density")
    plt.legend()
    plt.xlabel('Price')
    plt.title("Price Distribution by Property Type")
    st.pyplot(fig_distplot)

# --- CORRELATION HEATMAP ---
st.subheader("🧮 Correlation Heatmap (Numeric Features)")
with st.expander("ℹ️ What does this show?"):
    st.markdown(
        """
        - Visualizes statistical correlation between features in your current filtered data.
        - Bright colors = strong correlation (positive or negative).
        - Use this to spot features that move together or are inversely related.
        """
    )
numeric_cols = filtered_df.select_dtypes(include='number')
if not numeric_cols.empty:
    corr = numeric_cols.corr()
    fig_corr, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    plt.title("Correlation Matrix (Filtered Data)")
    st.pyplot(fig_corr)
else:
    st.info("No numeric features available for correlation analysis in current filter.")
