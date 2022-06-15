from requests import request

def improve(tickers,amount) :
    import numpy as np
    import pandas_datareader as web
    import datetime
    import os
    import pandas as pd
    from mcos import optimizer
    from mcos import observation_simulator
    from mcos import mcos
    from mcos.error_estimator import ExpectedOutcomeErrorEstimator, SharpeRatioErrorEstimator, \
        VarianceErrorEstimator
    from mcos.covariance_transformer import DeNoiserCovarianceTransformer, AbstractCovarianceTransformer
    from mcos.observation_simulator import AbstractObservationSimulator, MuCovLedoitWolfObservationSimulator, \
    MuCovObservationSimulator
    from pypfopt.expected_returns import mean_historical_return
    from pypfopt.risk_models import sample_cov
    import matplotlib.pyplot as plt
    import uuid
    import warnings
    warnings.filterwarnings('ignore')

    response={}
    def saveFigure():
        filename = str(uuid.uuid4())
        filepath = os.path.join("static",filename)
        plt.savefig(filepath)
        return filename+".png"

    start_date = datetime.datetime(1990, 5, 20)         #Look into this
    end_date = datetime.date.today()
    data = {}
    def price_df() -> pd.DataFrame:
        total_df = pd.DataFrame()
        for stock_symbol in tickers:
            stock_data = web.DataReader(stock_symbol, "yahoo", start_date, end_date) # Read stock data 
            data[stock_symbol] = stock_data
            prices =pd.DataFrame(stock_data["Adj Close"]).rename(columns={"Adj Close":stock_symbol})
            prices = prices.fillna(method="ffill") # Forward fill missing data points
            if total_df.empty:
                total_df = prices
            else:
                total_df = total_df.join(prices)

        return total_df

    df = price_df()
    print(df)
    # Choose the number of simulations to run
    num_sims = 75

    # Select the optimizers that you would like to compare
    op = [optimizer.HRPOptimizer(), optimizer.MarkowitzOptimizer(), optimizer.RiskParityOptimizer()]

    # select the metric to use for comparison
    ee = ExpectedOutcomeErrorEstimator()

    # select covariance transformer
    cov_trans = DeNoiserCovarianceTransformer()

    # convert price history to expected returns and covariance matrix
    mu = mean_historical_return(df).values
    #mu = ema_historical_return(df).values
    cov = sample_cov(df).values

    print("Covariance Matrix : ")
    print(cov)
    

    # select your observational simulator
    obs_sim = MuCovObservationSimulator(mu, cov, num_sims)

    # Run the simulation
    results = mcos.simulate_optimizations(obs_sim, num_sims, op, ee, [cov_trans])
    print(results)
    results.plot.bar()
    barExpectedOutcomeError = saveFigure()

    #variance error
    ee = VarianceErrorEstimator()
    results = mcos.simulate_optimizations(obs_sim, num_sims, op, ee, [cov_trans])
    print(results)
    results.plot.bar()
    barVarianceError = saveFigure()

    #sharpe ratio error
    ee = SharpeRatioErrorEstimator()
    results = mcos.simulate_optimizations(obs_sim, num_sims, op, ee, [cov_trans])
    print(results)
    results.plot.bar()
    barSharpeRatioError =saveFigure()
   
   #weights allocation
    HRPweights=optimizer.HRPOptimizer().allocate(mu,cov)
    fig = plt.figure(figsize =(10, 7))
    plt.pie(HRPweights, labels = tickers,autopct='%1.1f%%')
    pieMarkowitz=saveFigure()

    RiskParityweights=optimizer.RiskParityOptimizer().allocate(mu,cov)
    fig = plt.figure(figsize =(10, 7))
    plt.pie(RiskParityweights, labels = tickers,autopct='%1.1f%%')
    pieRiskParity=saveFigure()

    Markowitzweights=optimizer.MarkowitzOptimizer().allocate(mu,cov)
    fig = plt.figure(figsize =(10, 7))
    plt.pie(Markowitzweights, labels = tickers,autopct='%1.1f%%')
    pieHRP=saveFigure()

    response.update( [('pieMarkowitz', pieMarkowitz),('pieRiskParity',pieRiskParity),('pieHRP',pieHRP),
    ('barSharpeRatioError',barSharpeRatioError),('barVarianceError',barVarianceError),
    ('barExpectedOutcomeError',barExpectedOutcomeError)])

    import matplotlib.dates as mdates

    #function used for plotting the performance graph of all the algorithms

    def plotg(weights,total_amount, method,stockdata):
        x2d=[]
        amounts=[]
        y2d=[]
        start_date = datetime.datetime(2020, 5, 20)
        end_date = datetime.datetime(2022, 5, 20)

        for i in range(len(stockdata)):
    #         df = pd.read_csv(stockdata[i]) 
            # stock_data = web.DataReader(stockdata[i], "yahoo", start_date, end_date) # Read stock data 
            stock_data = data[stockdata[i]]
            #prices = stock_data.loc[:, "Adj Close"]
            x = pd.to_datetime(stock_data.index).tolist()
            x2d.append(x)
            y = stock_data['Adj Close'].tolist();
            y2d.append(y)
            a = (weights[i]*total_amount);
            amounts.append(a)
            
        return amounts
       
    response["ha"] = plotg(HRPweights,amount,"HRP",tickers)
    response["ra"] = plotg(RiskParityweights,amount, "Risk Parity",tickers)
    response["ma"] = plotg(Markowitzweights,amount, "Markowitz Method",tickers)
    
    
    # predicting expected returns and portfolio variance

    start_date = datetime.datetime(1990, 5, 20)
    end_date = datetime.datetime(2022, 5, 20)
    symbol_list = tickers


    for ii in range(3) : 
        curr = ""
        weights = []
        if ii == 0 : 
            weights = HRPweights
            curr = "HRP"
        elif ii == 1 : 
            weights = Markowitzweights
            curr = "Markowitz"
        else :
            curr = "RiskParity"
            weights = RiskParityweights
        
        stock_weights ={}
        stock_annual_returns = {}
        i=0
        for stock_symbol in symbol_list:
            stock_weights[stock_symbol] = weights[i]
            i=i+1
            
        no_business_days = 252

        portfolio_return = 0

        # """Read price data and compute daily returns"""                        
        for stock_symbol in symbol_list: 
            # print(stock_symbol)
            assets = web.DataReader(stock_symbol, "yahoo", start_date, end_date)
            # assets = assets.set_index(pd.DatetimeIndex(assets['Date'].values))
            # print(assets)
            daily_returns = assets.pct_change()
            annual_returns = daily_returns.mean()*no_business_days
            ar = annual_returns["Adj Close"]
            stock_annual_returns[stock_symbol] = ar

            portfolio_return += ar * stock_weights[stock_symbol]

        print('Annualized mean return by ' + curr + " : ","{0:.2%}".format(portfolio_return))
        print(ii)
        if ii == 1 :
            response["mr"] = portfolio_return
        elif ii == 0 :
            response["hr"] = portfolio_return
        else :
            response["rr"] = portfolio_return


        # "compute covariance matrix and correlation matrix"
                                    
        # covariance_matrix = pd.DataFrame(index=symbol_list, columns=symbol_list)
        # correlation_matrix = pd.DataFrame(index=symbol_list, columns=symbol_list)

        # # """Compute all covariances and correlation coefficients"""
        # for stock1_symbol in symbol_list:
        #     for stock2_symbol in symbol_list:
        #         # Retrieve return series as arrays
        #         stock1_returns = df[stock1_symbol].values.astype(float)
        #         stock2_returns = df[stock2_symbol].values.astype(float)

        #         # Compute covariance
        #         cov = np.cov(stock1_returns, stock2_returns)[0][1]

        #         # Add covariance to matrix
        #         covariance_matrix.loc[stock1_symbol, stock2_symbol] = cov

        #         # Compute correlation
        #         corr = np.corrcoef(stock1_returns, stock2_returns)[0][1]

        #         # Add correlation to matrix
        #         correlation_matrix.loc[stock1_symbol, stock2_symbol] = corr

        # # Round correlation coefficients
        # correlation_matrix = correlation_matrix.astype(float).round(5)

        # correlation_matrix

        portfolio_variance = 0


        # """Compute variance portfolio return"""
        for i in range(len(symbol_list)) :
            for j in range(len(symbol_list)) :
                stock1_symbol = symbol_list[i]
                stock2_symbol = symbol_list[j]
                weight_stock1 = stock_weights.get(stock1_symbol)
                weight_stock2 = stock_weights.get(stock2_symbol)
                covariance= cov[i][j]  
                portfolio_variance += weight_stock1*weight_stock2*covariance

        # print(portfolio_variance)
        # # Compute annualized mean and volatility portfolio
        import math
        # print(portfolio_variance*252)
        ann_portfolio_volatility = math.sqrt(portfolio_variance*no_business_days)
        # print(ann_portfolio_volatility)
        print('Annualized portfolio volatility '+ curr + " : ",ann_portfolio_volatility)
    
    return response


    




    
