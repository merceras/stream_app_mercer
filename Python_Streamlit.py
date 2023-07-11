import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
from streamlit_multipage import MultiPage

st.set_page_config(page_title="Sample Superstone Dashboard", page_icon="bar_chart", layout="wide")
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
st.title("Sample Supersore Dashboard using Python")
f = st.file_uploader("Upload a file", type=(["csv","txt","xlsx","xls"]))
if f is not None:
    path_in = f.name
    st.write(path_in)
    df = pd.read_csv(path_in, lineterminator='\n', encoding="ISO-8859-1")
else:
    df = pd.read_csv(r"Sample - Superstore.csv", lineterminator='\n', encoding="ISO-8859-1")

df["Order Date"] = pd.to_datetime(df["Order Date"])
startDate = pd.to_datetime(df['Order Date'].min())
endDate = pd.to_datetime(df['Order Date'].max())

col5, col6 = st.columns((2, 2))

with col5:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col6:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))
    df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)]

st.sidebar.header("Choose your filter :")

region = st.sidebar.multiselect('Pick the Region', df['Region'].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]

state = st.sidebar.multiselect('Pick the State', df2['State'].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)]

city = st.sidebar.multiselect('Pick the City', df3['City'].unique())

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
    filtered_df = df3[df3['State'].isin(state) & df3['City'].isin(city)]
elif region and city:
    filtered_df = df3[df3['Region'].isin(region) & df3['City'].isin(city)]
elif region and state:
    filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state)]
elif city:
    filtered_df = df3[df3['City'].isin(city)]
else:
    filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]

category_df = filtered_df

with col5:
    fig1, ax1 = plt.subplots()
    ax1.bar(category_df["Category"], category_df["Sales"], color='#004953')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Sales')
    ax1.set_title('Category-wise Sales')
    ax1.set_xticklabels(category_df["Category"], rotation=90)
    st.pyplot(fig1, use_container_width=True)

with col6:
    fig, ax = plt.subplots()
    ax.pie(filtered_df["Sales"], labels=filtered_df["Region"], autopct='%1.1f%%', startangle=90)
    ax.set_title('Total Sales % as per Region')
    st.pyplot(fig, use_container_width=True)

filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
fig2, ax2 = plt.subplots()
filtered_df.groupby(filtered_df['month_year'].dt.strftime('%Y : %b'))['Sales'].sum().plot(ax=ax2)
ax2.set_xlabel('Month')
ax2.set_ylabel('Sales Amount')
ax2.set_title('Month-wise Sales')
st.pyplot(fig2, use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df[['Region', 'State', 'City', 'Category', 'Sales', 'Quantity']])
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Data', data=csv, file_name="Data.csv", mime='text/csv')
