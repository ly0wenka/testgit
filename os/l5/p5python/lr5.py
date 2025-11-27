import sounddevice as sd
from scipy.io.wavfile import write

duration = 5  # тривалість запису в секундах
samplerate = 44100  # частота дискретизації

print("Recording...")
audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
sd.wait()  # чекаємо завершення запису
write('output.wav', samplerate, audio)
print("Saved to output.wav")
