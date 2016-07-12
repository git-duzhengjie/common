#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time


class Timer:
    def __init__(self):
        self.start = time()
        self.mylap = time()

    def start(self):
        self.start = time()
        self.mylap = time()

    def stop(self):
        return "%ss" % str(time() - self.start)

    def lap(self):
        tmp = time() - self.mylap
        self.mylap = time()
        return "%ss" % str(tmp)


timer = Timer()
