# -*- coding: utf-8 -*

import sys

from east import utils


def progress(message, step, total):
    if not utils.output_is_redirected():
        sys.stdout.write("\r%s: %i/%