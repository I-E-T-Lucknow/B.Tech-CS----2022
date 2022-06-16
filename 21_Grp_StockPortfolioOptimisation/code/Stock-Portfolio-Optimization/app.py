import os
import re
from flask import Flask, request , json ,render_template, send_from_directory
from portfolio import improve
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template("index.html")

''''
Basically a hotstocks.html page needs to be designed that will be put inside templates folder.
'''

@app.route('/hotstocks')
def hotStocks():
    return render_template("hotstocks.html")

# The flows below is a static web page and can be easily picked up.
@app.route('/optimizers')
def optimizers():
    return render_template("optimizers.html")

@app.route('/report')
def report():
    return render_template("report.html",report="oldreport.pdf")

@app.route('/signUp')
def signUp():
    return "Not a part of current project.To be done."


@app.route('/optimize', methods=['POST'])
def optimize():
    
    content_type = request.headers.get('Content-Type')
    print(content_type)

    data  = request.form

    amt = int(data["amount"])
    tic = list(data["tickers"].split(','))

    print(amt)
    print(tic)

    d = improve(tic,amt)
    print(d)

    # get these after rendering and storing in assets
    _chart_markowitz = d['pieMarkowitz']
    _chart_rpp = d['pieRiskParity']
    _chart_hrp = d['pieHRP']

    _barchart_expectedreturns =d['barExpectedOutcomeError']
    _barchart_changedvariance = d['barVarianceError']
    _barchart_sharpratio = d['barSharpeRatioError']
    mr = d["mr"]*100            
    hr = d["hr"]*100
    rr = d["rr"]*100

    return render_template(
    "optimized_portfolio.html",
    chart_markowitz=_chart_markowitz,
    chart_rpp=_chart_rpp,
    chart_hrp=_chart_hrp,
    barchart_expectedreturns=_barchart_expectedreturns,
    barchart_changedvariance=_barchart_changedvariance,
    barchart_sharpratio=_barchart_sharpratio,
    tickers=tic,
    hrp_allocation = d["ha"],
    rp_allocation= d["ra"],
    markowitz_allocation = d["ma"],
    markowitz_return = mr,
    hrp_return = hr,
    risk_return = rr
    )

    

if __name__ == "__main__":
    app.run()