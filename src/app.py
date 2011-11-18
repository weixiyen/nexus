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
    @classmethod
    def get_game(cls):
        if not hasattr(cls, '_game'):
            from game import Game
            game = Game()
            game.spawn('Lizard')
            game.spawn('Lizard')
            game.spawn('Lizard')
            game.spawn('Lizard')
            game.spawn('Lizard')
            game.spawn('Lizard')
            cls._game = game

        return cls._game

    def on_open(self, info):
        game = self.get_game()
        game.add_participant(self)

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