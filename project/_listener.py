from network.connection import server
from threading import Thread
import converter
from listening_controller import controller
from data import MyData
from json import load

data = MyData()

setting: dict = {}
with open("listener_conf.json", "rb") as f:
    setting = load(f)

def lis_ser():
    server_ = server(host=setting["_ip"], port=setting["_port"])
    while True:
        if server_.connected_users < server_.total_users:
            print("start listening...")
            temp = converter.deserialization(server_.get_byte_code(server_.listening()))
            data.ADDR = server_.ADDR
            Thread(target=controller, args=(data, temp, server_), daemon=True).start()
        else:
            server.shot_down()
lis_ser()