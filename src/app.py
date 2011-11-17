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
    # Class level variable
    participants = set()

    def on_open(self, info):
        self.send('Welcome from the server.')
        self.participants.add(self)

    def on_message(self, message):
        # Pong message back
        for p in self.participants:
            p.send(message)

    def on_close(self):
        self.participants.remove(self)

application = tornado.web.Application(
    tornadio2.TornadioRouter(SocketConnection).apply_routes([
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
    tornadio2.SocketServer(application)