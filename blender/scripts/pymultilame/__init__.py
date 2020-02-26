#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""
    Ce module propose les outils les plus courrant que j'utilise,
    et aussi pour retrouver des syntaxes peu utilisée que je n'ai pas en mémoire,
    et qui nécessiteraient des recherches.
    Les imports réalisé ici facilite les imports dans les scripts:
    Au lieu de:
        from pymultilame.httpdownload import HttpDownload
    faire:
        from pymultilame import HttpDownload
"""

name = "pymultilame"

from pymultilame.httpdownload import HttpDownload
from pymultilame.mytools import MyTools
from pymultilame.tcpclient3 import TcpClient3
from pymultilame.myconfig import MyConfig
from pymultilame.getmyip import get_my_ip
from pymultilame.multicast import Multicast
from pymultilame.udpclient import UdpClient
from pymultilame.fifolist import PileFIFO
from pymultilame.multicast import Multicast
from pymultilame.pathtools import PathTools
from pymultilame.pathtools import ShUtil
from pymultilame.pathtools import Developper

from pymultilame.blendertempo import Tempo
from pymultilame.blendersound import EasyAudio
from pymultilame.blendertexture import TextureChange

from pymultilame.blendergetobject import get_all_objects
from pymultilame.blendergetobject import get_all_scenes
from pymultilame.blendergetobject import get_scene_with_name

from pymultilame.blendertools import droiteAffine
from pymultilame.blendertools import scene_change
from pymultilame.blendertools import print_str_args

from pymultilame.blenderviewport import enable_full_viewport
from pymultilame.blenderviewport import enable_half_viewport
from pymultilame.blenderviewport import enable_stereo_viewport
from pymultilame.blenderviewport import enable_quad_viewport
from pymultilame.blenderviewport import disable_viewport
