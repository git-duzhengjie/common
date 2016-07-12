#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv


class CSV:
    def __init__(self, file, filemode, head=0, dialect='excel'):
        try:
            self.hd = head
            if filemode == 'w':
                self.csvfile = open(file, 'wb')
                self.spwr = csv.writer(self.csvfile, dialect)
            elif filemode == 'r':
                self.csvfile = open(file, 'rb')
                self.spre = csv.reader(self.csvfile, dialect)
                if self.spre == None:
                    print 'Failure'
        except IOError as e:
            print("Open file Error: %d: %s" % (e.args[0], e.args[1]))

    def wheader(self, rlist):
        self.spwr.writerow(rlist)

    def wrow(self, rlist):
        self.spwr.writerow(rlist)

    def wrows(self, list):
        self.spwr.writerows(list)

    def getlines(self):
        count = 0
        for line in self.spre:
            count += 1
        return count

    def rheader(self):
        header = []
        i = 0
        for line in self.spre:
            i += 1
            if i > self.hd:
                break
            header.append(line)
        return header

    def readrow(self, nu):
        i = 0
        for line in self.spre:
            i += 1
            if i == nu:
                return line
        return None

    def readrows(self):
        rows = []
        i = 0
        for line in self.spre:
            i += 1
            if i <= self.hd:
                continue
            rows.append(line)
        return rows

    def readrows2strip(self, ch):
        rows = []
        i = 0
        for line in self.spre:
            i += 1
            if i <= self.hd:
                continue
            line[1] = line[1].replace(ch, '')
            rows.append(line)
        return rows

    def getcsvreader(self):
        return self.spre

    def close(self):
        self.csvfile.close()


if __name__ == '__main__':
    f = open('test.f', 'wb')
    sp = csv.writer(f)
    sp.writerow('hh')
    f.close()
