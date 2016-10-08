#!/usr/bin/env python

import os
import time
import sys


def rtouch(path):
    if os.path.isdir(path):
        for sub in os.listdir(path):
            rtouch(path + os.sep + sub)

    os.utime(path, times)


if __name__ == '__main__':
    if 1 == len(sys.argv):
        print('Usage: rtouch.py <dir|file> ...')
        exit()

    now = time.time()
    times = (now, now)

    for item in sys.argv[1:]:
        rtouch(item)
