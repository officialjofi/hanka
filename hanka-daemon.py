#!/usr/bin/env python

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from tornado.ioloop import PeriodicCallback

# def sample():
#   print 'hiiiii'
#   threading.Timer(10, sample).start()

class WSHandler(tornado.websocket.WebSocketHandler):
  # track clients:
  # simplest method is just to keep a list or dict of WSHandler instances:
  clients = []

  def open(self):
    self.clients.append(self)
    # print 'New connection was opened'
    # self.write_message("Welcome to my websocket!")

    # http://tornado.readthedocs.org/en/latest/ioloop.html
    # The callback is called every callback_time milliseconds.
    #  class tornado.ioloop.PeriodicCallback(callback, callback_time, io_loop=None)
    self.callback = PeriodicCallback(self.send_hello, 5000)
    self.callback.start()

  def send_hello(self):
    self.write_message('hello')


  def msg(self,message):
    self.write_message(message)
    threading.Timer(10, self.msg('in timer')).start()
    print 'in msg'+message

#  def on_message(self, message):
#    pass
  def on_message(self, message):
    print 'Incoming message:', message
    self.write_message("You said: " + message)

  def on_close(self):
    self.clients.remove(self)
    print 'Connection was closed...'

application = tornado.web.Application([
  (r'/ws', WSHandler),
])

if __name__ == "__main__":
  print 'server started\n'
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
#   interval_ms=120
  tornado.ioloop.IOLoop.instance().start()

