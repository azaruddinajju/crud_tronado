import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


# from tornado.options import define, options

# define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test03.html")
class indexhandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")



def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
    ("/", MainHandler),
    ( "/index.html",indexhandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8898)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()