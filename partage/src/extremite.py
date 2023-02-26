import fcntl
import socket
import os
import select
import time
import traitement

def extOut(HOST,PORT,tun): 
 
    """Cette méthode créee une socket avec les paramètre passé en argument
        HOST : Adresse IP du serveur.
        PORT : Port du serveur.
        tun : Tunnel a utilisé.
    """
    # cette method prend en parametre le host le port et le descripteur de fichier du tun.
    # creation du socket serveur . 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((HOST, PORT))
    while True :
        print("En attende qu'un client ce connecte ...")
        server.listen()
        # attente bloquante qu'un client ce connecte .
        conn, addr = server.accept()
        print(f"le client d'ont l'adressse ip est {addr} est connecter")
        conn.setblocking(0)
        inputs = [tun,conn]
        outputs =[tun,conn]
        # Les listes suivantes sont des buffers qui vont stocker les donner prête à être erite pour le tunnele est la socket
        tunBuffer = []
        socketBuffer = []   
        while True : 
            try :
                # attente boquante que des changement ce font sur les descripteur de fichier tun est conn
                readable, writable, exceptional = select.select(inputs, outputs, inputs)
                # gestion des input
                for s in readable:
                    if s is conn:
                        # on lit la data depuis le socket
                        data = s.recv(1500)
                        print(len(data), ' octets recus la socket')
                        tunBuffer.append(data)
                    elif s is tun:
                        data = s.read(1500)
                        print(len(data), 'octets recus depuis tun0')
                        socketBuffer.append(data)
                #gestion des output 
                for s in writable : 
                    if s is conn : 
                        if len(socketBuffer) > 0 : 
                            data = socketBuffer.pop()
                            s.send(traitement.forward(data))
                    if s is tun : 
                        if len(tunBuffer )> 0: 
                            data = tunBuffer.pop()
                            tun.write(traitement.forward(data))
            except : 
                print("Le client s'est déconnecté")
                break; 


def extIn(HOST,PORT,tun):
    """ Cette méthode créee une socket avec les paramètre passé en argument
        HOST : Adresse IP du serveur.
        PORT : Port du serveur.
        tun : Tunnel a utilisé.
    """
    
    while True: 
        try : 
            print("connexion au serveur ...")
            time.sleep(1)
            client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            print("connextion reussi")
            client.setblocking(0)
            inputs = [tun,client] 
            outputs =[tun,client]
            tunBuffer = []
            socketBuffer = []  
            while True : 
                # listening of anu changes in the fields .
                readable, writable, exceptional = select.select(inputs, outputs, inputs)
                #Handle inputs
                for s in readable:
                    if s is client:
                        # on lit la data depuis la socket .
                        data = s.recv(1500)
                        print(len(data), 'octets recus depuis la socket')
                        tunBuffer.append(data)
                    elif s is tun:
                        data = s.read(1500)
                        print(len(data), 'octets recus depuis tun0')
                        socketBuffer.append(data)
                #handele output 
                for s in writable : 
                    if s is client : 
                        if len(socketBuffer) > 0 : 
                            data = socketBuffer.pop()
                            s.send(traitement.forward(data))
                    if s is tun : 
                        if len(tunBuffer ) > 0: 
                            data = tunBuffer.pop()
                            
                            tun.write(traitement.forward(data))
        except :
            client.close()
            print("connexion perdu !, reconnexion.")