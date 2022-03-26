import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

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
        ret, frame, x, y, w, h = self.accessCamera.get_frame()

        if ret:
            cv2.imwrite("Dataset/photo{}.png".format(time.time()),
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[y:y + h, x:x + w])

    def update(self):
        ret, frame, x, y, w, h = self.accessCamera.get_frame()

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

                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), x, y, w, h)
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.accessCamera.isOpened():
            self.accessCamera.release()

App(tkinter.Tk(), "Tkinter and OpenCV")