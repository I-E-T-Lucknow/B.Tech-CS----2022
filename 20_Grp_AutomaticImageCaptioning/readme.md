##Introduction:

Image Captioning is the system of producing a textual description for given images.It has been an extremely important and basic endeavor in the 
Deep Learning space. Picture subtitling has a major amount of use. NVIDIA is the usage of picture captioning applied sciences to create an software to assist human beings who have low or no eyesight.
Picture inscribing can be considered as a start to finish Sequence to Sequence issue, as it changes over pictures, which is considered as a grouping of pixels to a succession of words. For this reason, we need to methodology each the 
language or explanations and the pictures. For the Language part, we utilize intermittent Neural Networks and for the Image part, we use Convolutional Neural Networks to individually accomplish the capacity vectors.
Before moving to further chapters let’s understand the about digital imagers and their advantages.An image is visual representation of object. It can be anything from paintings, sculptures, photos etc. The images are in existence from a very 
long time now. As computers cannot understand images, it became necessary to develop special methods to represent images in computers.


To build this system we followed following architecture where we maintain 2 repositories one of image and other of images's corresponding captions.
We pass images and captions through image and language pipeline respectively. Image pipeline is basically a 2 step process of resizing image to 224x224 
image and passing it through Resnet50 model to generate feature vectors.
In language pipeline, we pass captions and first preprocess them to produce all lower case text, add suffix and prefixes as well. Then captions are passed through
RNN models to generate word embeddings and thus feature vectors.
Both image and caption feature vectors are then passed through LSTM architecture to build a model.

Once model developed, the site is build on Flask framework which is a light-weight python framework.



##Getting Started:
Clone the repo

Download and install python from https://www.python.org/downloads/
Install and update pip to latest version

Install requirements.txt file from "B.Tech-CS----2022/20_Grp_AutomaticImageCaptioning/code/image-captioning-website/" using 
pip3 install -r requirements.text

To start the application run app.py file
>python3 app.py
This will start the server on localhost
Open http://127.0.0.1:5000 and you will be presented with a running application



##To run training module
Clone the repo

Download and install python from https://www.python.org/downloads/
Install and update pip to latest version

Install requirements.txt file from "B.Tech-CS----2022/20_Grp_AutomaticImageCaptioning/code/image-captioning-website/" using 
pip3 install -r requirements.text

Download dataset from https://www.kaggle.com/datasets/srbhshinde/flickr8k-sau
run train.py using 
python3 train.py


##The Team:
1. Ansh Lehri (Roll No :1805210008, Mobile No :6387415081, email :1805210008@ietlucknow.ac.in)
2. Ashutosh Kumar Singh (Roll No :1805210013, Mobile No :8707046409, email :1805210013@ietlucknow.ac.in)
3. Himanshu Verma (Roll No :1805210022, Mobile No :9125841136, email :1805210022@ietlucknow.ac.in)

