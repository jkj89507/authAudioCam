from imutils import paths
import cv2
import numpy as np
from PIL import Image
import os
import face_recognition
import pickle

MAIN_PATH = "Dataset/"

recognizer = cv2.face.LBPHFaceRecognizer_create()
faceCascade = cv2.CascadeClassifier()
if not faceCascade.load(cv2.samples.findFile('faces.xml')):
    print("recognitionFace.py_faceCascsade: failed")
    exit(0)


def teachFace(path: str):
    imagePaths = list(paths.list_images(path))
    knownEncodings = []
    knownNames = []
    for (i, imagePath) in enumerate(imagePaths):
        name = imagePath.split(os.path.sep)[-2]
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb,model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()

def getDataForTeach(userName: str, video_source=0):
    totalPath = os.path.join(MAIN_PATH, userName)
    os.mkdir(totalPath)

    index = 0
    accessCamera = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
    accessCamera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    accessCamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    print("Collecting data for User" + userName + "...")
    while(True):
        ret, frame = accessCamera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            index += 1

        cv2.imwrite(totalPath + '/' + str(index) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('Collecting...', frame)
        if index == 20:
            break
    print("Stop collecting...")
    accessCamera.release()
    cv2.destroyAllWindows()

# getDataForTeach(1, )
# teachFace(MAIN_PATH)