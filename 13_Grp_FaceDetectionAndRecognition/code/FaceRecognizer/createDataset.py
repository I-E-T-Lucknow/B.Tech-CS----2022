import cv2


class FaceDetect(object):
    def __init__(self):
        # initialize the video stream, then allow the camera sensor to warm up
        # self.vs = VideoStream(src=0).start()
        # start the FPS throughput estimator
        # self.fps = FPS().start()
        self.count = 1
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self, face_id):

        face_detector = cv2.CascadeClassifier('FaceRecognizer/Cascades/haarcascade_frontalface_default.xml')

        ret, img = self.video.read()
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imwrite("FaceRecognizer/dataset/User." + str(face_id) + '.' + str(self.count) + ".jpg",
                            gray[y:y + h, x:x + w])
                self.count += 1

            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes()
