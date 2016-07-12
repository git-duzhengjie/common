# -*- coding: utf-8 -*-
state_file = "config/state"
import sys

def read_state():
    fh = open(state_file, 'r')
    line = fh.readline()
    fh.close()
    lines = line.split('=')
    return int(lines[1])


def write_state():
    fh = open(state_file, 'w')
    fh.write("state=0\n")
    fh.close()


def read_run_model():
    fh = open("config/run_model.ini", 'r')
    line = fh.readline()
    fh.close()
    lines = line.split('=')
    model = int(lines[1])
    if model != 1 and model != 2:
        print("wrong model")
        sys.exit(1)
    return model


def read_gamestart():
    gamestart_file = "./config/gamestart"
    fh = open(gamestart_file, 'r')
    line = fh.readline()
    fh.close()
    lines = line.split("=")
    return lines[1].replace(" ", "").replace("\n", "")

