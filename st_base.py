import pandas as pd
import datetime as dt
import yfinance as yf
import streamlit as st

from bootstrap import *
from monte_carlo import *

st.set_page_config(layout = "wide")
st.header("Simulation App")
today = dt.date.today()

function_list = ["Monte Carlo", "Bootstrap"]
graph_selections = ["Streamlit", "Matplotlib (JPEG)"]

before = today - dt.timedelta(days=3653)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)

if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    
else:
    st.sidebar.error('Error: End date must fall after start date.')
    
sidebar_function = st.sidebar.selectbox("select a function", function_list)

ticker = st.text_input("Please enter ticker here (seperate):")
st.text("ex for Microsoft (MSFT) for S&P 500 (^GSPC) for VIX (^VIX)")

quote_frequency_list = ["daily", "weekly", "monthly"]
beg_col1, beg_col2 = st.columns(2)

with beg_col1:
    quote_frequency = st.selectbox("Please select quote frequency", quote_frequency_list)

with beg_col2:
    status_radio = st.radio('Please click run when you are ready.', ('stop', 'run'))

if status_radio == "run":
    
    col1, col2 = st.columns(2)
    
    with col1: 
        
        if quote_frequency == "daily":
            
           df = yf.download(ticker, start_date, end_date)
           quote_frequency = "days"
           
        if quote_frequency == "weekly":
            
            df = yf.download(ticker, start_date, end_date, interval = "1wk")
            quote_frequency = "weeks"
           
        if quote_frequency == "monthly":
            
            df = yf.download(ticker, start_date, end_date, interval = "1mo")
            quote_frequency = "months"
           
        st.dataframe(df)
        quote_list = df.columns[:-1]
    
    with col2:
        st.line_chart(df[["Close", "Adj Close"]])

    if sidebar_function == "Monte Carlo":
        
        st.subheader("Monte Carlo Simulation")
        mc_col1, mc_col2 = st.columns(2)
        
        distribution_list = ["Normal Distribution"]
        
        with mc_col1:
            
            st.write("Select Distribution & Quote paramters")
            quote_type = st.selectbox("Select a quote", quote_list)
            distribution_type = st.selectbox("Select a distribution", distribution_list)
            
        with mc_col2:
            
            st.write('The default numbers are the mean and standard deviation for the stock inputted')
            
            mean = df[quote_type].pct_change().mean() * 100
            standard_deviation = df[quote_type].pct_change().std()
            
            input_mean = st.number_input("mean (%)", mean)
            input_standard_deviation = st.number_input("standard deviation", standard_deviation)
            
        mc_col3, mc_col4 = st.columns(2)
        
        with mc_col3:
            path_numbers = st.number_input("Number of paths (Default 10,000)", 2000)
            
        with mc_col4:
            estimate_value = st.number_input("Number of {} to estimate".format(quote_frequency), 252)
        
        mc_col5, mc_col6 = st.columns(2)
        
        with mc_col5: 
           mc_graph_type = st.selectbox("select an output for Monte Carlo graphs", graph_selections)
           
        with mc_col6:
            mc_radio = st.radio('Please click run when you are ready to run the Monte Carlo Simulation.', ('stop', 'run'))
        
        if mc_radio == "run":
            monte_carlo = MonteCarlo(ticker, quote_frequency, distribution_type, input_mean, input_standard_deviation, 
                                     path_numbers, estimate_value, df[quote_type][len(df) -1], mc_graph_type)
            
    if sidebar_function == "Bootstrap":
        
        bootstrap_col1, bootstrap_col2, bootstrap_col3 = st.columns(3)
        
        with bootstrap_col1:
            input_simulations = st.number_input("Insert the number of simulations", 2000)
            
        with bootstrap_col2:
            estimate_value = st.number_input("Number of {} to estimate".format(quote_frequency), 252)
            
        with bootstrap_col3:
            quote_type = st.selectbox("Select a quote", quote_list) 
            
        bootstrap_radio = st.radio('Please click run when you are ready to run the Boostrap.', ('stop', 'run'))
        
        if bootstrap_radio == "run":            
            bootstrap = BootStrap(ticker, quote_frequency, df, quote_type, input_simulations, estimate_value)
            