#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
(C) 2016 Unicall

live chat server demo

@author: chenbingfeng
'''

import json
import random

from gevent import pywsgi, sleep
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocketError


ws_dict = {}
class WebSocketApp(object):
    '''Send random data to the websocket'''

    def __call__(self, environ, start_response):
        #print environ
        ws = environ['wsgi.websocket']
        ws_dict[environ['HTTP_SEC_WEBSOCKET_KEY']] = ws
        try:
            while True:
                message = ws.receive()
                for (k,v) in ws_dict.items():
                    v.send(message)
            #sleep(0.5)
        except WebSocketError:
            print "websocket dead"
            del ws_dict[environ['HTTP_SEC_WEBSOCKET_KEY']]
            
print  "start"
server = pywsgi.WSGIServer(("", 8099), WebSocketApp(),
    handler_class=WebSocketHandler)
server.serve_forever()