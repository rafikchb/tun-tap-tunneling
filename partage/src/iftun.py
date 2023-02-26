# source de la function "tunalloc" : https://jvns.ca/blog/2022/09/06/send-network-packets-python-tun-tap/
import os
import struct
from fcntl import ioctl
# Décommenter la ligne suivante si la valeur de retour de la methode tunalloc a etait changer par , tun.fileno()
# tunList = []

def tunalloc(tunName):
    tunName = str.encode(tunName)
    # ce code est l'equivalent du programe tunnaloc.c donnee dans le TP
    # retourne un objet de type "file object", et non pas un entier afin d'utiliser l'entier descripteur de fichier 
    # il faut utilise tun.fileno().
    tun = open("/dev/net/tun", "r+b", buffering=0)
    LINUX_IFF_TUN = 0x0001
    LINUX_IFF_NO_PI = 0x1000
    LINUX_TUNSETIFF = 0x400454CA
    flags = LINUX_IFF_TUN 
    ifs = struct.pack("16sH22s", tunName, flags, b"")
    ioctl(tun, LINUX_TUNSETIFF, ifs)
    # Décommenter la ligne suivante si la valeur de retour de la method tunalloc a etait changer par , tun.fileno()
    # tunList.append(tun)
    # return tun.fileno()
    return tun

def streamBetween(src , dest):
    # attention cette boucle est bloquante .
    while True :
        # 1500 représente la taille du buffer en octet.
        data = os.read(src , 1500)
        if (len(data) > 0):
            os.write(dest , data)