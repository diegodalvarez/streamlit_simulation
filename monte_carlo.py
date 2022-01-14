import numpy as np
import pandas as pd
import streamlit as st

class MonteCarlo:
    
    def __init__(self, ticker, quote_frequency, distribution, mean, standard_deviation, number_of_paths, estimation_time, close_price):
        
        self.ticker = ticker
        self.quote_frequency = quote_frequency
        self.distribution = distribution
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.number_of_paths = number_of_paths
        self.estimation_time = estimation_time
        self.close_price = close_price
        
        if self.distribution == "Normal Distribution":
        
            st.write("generating simulations")
            monte_carlo = pd.DataFrame([np.random.normal(loc = float(self.mean / 100), scale = float(self.standard_deviation), size = self.number_of_paths) for x in range(estimation_time)])
            st.write("simulations done")
            monte_carlo_cumsum = monte_carlo.cumsum()
            
            st.subheader("{} Monte Carlo {} {} estimation with {} simulated return".format(self.ticker, self.estimation_time, self.quote_frequency, self.number_of_paths))
            st.line_chart(monte_carlo)
            
            st.subheader("{} Monte Carlo {} {} estimation with {} simulated cumulative return".format(self.ticker, self.estimation_time, self.quote_frequency, self.number_of_paths))
            st.line_chart(monte_carlo_cumsum)