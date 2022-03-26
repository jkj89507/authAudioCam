import speech_recognition as speachRec
from pocketsphinx import LiveSpeech, get_model_path
import time
import os

model_path = get_model_path()

startTime = time.time()
stopTime = 0

microphone = speachRec.Microphone()
recognizer = speachRec.Recognizer()

with microphone as audioFile:
    print("Say something...")
    recognizer.adjust_for_ambient_noise(audioFile)
    audio = recognizer.listen(audioFile)

    try:
        print("Total speeach: ")
        str = ""
        for i in recognizer.recognize_sphinx(audio):
            str += i
        print(str)
        stopTime = time.time()
        spendTime = int(stopTime - startTime)
        sec = spendTime % 60
        min = spendTime // 60
        print(min, "m", sec, "s")
    except Exception as error:
        print("Erorr is ", error)
#
# speech = LiveSpeech(
#     verbose=False,
#     sampling_rate=16000,
#     buffer_size=2048,
#     no_search=False,
#     full_utt=False,
#     hmm=os.path.join(model_path, 'zero_ru.cd_cont_4000'),
#     lm=os.path.join(model_path, 'ru.lm'),
#     dic=os.path.join(model_path, 'ru.dic')
# )
