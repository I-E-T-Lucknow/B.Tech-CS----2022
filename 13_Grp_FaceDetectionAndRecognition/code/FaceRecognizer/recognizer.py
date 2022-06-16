import cv2
from .models import Person


class Recognizer(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self, recognizer, faceCascade):

        font = cv2.FONT_HERSHEY_SIMPLEX

        names = list(Person.objects.all().values_list('name', flat=True))

        # set video width and height
        self.video.set(3, 1500)
        self.video.set(4, 1000)

        # Define min window size to be recognized as a face
        minW = 0.1 * self.video.get(3)
        minH = 0.1 * self.video.get(4)

        ret, img = self.video.read()
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Check if confidence is less them 100 ==> "0" is perfect match
                if 100 - confidence >= 50:
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(id), (x + 5, y - 5), font, 2, (0, 255, 0), 3)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 255), 1)

            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes()