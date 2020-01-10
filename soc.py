"""
Socket to listen to port and attach a request handler to every connection.
"""


import socket
import threading
import os

from .api import RequestHandler

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
