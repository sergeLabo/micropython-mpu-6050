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
Avec twisted en python3:
    Des classes pour créer:
        * un server TCP
        * un client qui se reconnecte

Le serveur et le client ne peuvent pas tourner ensemble dans ce script,
    il n'y a qu"un seul reactor !
"""


import sys
import threading
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor


class MyTCPServer(Protocol):
    """
    Attribut de class: nb_protocol
    Un protocol par client connecté,
    chaque protocol est  une  instance indépendante
    """

    nb_protocol = 0

    def __init__(self):
        self.message = ""
        print("Twisted TCP Serveur créé")

    def connectionMade(self):
        """
        self.factory was set by the factory"s default buildProtocol
        self.transport.loseConnection() pour fermer
        """

        MyTCPServer.nb_protocol += 1
        print("\nConnexion établie avec un client")
        print("Nombre de protocol = {}".format(MyTCPServer.nb_protocol))

    def connectionLost(self, reason):

        MyTCPServer.nb_protocol -= 1
        print("Connexion terminée")
        print("Nombre de protocol = {}\n".format(MyTCPServer.nb_protocol))

    def dataReceived(self, data):

        msg = data.decode("utf-8")
        self.message = msg

        print("Message reçu: {}".format(msg))


class MyTCPServerFactory(Factory):

    # This will be used by the default buildProtocol to create new protocols:
    protocol = MyTCPServer

    def __init__(self, quote=None):
        print("MyTCPServerFactory créé")


class MyTcpClient(Protocol):
    
    def __init__(self):
        print("Un protocol client créé")

    def dataReceived(self, data):

        msg = json.loads(data.decode("utf-8"))
        print("msg {}".format(msg))


class MyTcpClientFactory(ReconnectingClientFactory):
    
    def startedConnecting(self, connector):
        print("Essai de connexion ...")

    def buildProtocol(self, addr):
        print("Connecté à {}".format(addr))
        print("Resetting reconnection delay")
        self.resetDelay()
        return MyTcpClient()

    def clientConnectionLost(self, connector, reason):
        print("Lost connection.  Reason:", reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed. Reason:", reason)
        ReconnectingClientFactory.clientConnectionFailed(self,connector,reason)


def run_tcp_server(port):
    
    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(MyTCPServerFactory())
    reactor.run()

def client(host, port):
    """
    builtins.ValueError: signal only works in main thread
    http://stackoverflow.com/questions/12917980/non-blocking-server-in-twisted
    """

    print("Lancement d'un client host:{} port:{}".format(host, port))

    reactor.connectTCP(host, port, MyTcpClientFactory())
    reactor.run(installSignalHandlers=False)

def client_thread(host, port):
    
    thread_C = threading.Thread(target=client, args=(host, port))
    print("Thread Twisted  Client ....")
    thread_C.start()

def main(opt):
    """
    Le serveur et client ne peuvent pas tourner dans le même script,
    il n'y a qu'un seul reactor !
    """

    host = "192.168.1.17"
    port = 11111

    if opt == "server":
        run_tcp_server(port)
    if opt == "client":
        client_thread(host, port)

if __name__ == "__main__":
    print("""Lancement du script avec:
    python3 labtcptwisted.py server
    ou
    python3 labtcptwisted.py client
    """)

    opt = sys.argv[1]
    main(opt)
