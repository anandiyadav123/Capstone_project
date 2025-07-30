import streamlit as st
import pickle
import pandas as pd
import numpy as np
from numpy import expm1
st.set_page_config(page_title="viz_Demo")

with open('df.pkl','rb') as file:
    df=pickle.load(file)

with open('pipeline.pkl','rb') as file:
    pipeline=pickle.load(file)

st.title("Price Predictor")

st.header("Enter your inputs")

#property type
Property_Type=st.selectbox("Property Type",df['property_type'].unique().tolist())
Sector=st.selectbox("Sector",sorted(df['sector'].unique().tolist()))
Number_of_bedrooms=float(st.selectbox("Number of Bedroom",sorted(df['bedRoom'].unique().tolist())))
Number_of_bathrooms=float(st.selectbox("Number of Bathroom",sorted(df['bathroom'].unique().tolist())))
Number_of_balcony=st.selectbox("Number of Balcony",sorted(df['balcony'].unique().tolist()))
property_age=st.selectbox("Property Age",sorted(df['agePossession'].unique().tolist()))
Built_up_area=float(st.number_input("Built up area"))

servant_room=float(st.selectbox("Servant Room",[0.0,1.0]))
store_room=st.selectbox("Store Room",[0.0,1.0])
furnishing_type=st.selectbox("Furnishing Type",sorted(df['furnishing_type'].unique().tolist()))
luxury_category=st.selectbox("Luxury Category",sorted(df['luxury_category'].unique().tolist()))
floor_Category=st.selectbox("Floor Category",sorted(df['floor_category'].unique().tolist()))

if st.button("Predict Price"):
    #form a dataframe
    input_df=pd.DataFrame([[Property_Type,Sector,Number_of_bedrooms,Number_of_bathrooms,Number_of_balcony,property_age,Built_up_area,servant_room,store_room,furnishing_type,luxury_category,floor_Category]],columns=['property_type','sector','bedRoom','bathroom','balcony','agePossession','built_up_area','servant room','store room','furnishing_type','luxury_category','floor_category'])
    st.dataframe(input_df)

    #predict
    base_price=np.expm1(pipeline.predict(input_df))[0]
    low=round((base_price-0.22),2)
    high=round((base_price+0.22),2)

    #display
    if Built_up_area<50.0 or Built_up_area>15000.0:
        st.markdown("""
        <div style="
            background-color: #ffebee; 
            border: 2px solid #f44336; 
            border-radius: 10px; 
            padding: 15px; 
            margin: 10px 0; 
            color: #d32f2f; 
            font-weight: bold;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        ">
            ⚠️ ALERT ⚠️<br>
            Please enter a valid built up area
        </div>
        """, unsafe_allow_html=True)
    else:
        st.text("The Price of the {} is between {} cr and {} cr".format(Property_Type,low,high))