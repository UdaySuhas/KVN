"""run server"""
from server.server import Server

SER = Server()

if SER.running:
    SER.listen()
