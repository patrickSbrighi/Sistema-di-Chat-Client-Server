import socket
import threading

active = False
#Funzione per permettere al client di ricevere messaggi
def receive():
    while active:
        try:
            mess = client.recv(1024).decode("utf-8")
            if mess:
                print(mess)
            else:
                break
        except:
            if active:
                print("Errore durante la ricezione del messaggio")
            break
    client.close()

#Indirizzo e porta del server
HOST = '127.0.0.1'
PORT = 54321

#Il client si connette al server e si attiva
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
    active = True
    print("Benvenuto nel server")
except ConnectionRefusedError:
    print("Impossibile connettersi al server. Assicurati che il server sia in esecuzione.")
    exit()


receive_thread = threading.Thread(target=receive)
receive_thread.start()

try:
    while active:
        message = input()
        if message.lower() == "exit":
            active = False
            client.send(message.encode("utf-8"))
            break
        client.send(message.encode("utf-8"))
except:
    print("Errore durante l'invio del messaggio.")
finally:
    client.close()
    active = False
    receive_thread.join()

