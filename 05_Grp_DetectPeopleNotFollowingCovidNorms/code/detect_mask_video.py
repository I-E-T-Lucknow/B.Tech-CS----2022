# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
from datetime import datetime
from twilio.rest import Client 
import numpy as np
import imutils
import face_recognition
import time
import cv2
import os
import requests
import json
import secretKey
import smtplib

#connecting to mail server 

server = smtplib.SMTP()
server._host = "smtp.gmail.com"
server.connect("smtp.gmail.com",587)
server.ehlo()
server.starttls()
server.ehlo()

server.login(secretKey.MY_MAIL_ADDRESS , secretKey.MY_MAIL_PASSWORD)


f = open('data.json', 'r')
data = json.load(f)
data = data["data"]



def findEncoding(images):
	encodeList = []
	for img in images:
		curImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		encode = face_recognition.face_encodings(img)[0]
		encodeList.append(encode)
	return encodeList


path = 'knownImage'
images = []
contactNumber = []
mailArr = []
name = []
myList = os.listdir(path)

for img in myList:
	curImg = cv2.imread(f'{path}/{img}')
	images.append(curImg)
	index = os.path.splitext(img)[0]
	index = int(index)
	contactNumber.append(data[index]['contact'])
	mailArr.append(data[index]['mail'])
	name.append(data[index]['name'])

encodeList = findEncoding(images)



def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()
	print(detections.shape)

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []
  
	# loop over the detections
	for i in range(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > 0.5:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			
			face = preprocess_input(face)

		
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)




# load our serialized face detector model from disk
prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model frqqom disk
maskNet = load_model("mask_detector.model")



# initialize the video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()

# loop over the frames from the video stream
cnt = 0 


def sendTheMessage(contactNumber, mail , name):
	with open('sheet.csv' , 'r+') as file: 
		myDataList = file.readlines()
		contactList = []
		

		for contact in myDataList:
			entry = contact.split(',')
			contactList.append(entry[0])

		if contactNumber not in contactList:
			time = datetime.now()
			dtString = time.strftime('%H:%M:%S')

			file.writelines(f'\n{contactNumber},{name},{mail},{dtString}')

			client = Client(secretKey.ACCOUNT_SID , secretKey.AUTH_TOKEN)
			textMsg = "Dear " + name +",\n\n"+ "We have detected that you have not wear mask in public place. Please wear your mask otherwise you will be fined."
			if len(contactNumber)>11: 
				message = client.messages.create(
					body = textMsg,
					from_ = secretKey.TWILIO_NUMBER,
					to = contactNumber
					)
				print(message.body)
			else:
				print(contactNumber+" is not verified by twilio")
			SUBJECT = "Warning regarding COVID-19"
			message = 'Subject: {}\n\n{}'.format(SUBJECT, textMsg)
			server.sendmail(secretKey.MY_MAIL_ADDRESS, mail , message)




while True:

	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	imgS = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

	facesCurFrame = face_recognition.face_locations(imgS)
	encode = face_recognition.face_encodings(imgS , facesCurFrame)


	for encodeFace , FaceLoc in zip(encode , facesCurFrame):
		matches = face_recognition.compare_faces(encodeList , encodeFace)
		faceDist = face_recognition.face_distance(encodeList , encodeFace)
		
		matchIndex = np.argmin(faceDist)
		if matches[matchIndex] and contactNumber[matchIndex] and mailArr[matchIndex]:
			contact = contactNumber[matchIndex]
			mail = mailArr[matchIndex]
			Name = name[matchIndex]
			sendTheMessage(contact , mail, Name)


	(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
	for (box, pred) in zip(locs, preds):
		(startX, startY, endX, endY) = box
		(mask, withoutMask) = pred

		label = "Mask" if mask > withoutMask else "No Mask"
		color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

		label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

		cv2.putText(frame, label, (startX, startY - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()