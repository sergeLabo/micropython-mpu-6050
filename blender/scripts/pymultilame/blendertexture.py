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
Class générique qui permet de changer la texture d'un objet.
Ce script ne peut tourner que dans blender.
"""


class VirtualGl:
    """
    bge = blender game engine
    Cette class remplace
    from bge import logic
    en dehors du Game Engine.
    """
    pass

    
class VirtualTexture:
    """
    bge = blender game engine
    Cette class remplace
    from bge import logic
    en dehors du Game Engine.
    """
    pass

    
try:
    from bge import logic as gl
except:
    gl = VirtualGl()
try:
    from bge import texture
except:
    texture = VirtualTexture()

    
__all__ = ['TextureChange']




class TextureChange():
    """
    Classe générique utilisable dans d'autres projects,
    pour changer une texture d'un objet.
    """

    def __init__(self, obj, old_tex):
        """
        obj     = objet concerné
        old_tex = image de la texture originale, ex "danseur2.png"
        new_tex = "//textures/perso.png"
        """

        self.old_tex = old_tex
        # ID de la texture existante
        self.ID = texture.materialID(obj, 'IM' + old_tex)
        # Sauvegarde de l'objet python dans le Game Logic
        self.obj_texture = texture.Texture(obj, self.ID)

    def texture_new(self, new_tex):
        """
        Application de la nouvelle image de la texture.

        Répéter la fonction plusieurs fois (ex 5x) pour que
        le changement marche.
        Tous les object avec le matériau seront changés.
        """

        # Nouvelle source
        url = gl.expandPath(new_tex)
        print("Path du fichier", new_tex, "=", url)

        new_source = texture.ImageFFmpeg(url)

        # Remplacement
        self.obj_texture.source = new_source
        self.obj_texture.refresh(False)

    def texture2old(self):
        """
        Effacement de l'objet python, pour retourner à l'ancienne texture.
        """

        try:
            del self.obj_texture
        except:
            print("Problème avec la suppression de la texture:", self.obj_texture)
