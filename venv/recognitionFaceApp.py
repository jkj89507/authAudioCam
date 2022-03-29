import tkinter
import imutils
import pickle
import cv2
import PIL.Image, PIL.ImageTk
import time
import os
import face_recognition

faceCascade = cv2.CascadeClassifier()
if not faceCascade.load(cv2.samples.findFile('faces.xml')):
    print("recognitionFace.py_faceCascsade: failed")
    exit(0)

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.accessCamera = MyVideoCapture(self.video_source)
        self.canvas = tkinter.Canvas(window, width = self.accessCamera.width, height = self.accessCamera.height)
        self.canvas.pack()

        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        ret, frame = self.accessCamera.get_frame()

        if ret:
            cv2.imwrite("Dataset/photo{}.jpg".format(time.time()),
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            exit(0)

    def update(self):
        ret, frame = self.accessCamera.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        self.accessCamera = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        self.accessCamera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.accessCamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        if not self.accessCamera.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.accessCamera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.accessCamera.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.accessCamera.isOpened():
            ret, frame = self.accessCamera.read()
            if ret:
                faces = faceCascade.detectMultiScale(
                        frame,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(20, 20)
                    )

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (219,255,253), 1)

                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.accessCamera.isOpened():
            self.accessCamera.release()

# App(tkinter.Tk(), "Tkinter and OpenCV")

data = pickle.loads(open('face_enc', "rb").read())
image = cv2.imread("Dataset/photo1648562379.7690928.jpg")
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(gray,
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(60, 60),
                                     flags=cv2.CASCADE_SCALE_IMAGE)

encodings = face_recognition.face_encodings(rgb)
names = []
for encoding in encodings:
    matches = face_recognition.compare_faces(data["encodings"],
                                             encoding)
    name = "Unknown"
    if True in matches:
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}
        for i in matchedIdxs:
            name = data["names"][i]
            counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        names.append(name)
        for ((x, y, w, h), name) in zip(faces, names):
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)
    cv2.imshow("Frame", image)
    cv2.waitKey(0)