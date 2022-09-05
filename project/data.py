from datetime import datetime
import json
from pyaudio import PyAudio
from enum import Enum
from pydantic import BaseModel
from setting import PYAUDIO


class TriggerMode(str, Enum):
    end_listen = "end"
    start_listen = "start"
    get_list_id_device = "get"

class Trigger(BaseModel):
    trigger_mode: TriggerMode                  # взаимодействие с программой на удаленной машине
    evice_id : int                      # id девайса
    request : int
    ip : str | list[str]               # отправить одной машине или списку машин по ip
    class Config:  
        use_enum_values = True

class Event():
    def __init__(self) -> None:
        self.is_set: bool = True
    def __str__(self) -> str:
        pass


class MyData():

    input_device_index: int     = PYAUDIO["INPUT_DEVICE_INDEX"]
    format: int                 = PYAUDIO["FORMAT"]
    channels: int               = PYAUDIO["CHANNELS"]
    rate: int                   = PYAUDIO["RATE"] 
    input: bool                 = PYAUDIO["INPUT"]
    record_seconds: int         = PYAUDIO["RECORD_SECONDS"]
    chunk: int                  = PYAUDIO["CHUNK"]
    path: str                   = PYAUDIO["WOUTPUT_PATH"]
    py_audio: PyAudio           = None
    ADDR: tuple                 = ()

    def __init__(self) -> None:
        self.frames: list[bytes]         = []
        self.filename: str               = "default"
        self.time_start_listen: datetime = None
        self.time_end_listen: datetime   = None
        self.total_time: datetime        = None
        self.is_valid_data: bool         = False

    def toJson(self, wf):
        json.dump(self.get_info(), wf)
        
    def get_info(self) -> dict:
        print(self.total_time)
        return {
            "name" : self.filename,
            "time info" : {
                "start listen"  : str(self.time_start_listen),
                "end listen"    : str(self.time_end_listen),
                "total time"    : str(self.total_time),
            }
            
        }

    def __str__():
        pass