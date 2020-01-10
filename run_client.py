"""client to connect to server"""
import socket

ip = input("Enter host ip (Press enter to keep it default) : ")

if ip == "":
    conn = socket.socket()
    conn.connect(("127.0.0.1", 8080))
else:
    conn = socket.socket()
    conn.connect((ip, 8080))

    
def respond(inp):
    if inp == "":
        return
    if INP == "quit":
        conn.send(str.encode(INP))
        response = conn.recv(4096)
        print("Server -> " + str(response, "utf-8"))
        exit()
    conn.send(str.encode(INP))
    response = conn.recv(4096)
    print("Server -> " + str(response, "utf-8"))

print("Connected to server!\n")
while True:
    INP = input("Input command -> ")
    respond(INP)
