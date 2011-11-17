import tornado.ioloop
import tornado.web
import tornado.options
import os

ROOT_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT_PATH, '../public')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', hello_world='Hello, world!')

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH}),
], template_path=os.path.join(ROOT_PATH, '../templates'), static_path=STATIC_PATH, debug=True)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()