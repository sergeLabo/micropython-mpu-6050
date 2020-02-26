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
Lancé à chaque frame durant tout le jeu.
'''


from bge import logic as gl
import mathutils

def main():
    # Récup des datas de la pyboard
    gl.pyb.receive()
    # #set_coeff()
    # #if gl.coeff_done:
        # #set_rotation()

    # #set_rotation_gyro()
    # #set_rotation_angle()
    set_rotation_acc()

def set_rotation_acc():

    alpha = gl.pyb.aX  / 11000 + 0.1
    beta = - gl.pyb.aY / 5000 + 3.3
    gamma = - gl.pyb.aZ / 30000

    print(round(alpha, 2), round(beta, 2), round(gamma, 2))

    # set objects orientation with alpha, beta, gamma in radians
    # #rot_en_euler_cam = mathutils.Euler([alpha, beta, gamma])
    rot_en_euler_cam = mathutils.Euler([1.5, alpha, 0])


    # apply to objects local orientation if ok
    gl.cube.localOrientation = rot_en_euler_cam.to_matrix()

    gl.plane.localScale = 1, 1, beta

def set_rotation_angle():

    alpha = gl.pyb.angleX/90
    beta = - gl.pyb.angleY/90
    gamma = - gl.pyb.angleZ/90 - 0.48

    print(round(alpha, 1), round(beta, 1), round(gamma, 1))

    # set objects orientation with alpha, beta, gamma in radians
    # #rot_en_euler_cam = mathutils.Euler([alpha, beta, gamma])
    rot_en_euler_cam = mathutils.Euler([1.5, gamma, 0])


    # apply to objects local orientation if ok
    gl.cube.localOrientation = rot_en_euler_cam.to_matrix()

    gl.plane.localScale = 1, 1, beta

def set_rotation_gyro():

    alpha = gl.pyb.gX_c  / 20000
    beta = gl.pyb.gY_c / 10000
    gamma = gl.pyb.gZ_c / 10000

    print(round(alpha, 2), round(beta, 2), round(gamma, 2))

    # set objects orientation with alpha, beta, gamma in radians
    rot_en_euler_cam = mathutils.Euler([alpha, beta, gamma])
    rot_en_euler_cam = mathutils.Euler([1.5, gamma, 0])
    # apply to objects local orientation if ok
    gl.cube.localOrientation = rot_en_euler_cam.to_matrix()

    if beta > 0:
        gl.plane.localScale = 1, 1, acc
    else:
        gl.plane_1.localScale = 1, 1, - acc


def set_coeff():
    """calcul de la moyenne sur une seconde"""

    if not gl.coeff_done:

        while gl.frame_coeff < 60:
            gl.coeff_x += gl.pyb.aX
            gl.coeff_y += gl.pyb.aY
            gl.coeff_z += gl.pyb.aZ
            gl.frame_coeff += 1

        gl.coeff_done = True
        gl.coeff_x = (coeff_x/60) / 1600
        gl.coeff_y = (coeff_y/60) / 200
        gl.coeff_z = (coeff_z/60) / 17000
