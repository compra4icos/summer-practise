from time import time
import wave
import time
from setting import DESERIALIZATION
import os

"""
def des(file: str, *, fix_imports=True, encoding='ASCII', errors='strict', buffers=None):
    with open(file, 'rb') as outfile:
        obj = pickle.load(outfile)
    return obj
"""

def ob(obj):
    path: str = DESERIALIZATION["PATH"] + str(time.perf_counter()) + "/"
    os.mkdir(path)
    cr_wav(obj, path)
    js(obj, path)

def cr_wav(obj, path):
    with wave.open(f"{path}test.wav", 'wb') as wf:
        wf.setnchannels(obj.channels)
        wf.setsampwidth(obj.py_audio.get_sample_size(obj.format))
        wf.setframerate(obj.rate)
        wf.writeframes(b''.join(obj.frames))

def js(obj, path):
    with open(f"{path}data.json", "w") as wf:
        obj.toJson(wf)


