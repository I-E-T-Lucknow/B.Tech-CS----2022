
# Music Genre Detection - IET Lucknow
 
In Music IR research, genre classification is a common question. To group feature headings produced from short-opportunity record parts into kinds, the majority of music type categorization approaches use pattern recognition algorithms. Support Vector Machines (SVMs), Nearest-Neighbor (NN) classifiers, Gaussian Mixture Models, Linear Discriminant Analysis (LDA), and other classifiers are commonly
utilised. 

In this project we used CNN to categorize audio files into ten different musical genres: ‘classical, country, hip-hop, jazz, metal, disco, pop, blues, reggae, and rock’.


## Prerequisites

Your machine should have following items installed:

- Python 3.7 or higher [[Resource](https://www.python.org/downloads/)]
- A code editor like VS Code [[Resource](https://code.visualstudio.com/download)]


## Setup


- Clone the repo (or copy the folder to your local)

    ```bash
      git clone https://github.com/ExpressHermes/B.Tech-CS----2022.git
    ```

- Go to the project directory

    ```bash
      cd <my-project>
    ```

- Install dependencies using the requirements.txt file

    ```python
      pip install -r requirements.txt
    ```

- Run the project 

    ```
    cd src/
    python ./get_genre.py ./test.mp3
    ```
     The model will output the % probablity for each genre that the following audio file might belong to. 


## Tech Stack

- **Language:** Python

- **Libraries:** Librosa, Pytorch, Scikit, NumPy, Pandas

- **Machine Learning Model:** Convolutional Neural Netwok(CNN)



## Authors

- Shivam Yadav (B.Tech CSE-2022 - 1805210049) [[Resume](https://bit.ly/3h0XhVB), [LinkedIn](https://www.linkedin.com/in/express-hermes/), [GitHub](https://github.com/ExpressHermes)]
- Abhishek Kumar Singh (B.Tech CSE-2022 - 1805210001) [[Resume](https://docs.google.com/document/d/1FrHYQsoEXMD2nSE99j8G-rsm_af3OhUzukd4CGGwq5o/edit?usp=sharing), [LinkedIn](https://www.linkedin.com/in/abhishek-kumar-singh-6aa779187), [GitHub](https://github.com/abhisheksingh945)]
- Akash Saha (B.Tech CSE-2022 - 1805210005) 