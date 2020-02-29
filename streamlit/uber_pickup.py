"""
Base doc: https://docs.streamlit.io/tutorial/create_a_data_explorer_app.html
"""
import streamlit as st
import pandas as pd
import numpy as np

file = 'uber-raw-data-sep14.csv.gz'


@st.cache  # Caching
def load_data(nrows=None):
    """
    Load data, rename columns to lowercase, format date/time column data to datetime type
    :param nrows: Number of rows loaded, default is None mean that get whole data
    :return: Converted data
    """
    data = pd.read_csv(file, nrows=nrows)

    def lowercase_func(x): return str(x).lower()

    data.rename(lowercase_func, axis='columns', inplace=True)
    data['date/time'] = pd.to_datetime(data['date/time'])
    return data


# load_data()

if __name__ == '__main__':
    st.title('Uber pickups in NYC')
    # The text indicates that the app is loading data
    data_load_state = st.text('Loading data...')
    # Load 10000 rows of data to dataframe
    data = load_data(10000)
    # Notify user that data was successful loaded
    st.write('Done! (using st.cache)')
    # Add subheader and print data if checkbox is checked
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)  # This function render almost anything you pass to it

    # Draw a histogram
    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(data['date/time'].dt.hour, bins=24, range=(0, 24))[0]  # Generate histogram by numpy
    st.bar_chart(hist_values)  # Draw a bar chart

    # Plot data on a map (filter by time)
    hour_to_filter = st.slider('hour', 0, 23, 17)  # create slider, default is 17
    filtered_data = data[data['date/time'].dt.hour == hour_to_filter]
    st.subheader(f'Map of all pickups at {hour_to_filter}:00')  # pass hour_to_filter as parameter
    st.map(filtered_data)
