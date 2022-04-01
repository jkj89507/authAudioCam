from  tkinter import *
from  tkinter import ttk, messagebox, Label
from recordAudio import recordVoice
from PIL import ImageTk, Image

mainApp = Tk()

w = 400
h = 350
ws = mainApp.winfo_screenwidth()
hs = mainApp.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 50


mainApp.title("SHODAN")
mainApp.geometry('%dx%d+%d+%d' % (w, h, x, y))
mainApp.resizable(False, False)
mainApp.attributes('-alpha', 0.95)

tabContol = ttk.Notebook(mainApp)
tab1 = ttk.Frame(tabContol)
tab2 = ttk.Frame(tabContol)

tabContol.add(tab1, text="Авторизация")
tabContol.add(tab2, text="Регистрация")


def showAuthorInfo():
    return messagebox.showinfo('About', '\t[SHODAN ver 1.0] (c)Copyright 2022\n\nДанная программа предназначена '
                                        'для демонстрации \nавторизации с помощью голоса и/или\n'
                                        'фотографиии.\n\n'
                                        'Авторы: Старыгин Михаил\n\tМихайлов Александр\n\tМатвеев Евгений')

loadImage = Image.open("thumb-1920-40977.jpg").resize((400, 300), Image.ANTIALIAS)
renderImage = ImageTk.PhotoImage(loadImage)
logotype = Label(tab1, image=renderImage)
logotype.place(x=0, y=0)

labelStartMenu = Label(tab1, text=' $|-|0D4# ', bg="#343638", fg="#04d142", font=("Helvetica", 30))

btnLogin = Button(tab1, text='Войти', bg='#343638', fg='#04d142',
                  width=20, height=1,command=())
btnInfo = Button(tab1, text=' ? ', bg='#343638', fg='#04d142',
                  width=2, height=1,command=showAuthorInfo)
labelStartMenu.place(x=110, y=130)
btnLogin.place(x=130, y=300)
btnInfo.place(x=372, y=0)
#--------------------1st window-----------------------------


def openVoiceRecorder():
    if (userName.get() != ""):
        widthVoiceRecorder = 400
        heighVoiceRecorder = 200
        wsVoiceRecorder = mainApp.winfo_screenwidth()
        hsVoiceRecorder = mainApp.winfo_screenheight()
        xVoiceRecorder = (wsVoiceRecorder / 2) - (widthVoiceRecorder / 2)
        yVoiceRecorder = (hsVoiceRecorder / 2) - (heighVoiceRecorder / 2) - 50

        voiceRocorderWindow = Toplevel(mainApp)
        voiceRocorderWindow.title("Record voice")
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
                             command=lambda: recordVoice(str(userName.get()), int(seconds.get()), 1))
        voiceRecord.image = microImageRender
        voiceRecord.place(x=180, y=0)

userName = StringVar()

inputName = Entry(tab2, width=20, textvariable=userName)
btnGetVoice = Button(tab2, text='Записать голос',
                  width=20, height=1, command=openVoiceRecorder)
btnGetFace = Button(tab2, text='Сфотографировироваться',
                  width=20, height=1, command=())
inputName.place(x=130, y=30)
btnGetVoice.place(x=130, y=60)
btnGetFace.place(x=130, y=90)



tabContol.pack(expand=1, fill="both")
mainApp.mainloop()
