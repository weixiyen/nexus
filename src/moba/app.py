import tornado.ioloop
import tornado.web
import tornado.options
import os
import tornadio2
import uuid
from instance import Instance

ROOT_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT_PATH, '../../public')

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
        self.instance = Instance.get()

        self.uid = request.get_cookie('uid').value
        self.player = self.instance.add_player(self, request.get_argument('name'))

        state = self.instance.serialize()
        state['me'] = self.player.entity.id

        self.emit('initialize', state)

    @tornadio2.event('attack')
    def attack(self, ability, target_id, position):
        entity = self.player.entity

        if not ability:
            entity.target.set(target_id)
#        else:
#            self.player.ability(ability, target_id, position)

    @tornadio2.event('move')
    def move(self, position):
        entity = self.player.entity

        if entity.health.current: # is alive
            entity.target.set(None)
            entity.movement.move(*position)

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
    template_path=os.path.join(ROOT_PATH, '../../templates'),
    static_path=STATIC_PATH,
    static_url_prefix='/public/',
    debug=True,
    socket_io_port=8888,
)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    tornadio2.SocketServer(application, auto_start=False)
    tornado.ioloop.IOLoop().instance().start()