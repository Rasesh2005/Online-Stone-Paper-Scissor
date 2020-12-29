import socket
from _thread import start_new_thread
from game import Game
import pickle

IP=socket.gethostbyname(socket.gethostname())
PORT=1234
ADDR=(IP,PORT)
FORMAT="utf-8"

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    server.bind(ADDR)
except Exception as e:
    str(e)

server.listen()
print(f"\n[LISTENING] Listening For Connections...\n")

connected=set()
games={}
idCount=0

def handle_clients(client,p,gameId):
    global idCount
    client.send(str(p).encode(FORMAT))

    while True:
        try:
            data=client.recv(2048*2).decode(FORMAT)
            if gameId in games:
                game=games[gameId]
                if not data:
                    break
                else:
                    if data=="reset":
                        game.reset()
                    elif data!="get":
                        game.play(p,data)
                    client.sendall(pickle.dumps(game))
            else:
                break
        except:
            break
    try:
        del games[gameId]
        print(f"\n[LOST CONNECTION] Closing Game: {gameId}\n")
    except:
        pass
    idCount-=1
    client.close()
def run_server():
    global idCount
    while True:
        client,address=server.accept()
        print(f"\n[NEW CONNECTION] Connected To {address}\n")
        idCount+=1
        gameId=(idCount-1)//2
        p=0
        if idCount%2==1:
            games[gameId]=Game(gameId)
            print(f"\n[NEW GAME] Creating A New Game\n")
        if idCount%2==0:
            games[gameId].ready=True
            p=1
        start_new_thread(handle_clients,(client,p,gameId))

if __name__ == "__main__":
    run_server()