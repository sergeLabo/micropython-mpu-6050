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
Classe générique qui permet de gérer facilement le son
dans le Blender Game Engine BGE.

gl est le GameLogic, get with : from bge import logic as gl

Appel de cette classe où tous les sons sont dans une liste avec :
    import aud

    soundList = ["boum", ...] avec les fichiers boum.ogg etc...

    Création de l'objet qui est un dictionnaire

    gl.sound = EasyAudio(soundList)
        soit { "boum": fabrique de boum.ogg, ....}
    Joue le son boum
        gl.sound["boum"].play()
    Stop le son
        gl.sound["boum"].stop()
    Idem repeat, pause
"""

from time import sleep

__all__ = ['EasyAudio', 'Factory']


class VirtualGl:
    """
    bge = blender game engine
    Cette class remplace
    from bge import logic
    en dehors du Game Engine
    """
    pass
    
class VirtualAud:
    """
    idem VirtualGl pour aud
    """
    pass
    
try:
    from bge import logic as gl
except:
    gl = VirtualGl()
    
try:
    import aud
except:
    aud = VirtualAud()


class Factory():
    """
    Class usine pour chaque son.
    """
    def __init__(self, audio_file_path, buffered=True):
        """
        audio_file_path = "//audio/comment/boum.ogg"
        buffered = Boolean
        """
        self.device = aud.device()
        # Dictionnaire des fichiers son
        self.sound = gl.expandPath(audio_file_path)

        # Buffer par défaut
        self.buffered = buffered
        # load sound file
        try:
            self.factory = aud.Factory(self.sound)
        except:
            print("Pas de fichier son :", self.sound)
        if self.buffered:
            try:
                self.factory_buffered = aud.Factory.buffer(self.factory)
            except:
                print("Pas de fichier son :", self.sound)

    def set_volume(self, vol):
        """
        Volume
        """
        if not self.buffered:
            self.handle.volume = vol
        if self.buffered:
            self.handle_buffered.volume = vol

    def set_pitch(self, pitch):
        """
        Hauteur
        """
        if not self.buffered:
            self.handle.pitch = pitch
        if self.buffered:
            self.handle_buffered.pitch = pitch

    def play(self, volume=1):
        """
        play the audio, this return a handle to control play/pause/stop
        """

        if not self.buffered:
            self.handle = self.device.play(self.factory)
            self.handle.volume = volume
        if self.buffered:
            self.handle_buffered = self.device.play(self.factory_buffered)
            self.handle_buffered.volume = volume

    def repeat(self, volume=1):
        """
        Repeat
        """
        if not self.buffered:
            self.handle = self.device.play(self.factory)
            self.handle.loop_count = -1
            self.handle.volume = volume
        if self.buffered:
            self.handle_buffered = self.device.play(self.factory_buffered)
            self.handle_buffered.loop_count = -1
            self.handle_buffered.volume = volume

    def pause(self):
        """
        Pause
        """
        if not self.buffered:
            self.handle.pause()
        if self.buffered:
            self.handle_buffered.pause()

    def stop(self):
        """
        Stop
        """
        if not self.buffered:
            self.handle.stop()
        if self.buffered:
            self.handle_buffered.stop()


class EasyAudio(dict):
    """
    Crée une usine pour chaque son, dans un dict.
    """
    def __init__(self, soundList, path, buffered=True):
        """
        soundList = ["boum", ...]
        path example "//audio/comment/"
        """

        for s in soundList:
            audio_file_path = path + s + ".ogg"
            self[s] = Factory(audio_file_path, buffered)
