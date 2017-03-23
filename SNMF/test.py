# -*- coding: utf-8 -*-
""" Parser for UCI bag-of-words dataset

Usage: zcat docword.$(data).txt.gz | tail -n +4 | python parse.py vocab.$(data).txt $(min_freq)
- $(data): the name of data (e.g. nips)
- $(min_freq): minimum word frequency to put into a co-occurrence matrix
"""

import sys
from collections import defaultdict
import numpy as np


def _main_func():
    pred = np.ones(long(10))
    pred[:3] = 2
    print pred

_main_func()
