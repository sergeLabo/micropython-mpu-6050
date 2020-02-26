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

'''
Ce script est appelé par main_init.main dans blender
Il ne tourne qu'une seule fois pour initier lss variables
qui seront toutes des attributs du bge.logic (gl)
Seuls les attributs de logic sont stockés en permanence.
'''


from bge import logic as gl

from scripts.pymultilame.blendergetobject import get_all_objects
from scripts.pymultilame.myconfig import MyConfig
from scripts.pyboard import PyBoard


def get_conf():
    '''Récupère la configuration depuis le fichier *.ini.'''

    # Le dossier courrant est le dossier dans lequel est le *.blend
    current_dir = gl.expandPath("//")
    print("Dossier courant depuis once.py {}".format(current_dir))
    gl.once = 0

    # TODO: trouver le *.ini en auto
    gl.ma_conf = MyConfig(current_dir + "scripts/mpu6050.ini")
    gl.conf = gl.ma_conf.conf

    print("\nConfiguration du jeu mpu6050:")
    print(gl.conf, "\n")


def init_variable():
    gl.rot = [0] * 3
    gl.frame_coeff = 0
    gl.coeff_done = False
    gl.coeff_x = 1
    gl.coeff_y = 1
    gl.coeff_z = 1

def get_obj():
    gl.all_obj = get_all_objects()
    gl.cube = gl.all_obj["Cube"]
    gl.plane = gl.all_obj["Plane"]
    gl.plane_1 = gl.all_obj["Plane.001"]

def pyboard_init():
    dev = gl.conf["pyboard"]["dev"]
    gl.pyb = PyBoard(dev)


def main():
    '''Lancé une seule fois à la 1ère frame au début du jeu par main_once.'''

    print("Initialisation des scripts lancée un seule fois au début du jeu.")

    # Récupération de la configuration
    get_conf()

    # Init
    init_variable()
    get_obj()
    pyboard_init()


    # Pour les mondoshawan
    print("Initialisation ok")
