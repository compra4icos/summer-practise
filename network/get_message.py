"""

if connection_socket != -1:
            connection_socket.sendall('you connected'.encode('utf-8'))

            message = connection_socket.recv(1024)
            user_name = bytes.decode(message, encoding='utf-8')

            print(user_name, 'connected')
            try:
                while True:
                    try:
                        message = connection_socket.recv(1024)
                        print(user_name, " --> ", bytes.decode(message, encoding='utf-8'))
                    except:
                        self.connected_users-=1
                        print(user_name, ' disconnected')
                        break
            except IOError:
                connection_socket.send("404 Not Found")
                connection_socket.shutdown(SHUT_RDWR)
                connection_socket.close()
        else:
            print('connect error')

"""