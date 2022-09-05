import pickle
from threading import Thread
from connection import server


def get_cl(bc):
    print(type(pickle.loads(bc)))
    return pickle.loads(bc)

if __name__ == "__main__":
    server_ = server()
    server_.get_info()
    if server_.connected_users < server_.total_users:
        print('users: ', server_.connected_users)
        print(get_cl(server_.get_byte_code(server_.listening())).first)
        #Tget_cl
    else:
        server.shot_down()
