import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

class MonteCarlo:
    
    def __init__(self, ticker, quote_frequency, distribution, mean, standard_deviation, number_of_paths, estimation_time, close_price, mc_output_graph):
        
        self.ticker = ticker
        self.quote_frequency = quote_frequency
        self.distribution = distribution
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.number_of_paths = number_of_paths
        self.estimation_time = estimation_time
        self.close_price = close_price
        self.mc_output_graph = mc_output_graph
        
        if self.distribution == "Normal Distribution":
        
            st.write("generating simulations using normal distribution")
            monte_carlo = pd.DataFrame([np.random.normal(loc = float(self.mean / 100), scale = float(self.standard_deviation), size = self.number_of_paths) for x in range(estimation_time)])
            monte_carlo_cumsum = monte_carlo.cumsum()
            monte_carlo_dist = monte_carlo.iloc[len(monte_carlo) - 1]
            
            #simulated price path
            price_paths = (1 + monte_carlo_cumsum) * self.close_price
            
            #monte_carlo.to_csv('monte_carlo.csv')
            #monte_carlo_cumsum.to_csv('monte_carlo_cumsum.csv')
            
            if self.mc_output_graph == "Streamlit (Interactive)":

                st.subheader("{} Monte Carlo {} {} estimation with {} simulated return".format(self.ticker, self.estimation_time, self.quote_frequency, self.number_of_paths))
                st.line_chart(monte_carlo)
                
                st.subheader("{} Monte Carlo {} {} estimation with {} simulated cumulative return".format(self.ticker, self.estimation_time, self.quote_frequency, self.number_of_paths))
                st.line_chart(monte_carlo_cumsum)
                
                mc_output_col1, mc_output_col2 = st.columns(2)
                
                with mc_output_col1:
                    
                    st.header("{} Monte Carlo {} {} distribution with {} simulated return".format(self.ticker, self.estimation_time, self.quote_frequency, self.number_of_paths))
                    monte_carlo_dist_plotly = [monte_carlo_dist.values * 100]
                    group_label = [self.ticker]
                    fig = ff.create_distplot(monte_carlo_dist_plotly, group_label)
                    st.plotly_chart(fig, bin_size = [0.1])
                    
                with mc_output_col2:
                    
                    quote_frequency_dict = {"days": "Daily", "weeks": "weekly", "months": "Monthly"}
                    
                    st.header('Output Statistics')
                    st.subheader("{} Returns Mean".format(quote_frequency_dict[self.quote_frequency]))
                    st.text("{}%".format(round(monte_carlo_dist.mean() * 100,3)))
                    st.text("")
                    st.subheader("{} Returns Standard Deviation".format(quote_frequency_dict[self.quote_frequency]))
                    st.text(round(monte_carlo_dist.std(),3))
                    

            if self.mc_output_graph == "Matplotlib (JPEG)":
                
                mc_figure, mc_axes = plt.subplots(figsize = (24,10))
                mc_axes.plot(monte_carlo, color = "blue", alpha = 0.2)
                mc_axes.set_title("{} Monte Carlo {} {} estimation with {} simulated return".format(self.ticker, self.estimation_time, self.quote_frequency, self.number_of_paths))
                mc_axes.grid()
                st.pyplot(mc_figure)
                
                mc_figure_cumsum, mc_cumsum_axes = plt.subplots(figsize = (24,10))
                mc_cumsum_axes.plot(monte_carlo_cumsum, color = "red", alpha = 0.2)
                mc_cumsum_axes.set_title("{} Monte Carlo {} {} estimation with {} simulated cumulative return".format(self.ticker, self.estimation_time, self.quote_frequency, self.number_of_paths))
                mc_cumsum_axes.grid()
                st.pyplot(mc_figure_cumsum)
                
                price_path_figure, price_path_axes = plt.subplots(figsize = (24,10))
                price_path_axes.plot(price_paths, color = "green", alpha = 0.2)
                price_path_axes.set_title("{} Monte Carlo {} {} estimation with {} simulated price paths".format(self.ticker, self.estimation_time, self.quote_frequency, self.number_of_paths))
                price_path_axes.grid()
                st.pyplot(price_path_figure)
                
                mc_output_col1, mc_output_col2 = st.columns(2)
                
                with mc_output_col1:
                
                    dist_fig, dist_axes = plt.subplots(figsize = (5,5))
                    dist_axes.hist(monte_carlo_dist, bins = 50)
                    dist_axes.set_title("{} Monte Carlo {} {} distribution with {} simulated return".format(self.ticker, self.estimation_time, self.quote_frequency, self.number_of_paths))
                    st.pyplot(dist_fig)
                    
                with mc_output_col2:
                    
                    quote_frequency_dict = {"days": "Daily", "weeks": "weekly", "months": "Monthly"}
                    
                    st.header('Output Statistics')
                    st.subheader("{} Returns Mean".format(quote_frequency_dict[self.quote_frequency]))
                    st.text("{}%".format(round(monte_carlo_dist.mean() * 100,3)))
                    st.text("")
                    st.subheader("{} Returns Standard Deviation".format(quote_frequency_dict[self.quote_frequency]))
                    st.text(round(monte_carlo_dist.std(),3))