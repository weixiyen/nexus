import tornado.ioloop
import tornado.web
import tornado.options
import os
import tornadio2
import uuid
import time
from instance import Instance
from entity import Turret

ROOT_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT_PATH, '../public')

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        uid = self.get_cookie('uid')

        if uid is None:
            uid = uuid.uuid4().hex
            self.set_cookie('uid', uid)

        return uid

class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html', hello_world='Hello, world!')

class TestHandler(BaseHandler):
    def get(self):
        self.render('test.html')

class TestCanvasHandler(TestHandler):
    def get(self):
        self.render('test-canvas.html')

class SocketConnection(tornadio2.conn.SocketConnection):
    def on_open(self, request):
        self.instance = Instance.get(request.get_argument('instance'))

        self.uid = request.get_cookie('uid').value
        self.player = self.instance.add_player(self)

        state = self.instance.serialize()
        state['me'] = self.player.id

        self.emit('initialize', state)

    @tornadio2.event('spawn')
    def spawn(self, message):
        for i in xrange(100):
            self.instance.spawn('Lizard')

        self.instance.spawn('Turret', type_=Turret)
        self.instance.spawn('Turret', type_=Turret)
        self.instance.spawn('Turret', type_=Turret)
        self.instance.spawn('Turret', type_=Turret)

    @tornadio2.event('move')
    def move(self, message):
        x, y = message
        st = time.time()
        self.player.move(x, y)
        self.instance.logger.debug('Player A*: %.2f' % (time.time() - st))

    def on_message(self, message):
        pass

    def on_close(self):
        self.instance.remove_player(self)

application = tornado.web.Application(
    tornadio2.TornadioRouter(SocketConnection,{
        'enabled_protocols': ['websocket', 'xhr-polling', 'jsonp-polling', 'htmlfile'],
    }, namespace='socket').apply_routes([
        (r'/', IndexHandler),
        (r'/test', TestHandler),
        (r'/test-canvas', TestCanvasHandler),
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