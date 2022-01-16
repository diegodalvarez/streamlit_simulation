import random
import numpy as np
import pandas as pd
import streamlit as st

class BootStrap:
    
    def __init__(self, ticker, quote_frequency, df, quote_type, input_simulations, sample_size):
        
        #ticker
        self.ticker = ticker

        #days, weeks, month
        self.quote_frequency = quote_frequency
        
        #the stock dataframe
        self.df = df

        #open, high, low, close, or Adj Close
        self.quote_type = quote_type

        #number of simulations
        self.input_simulations = input_simulations

        #how many days to simulate out to
        self.sample_size = sample_size
        
        self.df = self.df[self.quote_type].to_frame().pct_change().dropna().mean(axis = 1)
        output_df = pd.DataFrame(columns = [i for i in range(self.input_simulations)])
        
        st.write("generating simulations via Boostrapping")
        for j in range(self.input_simulations):
            
            sample_list = []
            
            if j % 2 == 0:
                st.write("completed {} simulations".format(j))
            
            for i in range(sample_size):
                sample_list.append(random.choices(self.df)[0])
                
            output_df[j] = sample_list
        output_cumsum = output_df.cumsum()
        
        st.write("output df")
        st.write(output_df)
        output_df.to_csv("output.csv")
        
        st.write("output cumsum")
        st.write(output_cumsum)
        output_cumsum.to_csv("output_cumsum.csv")
        
        '''
        st.subheader("{} Bootstrapping {} {} estimation with {} simulated return".format(self.ticker, self.sample_size, self.quote_frequency, self.input_simulations))
        st.line_chart(output_df)
        
        st.subheader("{} Bootstrapping {} {} estimation with {} simulated cumulative returns".format(self.ticker, self.sample_size, self.quote_frequency, self.input_simulations))
        st.line_chart(output_cumsum)
        '''