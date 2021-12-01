import socket, threading

class SnakeServer:
    
    connections = []
    
    def remove_connection(self, connection: socket.socket):
        connection.close()
        self.connections.remove(connection)
        
    def removeAllConnections(self):
        for conn in self.connections:
            self.remove_connection(conn)
            
    def broadcast(self, msg):
    
        for conn in self.connections:
            try:
                conn.send(msg)
            except Exception as e:
                print('Error broadcasting message: {e}')
                self.remove_connection(conn)
        
    def handle_user_connection(self, connection: socket.socket):
    
        while True:
            try:

                msg = connection.recv(1024)

                # decode socet message
                result = msg.decode()
                print('server: ' + result)
                self.broadcast(msg)
                #connection.send(result.encode())

            except Exception as e:
                print(f'Error to handle user connection: {e}')
                self.remove_connection(connection)
                break
            
    def startServerAsync(self):
        threading.Thread(target=self.startServer).start()
        
    def startServer(self):
    
        LISTENING_PORT = 1236
        
        try:

            socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_instance.bind(('', LISTENING_PORT))
            socket_instance.listen(4)

            print('Server running!')
            
            while True:

                socket_connection, address = socket_instance.accept()
                self.connections.append(socket_connection)
                
                threading.Thread(target=self.handle_user_connection, args=[socket_connection]).start()

        except Exception as e:
            print(f'An error has occurred when instancing socket: {e}')
        finally:
            self.removeAllConnections()
            socket_instance.close()
            
server = SnakeServer()
server.startServer()