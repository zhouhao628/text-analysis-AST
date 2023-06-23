# -*- coding: utf-8 -*

import platform

from east import consts


def determine_operating_system():
    system = platform.system()
    bits = platform.architecture()[0]
    if s