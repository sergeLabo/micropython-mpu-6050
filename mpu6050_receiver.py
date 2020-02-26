#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from time import time, sleep
import serial
import ast


class PileFIFO():
    """
    Pile FIFO pour faire des statistiques
    sur les dernières valeurs d'une variable.
    """
    def __init__(self, size):
        """size définit la hauteur de la pile."""

        self.queue = []
        self.size = size
        self.average = 0

    def append(self, new):
        """Ajoute pour avoir une pile constante de size valeurs."""

        # Ajout dans la liste à la fin
        self.queue.append(new)

        # Remplissage de la pile avec la première valeur au premier ajout
        while len(self.queue) < self.size:
            self.queue.append(new)

        # Suppression du plus ancien si la pile fait size + 1
        if len(self.queue) > self.size:
            self.queue.pop(0)

    def average_calcul(self):
        """Maj de la valeur moyenne de la pile."""
        somme = 0
        for i in range(len(self.queue)):
            somme += self.queue[i]
        if len(self.queue) == 0:
            self.average = 0
        else:
            self.average = somme / len(self.queue)

    def inconsistency(self):
        """
        La dernière valeur est-elle cohérente par rapport aux précédentes ?
        à lancer après append et average_calcul
        """

        nb = len(self.queue)
        diff = abs((self.queue[nb - 1] - self.average) / self.average)

        if diff > 0.5:
            # Je supprime la valeur incohérente
            del self.queue[nb - 1]
            # je recalcule
            self.average_calcul()


def datagram_to_dict(data):
    """Décode le message.
    Retourne un dict ou None
    """

    try:
        dec = data.decode("utf-8")
    except:
        print("Décodage UTF-8 impossible")
        dec = data

    try:
        msg = ast.literal_eval(dec)
    except:
        print("ast.literal_eval impossible. Ajouter ast dans les import")
        msg = dec

    if isinstance(msg, dict):
        return msg
    else:
        print("Message reçu: None")
        return None


init = 1
while init:
    try:
        print("Connexion à ttyACM0 ....")
        sleep(1)
        seri = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        print("Connecté à ttyACM0")
        init = 0
    except:
        print("Connexion impossibble à ttyACM0")

t_0 = time()
n = 0
pile_x = PileFIFO(20)
pile_y = PileFIFO(20)
pile_z = PileFIFO(20)

while True:
    rcv = seri.readline()

    data = datagram_to_dict(rcv)

    if data:
        if "gX" in data:
            gX = data["gX"]
        else:
            gX = 0
        if "gX_c" in data:
            gX_c = data["gX_c"]
            pile_x.append(gX_c)
        else:
            gX_c = 0

        if "gY" in data:
            gY = data["gY"]
        else:
            gY = 0
        if "gY_c" in data:
            gY_c = data["gY_c"]
            pile_y.append(gY_c)
        else:
            gY_c = 0

        if "gZ" in data:
            gZ = data["gZ"]
        else:
            gZ = 0
        if "gZ_c" in data:
            gZ_c = data["gZ_c"]
            pile_z.append(gZ_c)
        else:
            gZ_c = 0

        if "aX" in data:
            aX = data["aX"]
        else:
            aX = 0
        if "aX_c" in data:
            aX_c = data["aX_c"]
        else:
            aX_c = 0

        if "aY" in data:
            aY = data["aY"]
        else:
            aY = 0
        if "aY_c" in data:
            aY_c = data["aY_c"]
        else:
            aY_c = 0

        if "aZ" in data:
            aZ = data["aZ"]
        else:
            aZ = 0
        if "aZ_c" in data:
            aZ_c = data["aZ_c"]
        else:
            aZ_c = 0

        print(int(aX_c), int(aY_c), int(aZ_c))

        # #pile_x.average_calcul()
        # #pile_x.inconsistency()
        # #x = pile_x.average

        # #pile_y.average_calcul()
        # #pile_y.inconsistency()
        # #y = pile_y.average

        # #pile_z.average_calcul()
        # #pile_z.inconsistency()
        # #z = pile_z.average

        # #print(int(x), int(y), int(z))

        n += 1
        if time() - t_0 > 1:
            t_0 = time()
            # #print(n)
            n = 0

        sleep(0.01)
