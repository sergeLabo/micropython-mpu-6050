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

__all__ = [ 'enable_full_viewport',
            'enable_half_viewport',
            'enable_stereo_viewport',
            'enable_quad_viewport',
            'disable_viewport'
            ]

class VirtualRender:
    """
    bge = blender game engine
    Cette class remplace
    from bge import logic
    en dehors du Game Engine, pour le module
    """
    pass

try:
    from bge import render
except:
    render = VirtualRender()


def enable_full_viewport(cam):
    """
    cam is blender object
    """

    W = render.getWindowWidth()
    H = render.getWindowHeight()
    cam.setViewport( 0, 0, W, H)
    cam.useViewport = True
    print("Camera {0} is full viewport".format(cam.name))

def enable_half_viewport(cam1, cam2):
    """
    cam1 and 2 are blender objects
    """

    W = render.getWindowWidth()
    H = render.getWindowHeight()
    B = int(H/2)
    cam1.setViewport( 0, 0, W, B)
    cam1.useViewport = True
    cam2.setViewport( 0, B, W, H)
    cam2.useViewport = True
    print("Cameras {0} and {1} are half viewport".format(cam1.name, cam2.name))

def enable_stereo_viewport(cam1, cam2):
    """
    cam1 and 2 are blender objects
    """

    W = render.getWindowWidth()
    H = render.getWindowHeight()
    A = int(W/2)
    cam1.setViewport( 0, 0, A, H)
    cam1.useViewport = True
    cam2.setViewport( A, 0, W, H)
    cam2.useViewport = True
    print("Cameras {0} and {1} are stereo viewport".format(cam1.name, cam2.name))

def enable_quad_viewport(cam1, cam2, cam3, cam4):
    """
    cam1 2 3 4 are blender objects
    """

    W = render.getWindowWidth()
    H = render.getWindowHeight()
    A = int(W/2)
    B = int(H/2)
    cam1.setViewport( 0, 0, A, B)
    cam1.useViewport = True
    cam2.setViewport( A, 0, W, B)
    cam2.useViewport = True
    cam3.setViewport( 0, B, A, H)
    cam3.useViewport = True
    cam4.setViewport( A, B, W, H)
    cam4.useViewport = True
    print("Cameras {0} {1} {2} {3} are quad viewport".format(cam1.name, cam2.name, cam3.name, cam4.name))

def disable_viewport(cam):
    """
    Disable
    """
    cam.useViewport = False
    print("Camera ", cam.name, "is disable")
