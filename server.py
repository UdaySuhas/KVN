"""
Main server class, socket attacher to attach socket.
"""

from .soc import SocketAttach

class Server():
    """
    Server class to attach socket and requests.

    Attributes:
    -----------------
        soc : Class(SocketAttach)
            Class to handle all socket connections.

        running : bool
            Is server running.

    Methods:
    -----------------
        listen():
            Listen to the clients.

        shutdown():
            Detach a socket.

    """
    def __init__(self):
        self.soc = SocketAttach()
        self.running = True

    def listen(self):
        """
        Start listening to clients.
        """
        if self.soc.session_available:
            self.soc.run_session()
            self.running = False
        else:
            self.shutdown()
            print("Error in opening session files!")

    def shutdown(self):
        """
        Detach a socket
        """
        self.soc = None
        self.running = False
