import socket
import threading

#Funzione per la gestione dei client
def clientHandler(clientSocket, addres):
    print(f"Nuova connessione da {addres}")
    mess = "...si è unito alla chat..."
    broadcast(mess, clientSocket)
    while True:
        try:
            mess = clientSocket.recv(1024)
            if not mess or mess.decode("utf-8").lower() == "exit":
                print(f"Connessione da {addres} terminata")
                mess = "...ha abbandonato la chat..."
                broadcast(mess, clientSocket)
                break

            broadcast(mess.decode("utf-8"), clientSocket)

        except ConnectionResetError:
            print(f"Connessione da {addres} terminata in modo anomalo")
            mess = "...ha abbandonato la chat..."
            broadcast(mess, clientSocket)
            break

    clients.remove(clientSocket)
    clientSocket.close()

#Funzione per l'invio dei messaggi a tutti i client tranne il mittente
def broadcast(mess, senderSocket):
    for client in clients:
        if client != senderSocket:
            try:
                newMess = f"{senderSocket.getpeername()}: {mess}"
                client.send(newMess.encode("utf-8"))
            except:
                print("Errore nell'invio del messaggio")

#Configurazione del server
HOST = '127.0.0.1'
PORT = 54321

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

clients = []

print("Il server è pronto...")

#Il server è in ascolto
while True:
    server.listen(5)
    clientSocket, addres = server.accept()

    clients.append(clientSocket)

    client_thread = threading.Thread(target=clientHandler, args=(clientSocket, addres))
    client_thread.start()
