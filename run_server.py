"""run server"""
from .server import Server

SER = Server()

if SER.running:
    SER.listen()
