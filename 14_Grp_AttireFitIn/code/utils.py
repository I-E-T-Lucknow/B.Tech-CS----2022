import os
import cv2
import numpy as np
from PIL import Image
import torch
import cv2
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys
from  PIL  import Image
from cv2 import hconcat

import tkinter
from tkinter import *
from PIL import Image, ImageTk


def gen_noise(shape):
    noise = np.zeros(shape, dtype=np.uint8)
    ### noise
    noise = cv2.randn(noise, 0, 255)
    noise = np.asarray(noise / 255, dtype=np.uint8)
    noise = torch.tensor(noise, dtype=torch.float32)
    return noise


def save_images(img_tensors, img_names, save_dir):
    for img_tensor, img_name in zip(img_tensors, img_names):
        tensor = (img_tensor.clone()+1)*0.5 * 255
        tensor = tensor.cpu().clamp(0,255)

        try:
            array = tensor.numpy().astype('uint8')
        except:
            array = tensor.detach().numpy().astype('uint8')

        if array.shape[0] == 1:
            array = array.squeeze(0)
        elif array.shape[0] == 3:
            array = array.swapaxes(0, 1).swapaxes(1, 2)

        im = Image.fromarray(array)
        im.save(os.path.join(save_dir, img_name), format='JPEG')


def load_checkpoint(model, checkpoint_path):
    if not os.path.exists(checkpoint_path):
        raise ValueError("'{}' is not a valid checkpoint path".format(checkpoint_path))
    model.load_state_dict(torch.load(checkpoint_path))

def concat(im1,im2,im5,im6,im3,im4):
    im1 = cv2.imread(im1)
    im2 = cv2.imread(im2)
    im5 = cv2.imread(im5)
    im6 = cv2.imread(im6)
    im3 = cv2.imread(im3)
    
    # im3 = im3.resize(256,192)
    result =cv2.hconcat([im2,im1,im5,im6,im3])
    cv2.imwrite(im4, result)


# im1 = r'D:\Final Year Project\VITON-HD\datasets\test\cloth\01430_00.jpg'
# im2 = r'D:\Final Year Project\VITON-HD\datasets\test\image\00891_00.jpg'
# im3 = r'D:\Final Year Project\VITON-HD\results\new_output\00891_01430_00.jpg'

# concat(im1,im2,im3)

def show(path):
    root = Tk()
    root.title('Cloth - Image - Image_Parse - Openpose_Img -  Output')
    canvas = Canvas(root, width = 1550, height = 450 )
    canvas.pack()
    # Create a photoimage object of the image in the path
    image1 = Image.open(path)
    image1 = image1.resize((1500, 400), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)
    
    canvas.create_image(20,20, anchor=NW, image=test)
    root.mainloop()

def newshow(path):
    root = Tk()

    canvas = Canvas(root, width = 350, height = 450 )
    canvas.pack()
    # Create a photoimage object of the image in the path
    image1 = Image.open(path)
    image1 = image1.resize((300, 400), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)

    # label1 = tkinter.Label(image=test)
    # label1.image = test

    # # Position image
    # label1.place(x=160, y=60)
    canvas.create_image(20,20, anchor=NW, image=test)
    root.mainloop()

def remove_back(path):
    img = cv.imread(path, cv.IMREAD_UNCHANGED)
    original = img.copy()

    l = int(max(15, 6))
    u = int(min(26, 26))

    ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges = cv.GaussianBlur(img, (21, 51), 3)
    edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(edges, l, u)

    _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

    data = mask.tolist()
    sys.setrecursionlimit(10**8)
    for i in  range(len(data)):
        for j in  range(len(data[i])):
            if data[i][j] !=  255:
                data[i][j] =  -1
            else:
                break
        for j in  range(len(data[i])-1, -1, -1):
            if data[i][j] !=  255:
                data[i][j] =  -1
            else:
                break
    image = np.array(data)
    image[image !=  -1] =  255
    image[image ==  -1] =  0

    mask = np.array(image, np.uint8)

    result = cv.bitwise_and(original, original, mask=mask)
    result[mask ==  0] =  255
    cv.imwrite('bg.png', result)

    img = Image.open('bg.png')
    img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(r"D:\Final Year Project\Attire_Fit_In\images\removed_back\img.jpg")