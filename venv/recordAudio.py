import pyaudio
import wave

def getInputAudioDevices():
    listOfAudioDevices = []
    for i in range(pyaudio.PyAudio().get_device_count()):
        listOfAudioDevices.append(pyaudio.PyAudio().get_device_info_by_index(i)['name'])
    for i in range(0, len(listOfAudioDevices)):
        print(listOfAudioDevices[i])


def recordVoice(nameFile: str, seconds: int, indexInputDevice:int ):
    __chunk = 1024
    __sample_format = pyaudio.paInt16
    __channels = indexInputDevice
    __rate = 44100
    __seconds = seconds

    __interfaceAudio = pyaudio.PyAudio()

    print("Say something....")

    stream = __interfaceAudio.open(format=__sample_format, channels=__channels,
                                   rate=__rate, frames_per_buffer=__chunk,
                                   input_device_index=2, input=True)
    frames = []

    for i in range(0, int(__rate / __chunk * __seconds)):
        data = stream.read(__chunk)
        frames.append(data)

    stream.stop_stream()
    print("Stop recording...")
    stream.close()
    __interfaceAudio.terminate()

    fileWriteVoice = wave.open(nameFile + ".wav", 'wb')
    fileWriteVoice.setnchannels(__channels)
    fileWriteVoice.setsampwidth(__interfaceAudio.get_sample_size(__sample_format))
    fileWriteVoice.setframerate(__rate)
    fileWriteVoice.writeframes(b''.join(frames))
    fileWriteVoice.close()