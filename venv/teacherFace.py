from imutils import paths
import cv2
import numpy as np
from PIL import Image
import os
import face_recognition
import pickle

MAIN_PATH = "Dataset/User1"

recognizer = cv2.face.LBPHFaceRecognizer_create()
faceCascade = cv2.CascadeClassifier()
if not faceCascade.load(cv2.samples.findFile('faces.xml')):
    print("recognitionFace.py_faceCascsade: failed")
    exit(0)


def teachFace(path: str):
#     imageListPaths = [os.path.join(path, file) for file in os.listdir(path)]
#     faceSamples = []
#     ids = []
#     for imagePath in imageListPaths:
#         PIL_img = Image.open(imagePath).convert('L')
#         img_numpy = np.array(PIL_img, 'uint8')
#         id = int(os.path.split(imagePath)[-1].split(".")[1])
#         for (x, y, w, h) in faceCascade.detectMultiScale(img_numpy):
#             faceSamples.append(img_numpy[y:y + h, x:x + w])
#             ids.append(id)
#     recognizer.train(faceSamples, np.array(ids))
#     recognizer.save("trainer/trainer.yml")

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

def getDataForTeach(idUser: int, video_source=0):
    index = 0
    accessCamera = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
    accessCamera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    accessCamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    print("Collecting data for User" + str(idUser) + "...")
    while(True):
        ret, frame = accessCamera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            index += 1

        cv2.imwrite(MAIN_PATH + "/" + str(index) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('Collecting...', frame)
        if index == 20:
            break
    print("Stop collecting...")
    accessCamera.release()
    cv2.destroyAllWindows()

# getDataForTeach(1, )
teachFace(MAIN_PATH)