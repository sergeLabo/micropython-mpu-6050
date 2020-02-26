#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#######################################################################
# Copyright (C) La Labomedia August 2018
#
# This file is part of pymultilame.

# pymultilame is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pymultilame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pymultilame.  If not, see <https://www.gnu.org/licenses/>.
#######################################################################


"""
Recréer un socket avant chaque envoi ou réception, résoud les problèmes
de réseau, ça se reconnecte tout seul.
Par contre, le port éphémère du recvfrom changera à chaque fois.
"""

import socket

__all__ = ['UdpClient']

class UdpClient():
    """
    Envoi et reception en UDP.
    Cette classe n'encode pas le message à envoyer.
    """

    def __init__(self, buffer_size=1024, timeout=0.01):
        """
        Création d'un socket UDP.
        buffer_size = entier, permet de vider le buffer à chaque lecture,
        pour avoir toujours la dernière valeur.
        """

        self.buffer_size = buffer_size
        self.timeout = timeout

        # Socket UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Le try de réception dure maxi le timeout
        self.sock.settimeout(self.timeout)

        # test car error avec asyncio
        self.sock.setblocking(False)

        # This option set buffer size
        # Every self.sock.recv() empty the buffer,
        # so we have always the last incomming value
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer_size)

    def bind(self, addr):
        """Quelle est la différence avec connect ?"""

        self.sock.bind(addr)

    def connect(self, addr):
        """Connexion à l'adresse pour recevoir addr = tuple."""

        self.sock.connect(addr)

    def send_to(self, req, address):
        """Envoi à l'adresse = (ip, port)."""

        self.sock.sendto(req, address)

    def listen(self):
        """Retourne les datas et l'adresse reçue."""

        try:
            raw_data, addr = self.sock.recvfrom(self.buffer_size)
            return raw_data, addr
        except:
            print('Pas de réception')
        return None, None

    def close(self):
        self.sock.close()
        self.sock = None


def test_client_server():
    from time import sleep
    sender_thread()
    
    # Réception
    clt_receive = UdpClient()
    while 1:
        data, addr = clt_receive.listen()
        if data:
            print(data, addr)
        sleep(0.1)

def sender():
    import json
    from time import sleep
    for i in range(10):   
        # Envoi
        clt_send = UdpClient()

        msg = {"quit": 1}
        msg = "quit"
        data = json.dumps(msg).encode("utf-8")
        print('Envoi de: ', data)
        clt_send.send_to(data, ("192.168.0.102", 8000))
        clt_send.close()
        sleep(0.1)

def sender_thread():
    import threading
    thread_send = threading.Thread(target=sender)
    thread_send.start()
        
def test_OSC():
    from time import sleep
    from OSC3 import OSCClient, OSCMessage
    import json
        
    receiver_thread()
    
    clt = OSCClient()
    address = ("127.0.0.1", 8080)
    
    for i in range(10):
        msg = OSCMessage("/info")
        sleep(0.1)
        msg.append(i)
        try:
            clt.sendto(msg, address)
            print("msg envoyé", msg)
        except:
            print("msg non envoyé")
            
    # Test d'envoi
    for nb in range(10):
        clt_send = UdpClient()

        data = {"phone": nb}
        data = json.dumps(data).encode("utf-8")

        clt_send.send_to(data, ("127.0.0.1", 9999))

        print("Envoi de {}".format(data))

        clt_send.close()

        # 60 Hz
        sleep(0.1)

def receiver():
    from time import sleep
    
    clt_receive = UdpClient()
    while 1:
        data, addr = clt_receive.listen()
        if data:
            print(data, addr)
        sleep(0.01)
        
def receiver_thread():
    import threading
    thread_send = threading.Thread(target=receiver)
    thread_send.start()
          
if __name__ == "__main__":
    """Ne finit pas: il manque une fin sur les threads"""
    
    test_OSC()
    
    test_client_server()
