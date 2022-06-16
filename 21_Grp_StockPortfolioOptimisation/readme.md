##Introduction:
The project aims to help users select an optimal portfolio allocation strategy according to there need. It provide an analysis of the performance of the portfolio allocated using different allocation strategies using Monte Carlo Simulations. The app is based on flask framework.

The Portfolio Allocation strategies being used:
1. Herarchical Risk Parity
2. Risk Parity
3. Markowitz Optimiser

After we have calculated the covariance matrix and the expected returns for your portfolio we feed them into the simulator. Using the optimization methods you've selected, the code then calculates the optimal weights. Then a Monte Carlo simulation is performed, where optimal allocations are computed on a large number of simulated covariances and returns. It then compares these allocations to the ideal and calculates the error.

##Getting Started:
Clone the repo

Download and install python from https://www.python.org/downloads/

Install and update using pip
>pip install mcos
>pip install pypfopt

Install flask
>pip install Flask

To start the application run app.py file
>python app.py

This will start the server on localhost

Open http://127.0.0.1:5000 and you will be presented with a running application

##The Team:

1. Yashraj Singh Bhadauria (Roll No :1805210066, Mobile No :7451000355, email :1805210066@ietlucknow.ac.in)
2. Umang Dubey (Roll No :1805210060, Mobile No :6395843633, email :1805210060@ietlucknow.ac.in)
3. Vivek Bhardwaj (Roll No :1805210063, Mobile No :9557552938, email :1805210063@ietlucknow.ac.in)



