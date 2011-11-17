import tornado.ioloop
import tornado.web
import tornado.options
import os
import tornadio2

ROOT_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT_PATH, '../public')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', hello_world='Hello, world!')

class SocketConnection(tornadio2.conn.SocketConnection):
    participants = set()

    def on_open(self, info):
        self.send('Welcome from the server.')
        self.participants.add(self)

    def on_message(self, message):
        for participant in self.participants:
            if participant != self:
                participant.send(message)

    def on_close(self):
        self.participants.remove(self)

application = tornado.web.Application(
    tornadio2.TornadioRouter(SocketConnection,{
        'enabled_protocols': ['websocket', 'xhr-polling', 'jsonp-polling', 'htmlfile'],
    }, namespace='socket').apply_routes([
        (r'/', IndexHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH})
    ]),
    template_path=os.path.join(ROOT_PATH, '../templates'),
    static_path=STATIC_PATH,
    debug=True,
    socket_io_port=8888,
)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    tornadio2.SocketServer(application, auto_start=False)
    tornado.ioloop.IOLoop().instance().start()