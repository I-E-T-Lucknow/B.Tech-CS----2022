from django.http import HttpResponse
from django.shortcuts import render
from django.http import StreamingHttpResponse
from .models import Person
from FaceRecognizer.createDataset import FaceDetect
from FaceRecognizer.recognizer import Recognizer
import cv2
import numpy as np
from PIL import Image
import os


def recognizer(request):
    return render(request, "recognizer.html", {})


def home(request):
    return render(request, "home.html", {})


def create(request):
    return render(request, "create.html", {"userName": request.GET['userName']})


def gen_create_dataset(camera, face_id):
    while camera.count <= 800:
        frame = camera.get_frame(face_id)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def create_dataset(request):
    names = list(Person.objects.all().values_list('name', flat=True))
    face_id = len(names)
    print(face_id)

    name = request.GET['userName'].capitalize()
    data=Person.objects.create(name=name)
    data.save()
    return StreamingHttpResponse(gen_create_dataset(FaceDetect(), face_id),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def train_dataset(request):
    path = 'FaceRecognizer/dataset'  # Path for face image database

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("FaceRecognizer/Cascades/haarcascade_frontalface_default.xml")

    # function to get the images and label data
    def getImagesAndLabels(path):

        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
            img_numpy = np.array(PIL_img, 'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)

        return faceSamples, ids

    faces, ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer/trainer.yml
    recognizer.save('FaceRecognizer/trainer/trainer.yml')
    return HttpResponse("Model Trained")


def gen_face_recognizer(camera):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('FaceRecognizer/trainer/trainer.yml')

    cascadePath = "FaceRecognizer/Cascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    while True:
        frame = camera.get_frame(recognizer, faceCascade)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def face_recognizer(request):
    return StreamingHttpResponse(gen_face_recognizer(Recognizer()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')