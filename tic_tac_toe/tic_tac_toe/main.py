import redis
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from game_handler import GameHandler
from games_handler import GamesHandler


define("port", default=8888, help="run on the given port", type=int)
define("redis_host", default="127.0.0.1", help="server database host")
define("redis_port", default=6379, help="server database port", type=int)
define("redis_password", default="", help="server database password")
define("redis_database", default=0, help="server database number", type=int)


class Application(tornado.web.Application):
    """
    tic tac toe application.

    It supports four RESTful APIs
        * GET /api/games: Return a list of the Games known to the server, as JSON.
        * POST /api/games: Create a new Game, assigning it an ID and returning the newly created Game.
        * GET /api/games/<id>: Retrieve a Game by its ID, returning a 404 status code if no game with that ID exists.
        * POST /api/games/<id>: Update the Game with the given ID, replacing its data with the newly POSTed data.
    """

    def __init__(self):
        handlers = [
            (r"/api/games/?", GamesHandler),
            (r"/api/games/([0-9]+)/?", GameHandler)
        ]
        super(Application, self).__init__(handlers)

        self.db = redis.Redis(host=options.redis_host,
                              port=options.redis_port,
                              password=options.redis_password,
                              db=options.redis_database)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
