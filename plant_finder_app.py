import pandas as pd
import streamlit as st

from plant_finder_main import data_input

st.set_page_config(layout="wide")

def st_normal(): #Normal page width option
    _, col, _ = st.columns([1, 2, 1])
    return col

def st_wider(): #Wider page width option
    _, col, _ = st.columns([1, 5, 1])
    return col

with st_normal():

    st.title("Plant Finder App")


    option = st.selectbox( #Primary filter search
        'Please select an option:',
        [ 'Soil Search', 'pH Search'])

    st.write('You selected: ', option)

if option == 'Soil Search':
    with st_normal():
        soil_type = st.selectbox( #Soil types to select
            'Please select a soil type:',
            ['Gravel', 'Clay', 'Sand'])
        st.write('You selected: ', soil_type)

    results = data_input('soil', soil_type, None, None) #Sends request to backend
    df = pd.DataFrame(results, columns=['ID', 'Name', 'Description', 'pH Min', 'pH Max', 'Sunlight', 'Water Frequency'])
    with st_wider(): #Receives and proceeds to write the returned plants
        st.write(df)

else:
    with st_normal(): #pH range options
        ph_min = st.slider('Select minimum pH value:', 
                           0, 14, 6)
        ph_max = st.slider('Select maximum pH value:', 
                           0, 14, 8)
        st.write(f'You selected: pH{ph_min} to pH{ph_max}')

    results = data_input('ph', None, ph_min, ph_max)
    df = pd.DataFrame(results, columns=['ID', 'Name', 'Description', 'pH Min', 'pH Max', 'Sunlight', 'Water Frequency'])
    with st_wider(): #Receives and proceeds to write the returned plants
        st.write(df)
