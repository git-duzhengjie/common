#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from util.time_utility import *
from util.readstate import read_run_model

sys.path.append('log')


class LOG:
    def __init__(self, logname=None):
        model = read_run_model()
        if model == 1 and logname is None:
            logname = "daily_run"
        if model == 2 and logname is None:
            logname = "daily_run_2"
        self.logname = 'log/%s/' % logname
        self.today = today()
        self.f = open(self.logname + self.today, 'a')

    def dumplog(self, log):
        if self.today != today():
            self.today = today()
            self.f.close()
            self.f = open(self.logname + self.today, 'a')
        self.f.write(log + '\n')
        self.f.flush()
        print log

    def __del__(self):
        self.f.close()


mylog = LOG()
