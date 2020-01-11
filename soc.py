"""
Socket to listen to port and attach a request handler to every connection.
"""


import socket
import threading
import os

from api import RequestHandler

class SocketAttach():
    """
    Socket Attaach module

    Attributes:
    -----------------
        binding_ip_port : tuple(ip, port)
            Ip and port for socket

        session_available : bool
            Session data available

        socket_object : Socket class
            Socket object

        connections : list(conn)
            List of connections

        ips : list(ips)
            List of ips

        threads : dict{ip:thread}
            Thread locking

        connection_api : dict{ip:RequestHandler}
            Attach a request handler to ip

    Methods:
    -----------------
        check_session_files():
            Check session files.

        run_session():
            Run the session.

        attach_socket():
            Attach a socket.

        connection_accept_async():
            Start accepting connections.

        manage_connections():
            Manage connections.

        respond():
            Respond to client response.
    """

    def __init__(self):
        """
        Initialize the attributes.
        """
        self.binding_ip_port = ("", 8080)
        self.session_available = self.check_session_files()
        self.socket_object = self.attach_socket()
        self.connections = []
        self.ips = []
        self.threads = {}
        self.connection_api = {}

    def check_session_files(self):
        """
        Check session can initialize or not.

        Return: bool
            Session available or not.
        """
        if os.path.exists("server_session") and os.path.exists("server_session/server_data"):
            return True
        return False

    def run_session(self):
        """
        Start accepting connections.
        """
        threading.Thread(target=self.connection_accept_async, args=(), daemon=True).start()
        self.manage_connections()

    def attach_socket(self):
        """
        Bind a socket to port 8080.

        Return: Class(Socket)
            Socket object
        """
        socket_object = socket.socket()
        socket_object.bind(self.binding_ip_port)
        socket_object.listen(5)
        print("Successfully opened server at port 8080")
        return socket_object
    def connection_accept_async(self):
        """
        Start accepting connections.
        """
        while True:
            try:
                conn, address = self.socket_object.accept()
                self.socket_object.setblocking(1)
                self.connections.append(conn)
                self.ips.append(address)
                self.threads[address] = False
                self.connection_api[address] = RequestHandler()
                print("Connection established from ip :" + address[0])
            except:
                print("Error in accepting connections")
                
    def manage_connections(self):
        """
        Handle threads and its locks.
        """
        while True:
            for conn, address in zip(self.connections, self.ips):
                try:
                    if not self.threads[address]:
                        threading.Thread(target=self.respond, args=(conn, address), daemon=True).start()
                except:
                    pass

    def respond(self, conn, addr):
        """
        Respond to the client.
        """
        try:
            self.threads[addr] = True
            client_res = str(conn.recv(4096), "utf-8")
            response = self.connection_api[addr].respond(client_res)
            encoded_str = str.encode(response)
            conn.send(encoded_str)
            self.threads[addr] = False
        except Exception as exps:
            print(exps)

