# Fake Product Review Monitoring
In recent times, product reviews on online shopping sites perform a significant role in product sales since people and organizations strive to learn all of the benefits and drawbacks of a product before purchasing it because there are numerous options for the same thing, as there can be different multiple manufacturers who manufacture the same type of product. There could be a variation in the sellers who provide the product, or there could be a difference in the procedure that is followed while making a purchase of the product, so the reviews can be directly linked with the product's sales, and thus it is crucial for online services to filter out fake reviews since their own reputation is at stake. Thus, we need a Fake Review Detection System is needed to discover any suspicious reviews because it's impractical for them to manually check for every review linked with products. So a technology is utilised to try to detect any tendency in the customer reviews. Our review monitoring system makes 6 checks to check for the negative reviews in large datasets. The six kinds of checks are -Review which have dual view, Reviews in which same user promoting or demoting a brand, Reviews in which same IP address is promoting or demoting a brand, Reviews posted as flood by same user, Similar reviews posted in same time frame, Meaning less texts in reviews using LSA


## Installation

Make sure you have Python & jupyter notebook installed on your system. 

- Install Python 3 or above for ML model.

- Install Jupyter Notebook for ML model.

- Install Visual Studio Code for better code readbility for fullstack product review app.

- Install Nodejs and Mongodb.

- Clone the project (or copy the folder to your local)

- To Run ML Model Locally:

- Install dependencies in cmd

    ```
      pip install  nltk, pickle, re, Pandas , random


    ```
- run jupyter notebook in cmd.

Now, the ML model is ready to run.

## Run fullstack product review app Locally

## Run it locally
1. Install [mongodb](https://www.mongodb.com/)
2. Create a cloudinary account to get an API key and secret code

```
git clone 
cd Wander-World
npm install
```

Create a .env file (or just export manually in the terminal) in the root of the project and add the following:  

```
DATABASEURL='<url>'
API_KEY=''<key>
API_SECRET='<secret>'
```

Run ```mongod``` in another terminal and ```node app.js``` in the terminal with the project.  

Then go to [localhost:3000](http://localhost:3000/).
  
The project is running now.


## Tech Stack

**Language:** Python, Nodejs,Html, CSS, ejs

**Libraries:** nltk, pickle, re, Pandas



## Authors

- Anushka kanaujia (B.Tech. CSE-2022 - 1805210010) (clg Email id)(1805210010@ietlucknow.ac.in), (per email)(anushkakanaujia@gmail.com)
- Astha Sachan (B.Tech. CSE-2022 - 1805210015) (clg Email id)(1805210015@ietlucknow.ac.in), (per email)(asthasachan02@gmail.com)
- Prateeksha Tiwari (B.Tech. CSE-2022 - 1805210037) (clg Email id)(1805210037@ietlucknow.ac.in), (per email)(prateekshatiwari56@gmail.com)
