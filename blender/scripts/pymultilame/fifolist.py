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


__all__ = ['PileFIFO']


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


if __name__ == '__main__':

    pile = PileFIFO(5)

    pile.append(1)
    print(pile.queue)

    pile.append(2)
    print(pile.queue)

    pile.append({1: "test"})
    print(pile.queue)
