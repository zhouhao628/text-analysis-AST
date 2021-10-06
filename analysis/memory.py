# -*- coding: utf-8 -*

import gc
import getopt
import os
import psutil
import sys
import time

from analysis import utils
from east.asts import base


def memory_usage():
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    mem = process.get_memory_info()[0] / f