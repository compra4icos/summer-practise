from pyaudio import paInt16

PYAUDIO = { 
        "CHUNK" : 900,
        "FORMAT" : paInt16,
        "CHANNELS" : 2,
        "RATE" : 44100,
        "RECORD_SECONDS" : 3,
        "INPUT_DEVICE_INDEX" : 0,
        "INPUT" : True,
        "WOUTPUT_PATH" : "voice files/",
    }

NETWORK = {
    "self" : {
        "_ip"     : "127.0.0.1",
        "_port"   : "5005"
    },
    
    "other_pc" : {
        "_ip"     : "127.0.0.1",
        "_port"   : "5016"
    }
}

DESERIALIZATION = {
    "PATH" : "saved files/"
}