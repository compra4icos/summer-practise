import pickle
import json



def get_trigger_js(path: str):
    with open("triger_/triger_get_id_device.json", "rb") as rf:
        json.load(rf)
###########  !!!!!!!!!!!!!!!!!!!!!!!!!

import pyaudio
pyaudio.Stream
def serialization(object: object) -> bytes:
    return pickle.dumps(object)

def deserialization(byte_code: bytes) -> object:
    return pickle.loads(byte_code)