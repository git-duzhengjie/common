# coding:utf-8
# description:
# python version:
# version:v1.0
# author:杜政颉
# time:2016/7/11 15:50
# Copyright 成都简乐互动远景科技公司版权所有®


import asyncore
import os
import socket
import traceback
import select
from util.color import in_green


class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port, handler):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.handler = handler

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = self.handler(sock)


class SelectServer:
    def __init__(self, ip, port):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((ip, port))
            self.s.listen(5)
        except:
            traceback.print_exc()
            os.exit()

    def accept(self, handler):
        inputs = [self.s]
        while 1:
            rs, ws, es = select.select(inputs, [], [], 1)
            for r in rs:
                if r is self.s:
                    clientsock, clientaddr = r.accept()
                    inputs.append(clientsock)
                    print(in_green(u'接受到来自于{0}的连接'.format(clientaddr)))
                else:
                    if not handler(r):
                        inputs.remove(r)

    def __del__(self):
        self.s.close()


class PollServer:
    def __init__(self, ip, port):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((ip, port))
            self.fdmap = {self.s.fileno(): self.s}
            self.s.listen(5)
            self.p = select.poll()
            self.p.register(self.s.fileno(), select.POLLIN | select.POLLERR | select.POLLHUP)

        except:
            traceback.print_exc()
            os.exit()

    def accept(self, handler):
        while 1:
            events = self.p.poll(5000)
            if len(events) != 0:
                if events[0][1] == select.POLLIN:
                    sock, addr = self.s.accept()
                    print(in_green(u'接受到来自于{0}的连接'.format(addr)))
                    handler(sock)

    def __del__(self):
        self.s.close()
