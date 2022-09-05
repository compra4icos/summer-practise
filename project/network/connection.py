from socket import * 
import ssl
import sys
import traceback
import json


version_dict = {
    "tlsv1.0" : ssl.PROTOCOL_TLSv1,
    "tlsv1.1" : ssl.PROTOCOL_TLSv1_1,
    "tlsv1.2" : ssl.PROTOCOL_TLSv1_2,
    "sslv23"  : ssl.PROTOCOL_SSLv23,
}

protocols_dict:dict[str, SocketKind] = {
    "UDP" : SOCK_STREAM,
    "TCP" : SOCK_DGRAM,
}

client_identifiers: dict[str, int] = {}

conf_file = open('network/config/conf.json', 'r')
data = json.load(conf_file)


class connect:
    def __init__(self):
        self.HOST = data['connect']['node_data']['host']
        self.PORT = int(data['connect']['node_data']['port'])
        self.ssl_version = None
        self.ciphers = None
        self.certfile = data['connect']['path']['certfile']
        self.keyfile = data['connect']['path']['keyfile']

    def _get_ssl_context(self, *, CLIENT_AUTH = None):
        if self.ssl_version is not None and self.ssl_version in version_dict:
            #создание ssl контекста(принимает версию протокола)
            sslContext = ssl.SSLContext(version_dict[self.ssl_version])
            print("ssl_version OK - ", self.ssl_version)
        else:
            #создание ssl контекста по умолчанию
            sslContext = ssl.create_default_context() if CLIENT_AUTH == None else ssl.create_default_context(CLIENT_AUTH)
        if self.ciphers is not None:
            #задание шифра
            sslContext.set_ciphers(self.ciphers)
            print("ciphers OK - ", self.ciphers)
        return sslContext

    def _hend_shake():
        pass

    def _get_message_text(connection_socket, *, buffer_size = 8, encoding: str = "utf-8"):
        return connection_socket.recv(buffer_size)

    def _send_message_text(connection_socket, message: str, *, encoding: str = "utf-8"):
        connection_socket.sendall(message.encode(encoding))

    def get_info(self):
        print("version - ", self.ssl_version, "ciphers - ", self.ciphers, "certfile - ", self.certfile,\
                        "keyfile - ", self.keyfile, "HOST - ", self.HOST, "PORT - ", self.PORT)


class server(connect):
    def __init__(self, *, protacol:str=data['connect']['node_data']['protacol'],
                    total_users:int=int(data['connect']['node_data']['total_users']),
                    port = data['connect']['node_data']['port'],
                    host = data['connect']['node_data']['host']):
        connect.__init__(self)
        self.PORT = port
        self.HOST = host
        self.server_socket: socket  = socket(AF_INET, protocols_dict[protacol]) 
        self.server_socket.bind((host, eval(str(port))))
        self.total_users: int       = total_users
        self.server_socket.listen(self.total_users)
        self.connected_users: int   = 0
        self.user_name: str         = ""
        self.ADDR: tuple            = ()
        

    #####################################################################
    def get_ssl_wrap_socket(self, sock):
        sslContext = self._get_ssl_context(CLIENT_AUTH=ssl.Purpose.CLIENT_AUTH)
        sslContext.load_cert_chain(self.certfile, self.keyfile)
        try:
            return sslContext.wrap_socket(sock, server_side = True)
        except ssl.SSLError as message:
            print(f"wrap socket failed, {message}")
            print(traceback.format_exc())
    #####################################################################

    def get_byte_code(self, connection_socket, *, buffer_size = 2048, encoding = "utf-8"):
        """function get byte code of object"""
        if connection_socket != -1:                                     ###########
            try:
                return connection_socket.recv(buffer_size)
            except IOError:
                connection_socket.send("404 Not Found")
                connection_socket.shutdown(SHUT_RDWR)
                connection_socket.close()
        else:
            print('connect error')

    
    def get_byte_line(self, connection_socket, *, path="arhive_getting.zip", buffer_size = 2048, encoding = "utf-8"):
        try:
            file = open(path, "wb")
            data = connection_socket.recv(buffer_size)
            while data != b"end":
                file.write(data)
                data = connection_socket.recv(buffer_size)
            file.close()

        except socket.error:
            print('ERROR: Send failed')
            connection_socket.shutdown(SHUT_RDWR)
            connection_socket.close()
            sys.exit(-1)


    def listening(self):
        newSocket, addr = self.server_socket.accept()
        self.ADDR = addr
        connection_socket =  self.get_ssl_wrap_socket(newSocket)
        self.connected_users+=1
        return -1 if not connection_socket else connection_socket

    def shot_down(self):
        self.connected_users-=1
        print(self.user_name, ' disconnected')
        self.server_socket.close()
        sys.exit(0)

class client(connect):    
    def __init__(self, *, port = data['connect']['node_data']['port'],
                    host = data['connect']['node_data']['host']):
        connect.__init__(self)
        self.PORT = port
        self.HOST = host
        self.certfile = None    
        self.hostname = 'localhost'
       
    def send_byte_code(self, byte_code: bytes, *, path="", ip="127.0.0.1",
                        protacol:str=data['connect']['node_data']['protacol'],
                        port = data['connect']['node_data']['port'],
                        host = data['connect']['node_data']['host']):
        self.client_socket = socket(AF_INET, protocols_dict[protacol])
        self.ssl_socket = self.get_ssl_wrap_socket(self.client_socket)
        self.ssl_socket.connect((host, eval(str(port))))
        try:
            self.ssl_socket.send(byte_code)
        except IOError:
            print('ERROR: Send failed')
            self.ssl_socket.shutdown(SHUT_RDWR)
            self.ssl_socket.close()
            sys.exit(-1)

    def send_byte_line(self, *, path, buffer_size = 2048, encoding = "utf-8",
                            protacol:str=data['connect']['node_data']['protacol'],
                            port = data['connect']['node_data']['port'],
                            host = data['connect']['node_data']['host']):
        self.client_socket = socket(AF_INET, protocols_dict[protacol])
        self.ssl_socket = self.get_ssl_wrap_socket(self.client_socket)
        self.ssl_socket.connect((host, eval(str(port))))
        try:
            f = open(path, "rb")
            data = f.read(buffer_size)
            while data:
                print(f"{data} \n\n")

                self.ssl_socket.send(data)
                data = f.read(buffer_size)
            self.ssl_socket.send(b"end")
            f.close()

        except IOError:
            print('ERROR: Send failed')
            self.ssl_socket.shutdown(SHUT_RDWR)
            self.ssl_socket.close()
            sys.exit(-1)

        
            
    def get_ssl_wrap_socket(self, sock):
            ssl_context = self._get_ssl_context()
            try:
                if self.certfile is not None and self.keyfile is not None:
                    ssl_context.verify_mode = ssl.CERT_REQUIRED
                    ssl_context.check_hostname = True
                    ssl_context.load_verify_locations(self.certfile, self.keyfile)
                    print("ssl OK certfile - ", self.certfile, "keyfile - ", self.keyfile)
                    return ssl_context.wrap_socket(sock, server_hostname = self.hostname)
                else:
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                    ssl_context.load_default_certs()
                    return ssl_context.wrap_socket(sock)
            except ssl.SSLError:
                print("wrap socket failed")
                print(traceback.format_exc())
                self.sock.close()
                sys.exit(-1)
