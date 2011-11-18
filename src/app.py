import tornado.ioloop
import tornado.web
import tornado.options
import os
import tornadio2
from game import Game

ROOT_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT_PATH, '../public')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', hello_world='Hello, world!')

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html')

class SocketConnection(tornadio2.conn.SocketConnection):
    @classmethod
    def get_game(cls):
        if not hasattr(cls, '_game'):
            cls._game = Game()

            for i in xrange(10):
                cls._game.spawn('Lizard')

        return cls._game

    def on_open(self, info):
        game = self.get_game()
        game.add_participant(self)
        self.emit('game:init', game.serialize())

    def on_message(self, message):
        pass

    def on_close(self):
        game = self.get_game()
        game.remove_participant(self)

application = tornado.web.Application(
    tornadio2.TornadioRouter(SocketConnection,{
        'enabled_protocols': ['websocket', 'xhr-polling', 'jsonp-polling', 'htmlfile'],
    }, namespace='socket').apply_routes([
        (r'/', IndexHandler),
        (r'/test', TestHandler),
        (r'/public/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH})
    ]),
    template_path=os.path.join(ROOT_PATH, '../templates'),
    static_path=STATIC_PATH,
    static_url_prefix='/public/',
    debug=True,
    socket_io_port=8888,
)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    tornadio2.SocketServer(application, auto_start=False)
    tornado.ioloop.IOLoop().instance().start()