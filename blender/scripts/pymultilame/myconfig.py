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
Charge une configuration à partir d'un fichier *.ini

Le fichier ini doit être défini avec son chemin absolu

Pour un projet python:
    import os
    dossier = os.path.dirname(os.path.abspath(__file__))
    ou
    os.getcwd()

Pour un projet Blender, le chemin complet est trouvé avec:
    bge.logic.expandPath()
"""


import os
import ast
from configparser import SafeConfigParser

__all__ = ['MyConfig']

class MyConfig():
    """
    Charge la configuration depuis le fichier *.ini,
    sauve les changement de configuration,
    enregistre les changements par section, clé.
    """

    def __init__(self, ini_file, verbose=1):
        """
        Charge la config depuis un fichier *.ini
        Le chemin doit être donné avec son chemin absolu.
        """

        self.conf = {}
        self.ini = ini_file
        self.verbose = verbose
        self.load_config()
        

    def load_config(self):
        """Lit le fichier *.ini, et copie la config dans un dictionnaire."""

        parser = SafeConfigParser()
        parser.read(self.ini, encoding="utf-8")

        # Lecture et copie dans le dictionnaire
        for section_name in parser.sections():
            self.conf[section_name] = {}
            for key, value in parser.items(section_name):
                self.conf[section_name][key] = ast.literal_eval(value)

        if self.verbose:
            print("\nConfiguration chargée depuis {}".format(self.ini))

        # Si erreur chemin/fichier
        if not self.conf:
            print("Le fichier de configuration est vide")
        
    def save_config(self, section, key, value):
        """
        Sauvegarde dans le fichioer *.ini  avec section, key, value.
        Uniquement int, float, str
        """

        if isinstance(value, int):
            val = str(value)
        if isinstance(value, float):
            val = str(value)
        if isinstance(value, str):
            val = """ + value + """

        config = SafeConfigParser()
        config.read(self.ini)
        config.set(section, key, val)
        with open(self.ini, "w") as f:
            config.write(f)
        f.close()
        if self.verbose:
            print("{1} = {2} saved in {3} in section {0}\n".format(section, key, val, self.ini))


if __name__ == "__main__":

    dossier = os.path.dirname(os.path.abspath(__file__))
    print("dossier", dossier)

    dossier_a = os.getcwd()
    print("dossier_a", dossier_a)

    ma_config = MyConfig(dossier_a + "/example.ini")
    a = ma_config.conf
    # conf est un dictionnaire avec tous les paramètres
    print(a)
