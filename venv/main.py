import os
import tkinter
from  tkinter import *
from  tkinter import ttk, messagebox, Label, Toplevel, Tk
from PIL import ImageTk, Image
from threading import Thread

from recordAudio import recordVoice
from teacherFace import getDataForTeach, teachFace, MAIN_PATH
from recognitionFaceApp import App, recog
from recognitionVoice import recognitionVoice

mainApp = Tk()

w = 400
h = 350
ws = mainApp.winfo_screenwidth()
hs = mainApp.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 50

voiceCheck = BooleanVar()
faceCheck = BooleanVar()
voiceCheck.set(False)
faceCheck.set(False)

mainApp.title("SHODAN")
mainApp.geometry('%dx%d+%d+%d' % (w, h, x, y))
mainApp.resizable(False, False)
mainApp.attributes('-alpha', 0.95)

tabContol = ttk.Notebook(mainApp)
tab1 = ttk.Frame(tabContol)
tab2 = ttk.Frame(tabContol)
tab3 = ttk.Frame(tabContol)

tabContol.add(tab1, text="Авторизация")
tabContol.add(tab2, text="Регистрация")
tabContol.add(tab3, text="Настройка")

loadImage = Image.open("thumb-1920-40977.jpg").resize((400, 300), Image.ANTIALIAS)
renderImage = ImageTk.PhotoImage(loadImage)
logotype = Label(tab1, image=renderImage)
logotype.place(x=0, y=0)

labelStartMenu = Label(tab1, text=' $|-|0D4# ', bg="#343638", fg="#04d142", font=("Helvetica", 30))

userName2 = StringVar()

def authAudioFace():
    mainApp.destroy()
    if (faceCheck.get() == True and voiceCheck.get() == True):
        th1 = Thread(target=runAppFace())
        th2 = Thread(target=openVoiceRecorderSecond())
        th3 = Thread(target=recognition())

        th1.start()
        th2.start()
        th3.start()

        th1.join()
        th2.join()
        th3.join()

    if (faceCheck.get() == True and voiceCheck.get() == False):
        th1 = Thread(target=runAppFace())
        th3 = Thread(target=recognition())

        th1.start()
        th3.start()

        th1.join()
        th3.join()

    if (faceCheck.get() == False and voiceCheck.get() == True):
        th2 = Thread(target=openVoiceRecorderSecond())
        th3 = Thread(target=recognition())

        th2.start()
        th3.start()

        th2.join()
        th3.join()


inputName2 = Entry(tab1, width=20, textvariable=userName2)
inputLabel = Label(tab1, text="Логин: ")
btnLogin = Button(tab1, text='Войти', bg='#343638',
                  fg='#04d142', width=20,
                  height=1, command=authAudioFace)

def showAuthorInfo():
    return messagebox.showinfo('About', '\t[SHODAN ver 1.0] (c)Copyright 2022\n\nДанная программа предназначена '
                                        'для демонстрации \nавторизации с помощью голоса и/или\n'
                                        'фотографиии.\n\n'
                                        'Авторы: Старыгин Михаил\n\tМихайлов Александр\n\tМатвеев Евгений')

btnInfo = Button(tab1, text=' ? ', bg='#343638', fg='#04d142',
                  width=2, height=1,command=showAuthorInfo)
inputLabel.place(x=35, y=302)
inputName2.place(x=85, y=302)
labelStartMenu.place(x=110, y=130)
btnLogin.place(x=215, y=302)
btnInfo.place(x=372, y=0)
#--------------------1st window-----------------------------

userName1 = StringVar()
inputLabel = Label(tab2, text="Логин: ")
inputName = Entry(tab2, width=20, textvariable=userName1)
btnGetVoice = Button(tab2, text='Записать голос',
                  width=20, height=1, command=lambda: openVoiceRecorderFirst())
def openFaceRecognition():
    if (userName1.get() != "" and userName1.get().find(' ') == -1
    and userName1.get().find('/') == -1
    and userName1.get().find(',') == -1):
        getDataForTeach(str(userName1.get()), )
        teachFace(str(userName1.get()))
    else:
        messagebox.showwarning('Warning!',"Поле для ввода пользователя не может быть пустым\n"
                                          "и не может содержать символы: ',' , '/', ' ' ")
        userName1.set("")

btnGetFace = Button(tab2, text='Сфотографировироваться',
                  width=20, height=1, command=openFaceRecognition)

inputLabel.place(x=90, y=80)
inputName.place(x=140, y=80)
btnGetVoice.place(x=130, y=110)
btnGetFace.place(x=130, y=140)
#------------------2nd window------------------------------

faceCheckChBt = Checkbutton(tab3, text='Авторизация по лицу', var=faceCheck)
voiceCheckChBt = Checkbutton(tab3, text='Авторизация по голосу', var=voiceCheck)
faceCheckChBt.place(x=130, y=100)
voiceCheckChBt.place(x=130, y=150)

#------------------3nd window------------------------------

tabContol.pack(expand=1, fill="both")


def showAuthorInfo():
    return messagebox.showinfo('About', '\t[SHODAN ver 1.0] (c)Copyright 2022\n\nДанная программа предназначена '
                                        'для демонстрации \nавторизации с помощью голоса и/или\n'
                                        'фотографиии.\n\n'
                                        'Авторы: Старыгин Михаил\n\tМихайлов Александр\n\tМатвеев Евгений')

def runAppFace():
    App("Tkinter and OpenCV")

def recognition():
    file = open("temp.txt", 'r')
    content = str(file.readline())
    file.close()

    getNameFromPhotoRecog = ""
    getValueFromAudioRecog = 100
    if (faceCheck.get() == True):
        getNameFromPhotoRecog = recog(content, str(userName2.get()))[len(MAIN_PATH):]

    if (voiceCheck.get() == True):
        getValueFromAudioRecog = 100 - int(recognitionVoice(str(userName2.get()) + "_1.wav", str(userName2.get()) +
                                                        "_2.wav") * 100)
    print(getNameFromPhotoRecog)
    print(getValueFromAudioRecog)

    if (getNameFromPhotoRecog != "Unknown" and getValueFromAudioRecog > 70):
        messagebox.showinfo("Login success", "Welcome {}!".format(str(userName2.get())))
    else:
        messagebox.showwarning("Access denied", "Photo/audio auth is invalid!")

    return 0


def openVoiceRecorderSecond():
    userName = str(userName2.get())
    nameForFile = "_2"
    if (userName != "" and userName.find(' ') == -1
    and userName.find('/') == -1
    and userName.find(',') == -1):
        widthVoiceRecorder = 400
        heighVoiceRecorder = 200
        wsVoiceRecorder = 1920
        hsVoiceRecorder = 1080
        xVoiceRecorder = (wsVoiceRecorder / 2) - (widthVoiceRecorder / 2)
        yVoiceRecorder = (hsVoiceRecorder / 2) - (heighVoiceRecorder / 2) - 50

        voiceRocorderWindow = Tk(className="Record voice")
        voiceRocorderWindow.geometry('%dx%d+%d+%d' % (widthVoiceRecorder, heighVoiceRecorder,
                                                      xVoiceRecorder, yVoiceRecorder))
        voiceRocorderWindow.resizable(False, False)

        texForRead = Label(voiceRocorderWindow, anchor=CENTER,
                           text='Эльвина, милый друг, приди, подай мне руку,\n'
                                    'Я вяну, прекрати тяжелый жизни сон;\n'
                                    'Скажи… увижу ли, на долгую ль разлуку\n'
                                    'Я роком осужден?\n\n'
                                    'Ужели никогда на друга друг не взглянет?\n'
                                    'Иль вечной темнотой покрыты дни мои?\n'
                                    'Ужели никогда нас утро не застанет\n'
                                    'В объятиях любви?\n\n А. С. Пушкин')
        texForRead.place(x=80, y=60)

        labelSec = Label(voiceRocorderWindow, text='sec')
        labelSec.place(x=125,y=20)

        seconds = IntVar()
        spinBoxSeconds= Spinbox(voiceRocorderWindow, textvariable=seconds,
                                values=([i for i in range(5, 13)]), width=2)
        spinBoxSeconds.place(x=100, y=20)

        microImageLoader = Image.open("micro.jpg").resize((50, 40), Image.ANTIALIAS)
        microImageRender = ImageTk.PhotoImage(microImageLoader)
        voiceRecord = Button(voiceRocorderWindow, image=microImageRender,
                             command=lambda: recordVoice(userName+nameForFile, int(seconds.get()), 1))
        voiceRecord.image = microImageRender
        voiceRecord.place(x=180, y=0)
        voiceRecord.mainloop()


def openVoiceRecorderFirst():
    userName = str(userName1.get())
    nameForFile = "_1"
    if (userName != "" and userName.find(' ') == -1
    and userName.find('/') == -1
    and userName.find(',') == -1):
        widthVoiceRecorder = 400
        heighVoiceRecorder = 200
        wsVoiceRecorder = 1920
        hsVoiceRecorder = 1080
        xVoiceRecorder = (wsVoiceRecorder / 2) - (widthVoiceRecorder / 2)
        yVoiceRecorder = (hsVoiceRecorder / 2) - (heighVoiceRecorder / 2) - 50

        voiceRocorderWindow = Toplevel(mainApp)
        voiceRocorderWindow.geometry('%dx%d+%d+%d' % (widthVoiceRecorder, heighVoiceRecorder,
                                                      xVoiceRecorder, yVoiceRecorder))
        voiceRocorderWindow.resizable(False, False)

        texForRead = Label(voiceRocorderWindow, anchor=CENTER,
                           text='Эльвина, милый друг, приди, подай мне руку,\n'
                                    'Я вяну, прекрати тяжелый жизни сон;\n'
                                    'Скажи… увижу ли, на долгую ль разлуку\n'
                                    'Я роком осужден?\n\n'
                                    'Ужели никогда на друга друг не взглянет?\n'
                                    'Иль вечной темнотой покрыты дни мои?\n'
                                    'Ужели никогда нас утро не застанет\n'
                                    'В объятиях любви?\n\n А. С. Пушкин')
        texForRead.place(x=80, y=60)

        labelSec = Label(voiceRocorderWindow, text='sec')
        labelSec.place(x=125,y=20)

        seconds = IntVar()
        spinBoxSeconds= Spinbox(voiceRocorderWindow, textvariable=seconds,
                                values=([i for i in range(5, 13)]), width=2)
        spinBoxSeconds.place(x=100, y=20)

        microImageLoader = Image.open("micro.jpg").resize((50, 40), Image.ANTIALIAS)
        microImageRender = ImageTk.PhotoImage(microImageLoader)
        voiceRecord = Button(voiceRocorderWindow, image=microImageRender,
                             command=lambda: recordVoice(userName+nameForFile, int(seconds.get()), 1))
        voiceRecord.image = microImageRender
        voiceRecord.place(x=180, y=0)
        voiceRecord.mainloop()
    else:
        messagebox.showwarning('Warning!',"Поле для ввода пользователя не может быть пустым\n"
                                          "и не может содержать символы: ',' , '/', ' ' ")
        userName.set("")
mainApp.mainloop()