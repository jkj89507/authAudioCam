import librosa as lr
import numpy as np
import time
from recordAudio import recordVoice

def recognitionVoice(nameFirstAudio: str, nameSecondAudio: str):
    SR = 16000 # Частота дискретизации

    def process_audio(aname):
      audio, _ = lr.load(aname, sr=SR) # Загружаем трек в память

      # Извлекаем коэффициенты
      afs = lr.feature.mfcc(audio, # из нашего звука
                            sr=SR, # с частотой дискретизации 16 кГц
                            n_mfcc=34, # Извлекаем 34 параметра
                            n_fft=2048) # Используем блоки в 125 мс
      # Суммируем все коэффициенты по времени
      # Отбрасываем два первых, так как они не слышны человеку и содержат шум
      afss = np.sum(afs[2:], axis=-1)

      # Нормализуем их
      afss = afss / np.max(np.abs(afss))

      return afss

    def confidence(x, y):
      return np.sum((x - y)**2) # Евклидово расстояние
      # Меньше — лучше

    ## Загружаем несколько аудиодорожек
    return confidence(process_audio(nameFirstAudio), process_audio(nameSecondAudio))