#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import subprocess


# python3
print('Imports en python3')

from pymultilame import HttpDownload
from pymultilame import MyTools
from pymultilame import TcpClient3
from pymultilame import MyConfig
from pymultilame import get_my_ip
from pymultilame import Multicast
from pymultilame import UdpClient
from pymultilame import PileFIFO
from pymultilame import Multicast

from pymultilame import Tempo
from pymultilame import EasyAudio
from pymultilame import TextureChange

from pymultilame import scene_change, droiteAffine, scene_change, print_str_args
from pymultilame import get_all_objects, get_all_scenes, get_scene_with_name

print('Tous les imports en python3 sont ok')

# python2
print('\n\nImports en python2')

commands = [['python2', 'from pymultilame.myconfig2 import MyConfig2'],
            ['python2', 'from pymultilame.tcpclient2 import TcpClient2']]

for c in commands:
    p = subprocess.Popen(c,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    output, errors = p.communicate()

    print(output.decode('utf-8'))

print('Tous les imports en python2 sont ok')
