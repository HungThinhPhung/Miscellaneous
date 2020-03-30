import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(nrows=None):
    data = pd.read_csv('titanic_data/train.csv', nrows=nrows)
    return data


if __name__ == '__main__':
    st.title('Titanic Visualize')
    data:pd.DataFrame = load_data()
    max_nrows = len(data)
    # Show raw data
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        nrows = st.number_input('Select number or rows to display (0 to display all)', min_value=0, step=1, value=10)
        if nrows == 0 or nrows > len(data):
            nrows = len(data)
        st.write(data.head(int(nrows)))

    # Describe columns
    des_col = st.selectbox('Describe column', ['---'] + list(data.columns)[1:])
    if not des_col == '---':
        st.write(data[des_col].describe())

    # Pivot table
    pivot_col = st.selectbox('Show pivot table', ['---'] + list(data.columns)[2:])
    if not pivot_col == '---':
        pivot = data.pivot_table(index=pivot_col,values="Survived")
        st.write(pivot)
        if st.checkbox('Plot bar chart'):
            chart = pivot.plot.bar()
            st.write('Drawing ...')
            st.pyplot()
            st.write('Done')