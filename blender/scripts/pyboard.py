#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

########################################################################
# This file is part of MPU 6050.
#
# MPU 6050 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MPU 6050 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
########################################################################


from time import time, sleep
import serial
import ast
import math

class PyBoard:
    def __init__(self, dev):

        self.dev = dev
        self.temps = time()
        init = 1
        while init:
            try:
                print("Connexion à ttyACM0 ....")
                sleep(1)
                self.seri = serial.Serial(self.dev, 57600, timeout=1)
                print("Connecté à ttyACM0")
                init = 0
            except:
                print("Connexion impossibble à ttyACM0")

    def receive(self):

        rcv = self.seri.readline()
        self.seri.reset_output_buffer()
        data = datagram_to_dict(rcv)

        self.gX, self.gY, self.gZ = (0, 0, 0)
        self.gX_c, self.gY_c, self.gZ_c = (0, 0, 0)
        self.aX, self.aY, self.aZ = (0, 0, 0)
        self.aX_c, self.aY_c, self.aZ_c = (0, 0, 0)
        self.angleX, self.angleY, self.angleZ = (0, 0, 0)

        if data:
            if "gX" in data:
                self.gX = data["gX"]
            else:
                self.gX = 0
            if "gX_c" in data:
                self.gX_c = data["gX_c"]
            else:
                self.gX_c = 0

            if "gY" in data:
                self.gY = data["gY"]
            else:
                self.gY = 0
            if "gY_c" in data:
                self.gY_c = data["gY_c"]
            else:
                self.gY_c = 0

            if "gZ" in data:
                self.gZ = data["gZ"]
            else:
                self.gZ = 0
            if "gZ_c" in data:
                self.gZ_c = data["gZ_c"]
            else:
                self.gZ_c = 0

            if "aX" in data:
                self.aX = data["aX"]
            else:
                self.aX = 0
            if "aX_c" in data:
                self.aX_c = data["aX_c"]
            else:
                self.aX_c = 0

            if "aY" in data:
                self.aY = data["aY"]
            else:
                self.aY = 0
            if "aY_c" in data:
                self.aY_c = data["aY_c"]
            else:
                self.aY_c = 0

            if "aZ" in data:
                self.aZ = data["aZ"]
            else:
                self.aZ = 0
            if "aZ_c" in data:
                self.aZ_c = data["aZ_c"]
            else:
                self.aZ_c = 0

            if "angleX" in data:
                self.angleX = data["angleX"]
            else:
                self.angleX = 0
            if "angleY" in data:
                self.angleY = data["angleY"]
            else:
                self.angleY = 0
            if "angleZ" in data:
                self.angleZ = data["angleZ"]
            else:
                self.angleZ = 0

    def angle(self):
        # Calcul en utilisant un filtre complementaire
        # Pour l'utilisation de l'axe Z il est nécessaire d'y adjoindre un magnetometre
        # si on veut des mesures utilisables
        self.temps_precedent = self.temps
        self.temps = time()
        self.intervalle = (self.temps - self.temps_precedent) / 1000
        self.aX = self.accX_calibre / 16384.0  # 16384 pour le choix plage de mesure accelerometre +/- 2g
        self.aY = self.accY_calibre / 16384.0
        self.aZ = self.accZ_calibre / 16384.0
        self.accX_angle = math.degrees (math.atan(self.aY / math.sqrt((self.aX * self.aX) + (self.aZ * self.aZ))))
        self.accY_angle = math.degrees (math.atan(-1 * self.aX / math.sqrt((self.aY * self.aY) + (self.aZ * self.aZ))))
        self.accZ_angle = math.degrees (math.atan(math.sqrt((self.aX * self.aX) + (self.aY * self.aY)) / self.aZ ))
        self.gyroX_angle = self.gyroX_calibre / 131  # 131 pour le choix de mesure +/- 250 deg/s
        self.gyroY_angle = self.gyroY_calibre / 131
        self.gyroZ_angle = self.gyroZ_calibre / 131
        self.AngleX = 0.98 * (self.AngleX + self.gyroX_angle * self.intervalle) + 0.02 * self.accX_angle
        self.AngleY = 0.98 * (self.AngleY + self.gyroY_angle * self.intervalle) + 0.02 * self.accY_angle
        self.AngleZ = 0.98 * (self.AngleZ + self.gyroZ_angle * self.intervalle) + 0.02 * self.accZ_angle
        print(self.AngleX)

def datagram_to_dict(data):
    """Décode le message. Retourne un dict ou None."""

    try:
        dec = data.decode("utf-8")
    except:
        print("Décodage UTF-8 impossible")
        dec = None

    try:
        msg = ast.literal_eval(dec)
    except:
        print("Error: ajouter ast dans les import ou message anormal !")
        msg = None

    if isinstance(msg, dict):
        return msg
    else:
        print("Message reçu: None")
        return None

if __name__ == "__main__":
    pb = PyBoard("/dev/ttyACM0")
    while True:
        pb.receive()
        pb.angle()
        print(pb.angleX)
