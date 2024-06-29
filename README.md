# Stock-Analysis Project

# Overview
This project provides a Python script that fetches historical stock prices from the Twelve Data API, calculates various technical indicators such as SMA, EMA, RSI, and MACD, and visualizes the results. Users can generate detailed stock analysis charts and summaries, aiding in better investment decisions and market trend evaluations.

# Design
The design of this project emphasizes simplicity and ease of use, leveraging standard Python libraries to maximize accessibility. I utilized `pandas` for data manipulation, `requests` for API interaction, and `matplotlib` for visualization, ensuring a streamlined workflow for fetching, analyzing, and visualizing stock market data with minimal setup. 

# Methodology
I utilized historical stock price data, including daily closing prices, to calculate key technical indicators such as SMA, EMA, RSI, and MACD. By applying rolling calculations and exponential smoothing techniques, I derived these indicators to identify market trends and potential trading signals. The processed data was then visualized to provide clear insights into stock performance and trend analysis.

# Usage
Clone this repository to your local machine. Navigate to the repository's directory and run the 'Stock_Analysis.py' script to start the analysis. Enter in the desired stock symbol, the start and end date of the analysis, and if you'd like to include the EMA, RSI, and MACD lines in the visualization. 

# Sample Execution
For these inputs:

<img width="550" alt="Screen Shot 2024-06-29 at 1 24 07 AM" src="https://github.com/eshaanadu/Stock-Analysis/assets/142547447/cf11c0a2-3d10-4dd0-8ac4-a718f96f7739">

The output plots Apple's stock price analysis during the desired time frame.
<img width="800" alt="Screen Shot 2024-06-29 at 1 31 57 AM" src="https://github.com/eshaanadu/Stock-Analysis/assets/142547447/454d4455-7b18-412f-9e3b-c520ec9d24d7">


The output also provides a brief description of the visualization.
<img width="1010" alt="Screen Shot 2024-06-29 at 1 25 24 AM" src="https://github.com/eshaanadu/Stock-Analysis/assets/142547447/c266292d-8134-4838-8ec8-268dc853c752">
