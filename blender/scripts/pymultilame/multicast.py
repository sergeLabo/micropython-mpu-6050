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
Socket multicast
"""


import socket

__all__ = ['Multicast']

class Multicast():
    """Récupère des datas en Multicast."""

    def __init__(self, ip, port, buffer_size=1024):
        self.ANY = "0.0.0.0"
        self.MCAST_ADDR = ip
        self.MCAST_PORT = port
        self.buffer_size = buffer_size
        self.create_sock()

    def create_sock(self):
        """Création d'un socket multicast self.sock."""

        # Création d'un socket

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Allow multiple sockets to use the same PORT number
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to the port that we know will receive multicast data
        self.sock.bind((self.ANY, self.MCAST_PORT))

        # Tell the kernel that we are a multicast socket
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        # Tell the kernel that we want to add ourselves to a multicast group
        # The address for the multicast group is the third param
        status = self.sock.setsockopt(socket.IPPROTO_IP,
                                      socket.IP_ADD_MEMBERSHIP,
                                      socket.inet_aton(self.MCAST_ADDR)\
                                    + socket.inet_aton(self.ANY))

        self.sock.setblocking(False)

        # Limite la taille du buffer UDP pour éviter la latence,
        # le buffer est vidé à chaque lecture
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer_size)

        s = "Socket multicast créé avec IP = {} Port = {} Buffer = {}\n"
        print(s.format(self.MCAST_ADDR, self.MCAST_PORT,
               self.buffer_size))

    def receive(self):
        """Retourne les datas brutes reçue sur multicast."""

        raw_data = None

        raw_data = self.sock.recv(self.buffer_size)

        return raw_data

    def send_to(self, msg, addr):
        """Envoi de msg à addr en multicast."""

        self.sock.sendto(msg, addr)


if __name__ == "__main__":
    # Test
    import json
    from time import sleep

    my_multicast = Multicast("224.0.0.11", 18888, 1024)
    mcast = {"Ip Adress": "192.168.0.102"}
    resp = json.dumps(mcast).encode("utf-8")

    while 1:
        print("envoi")
        sleep(1)
        my_multicast.send_to(resp, ("224.0.0.11", 18888))
        sleep(0.1)
        data = my_multicast.receive()
        print(data)
