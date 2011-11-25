import tornado.ioloop
import tornado.web
import tornado.options
import os
import tornadio2
import uuid
import venom
from venom import prop, mob

ROOT_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT_PATH, '../public')

_instance = None

def _get_instance():
    global _instance

    if _instance is None:
        instance = _instance = venom.Instance(188, 219)

        for i in xrange(25):
            instance.place(kind=prop.Tree)
            instance.place(kind=prop.Rock)

        for i in xrange(50):
            instance.spawn('Minion',  kind=mob.Minion, hp=50, attack=1)

        # Team Blue
        instance.spawn('Nexus', x=14, y=117, faction='blue', kind=mob.Nexus, sprite='structure/base1.png', hp=1000)
        instance.spawn('Inhibitor', x=28, y=97,faction='blue', kind=mob.Tower, sprite='structure/tower1.png', hp=200, attack=20)
        instance.spawn('Inhibitor', x=34, y=112, faction='blue', kind=mob.Tower, sprite='structure/tower1.png', hp=200, attack=20)
        instance.spawn('Inhibitor', x=28, y=127, faction='blue', kind=mob.Tower, sprite='structure/tower1.png', hp=200, attack=20)

        instance.spawn('Turret', x=62, y=57, faction='blue',kind=mob.Tower, sprite='structure/tower1.png', hp=100, attack=15)
        instance.spawn('Turret', x=62, y=112, faction='blue',kind=mob.Tower, sprite='structure/tower1.png', hp=100, attack=15)
        instance.spawn('Turret', x=62, y=168, faction='blue', kind=mob.Tower, sprite='structure/tower1.png', hp=100, attack=15)

        # Team Pink
        instance.spawn('Nexus', x=174, y=117, faction='pink', kind=mob.Nexus, sprite='structure/base6.png',hp=1000)
        instance.spawn('Inhibitor', x=160, y=97, faction='pink', kind=mob.Tower, sprite='structure/tower2.png', hp=200, attack=20)
        instance.spawn('Inhibitor', x=154, y=112, faction='pink', kind=mob.Tower, sprite='structure/tower2.png', hp=200, attack=20)
        instance.spawn('Inhibitor', x=160, y=127, faction='pink', kind=mob.Tower, sprite='structure/tower2.png', hp=200, attack=20)

        instance.spawn('Turret', x=124, y=62, faction='pink', kind=mob.Tower, sprite='structure/tower2.png', hp=100, attack=15)
        instance.spawn('Turret', x=124, y=121, faction='pink', kind=mob.Tower, sprite='structure/tower2.png', hp=100, attack=15)
        instance.spawn('Turret', x=124, y=168, faction='pink', kind=mob.Tower, sprite='structure/tower2.png', hp=100, attack=15)

        instance.start()

    return _instance

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        uid = self.get_cookie('uid')

        if uid is None:
            uid = uuid.uuid4().hex
            self.set_cookie('uid', uid)

        return uid

class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')

class SocketConnection(tornadio2.conn.SocketConnection):
    def on_open(self, request):
        self.instance = _get_instance()

        self.uid = request.get_cookie('uid').value
        self.player = self.instance.add_player(self, request.get_argument('name'))

        state = self.instance.serialize()
        state['me'] = self.player.id

        self.emit('initialize', state)

    @tornadio2.event('attack')
    def attack(self, ability, target_id, position):
        if not ability:
            self.player.set_target(target_id)
        else:
            self.player.ability(ability, target_id, position)

    @tornadio2.event('move')
    def move(self, position):
        if self.player.is_alive():
            self.player.set_target(None)
            self.player.move(*position)

    def on_message(self, message):
        pass

    def on_close(self):
        self.instance.remove_player(self)

application = tornado.web.Application(
    tornadio2.TornadioRouter(SocketConnection,{
        'enabled_protocols': ['websocket', 'xhr-polling', 'jsonp-polling', 'htmlfile'],
    }, namespace='socket').apply_routes([
        (r'/', IndexHandler),
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