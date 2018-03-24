import logging
import json
import tornado.web
from game import Game, decode

logger = logging.getLogger(__name__)


class GamesHandler(tornado.web.RequestHandler):
    """
    Retrieves all games known to the server, and creates new game.
    """

    @property
    def db(self):
        return self.application.db

    def get(self):
        """
        :return: a list of the Games known to the server, as JSON.
        """
        games = list()
        game_ids = decode(self.db.smembers("game_id_list"))

        for game_id in game_ids:
            game = Game(self.db, game_id)
            games.append(game.game)

        logger.info(games)

        self.write(json.dumps(games))
        self.finish()

    def post(self):
        """
        Create a new Game, assigning it an ID and returning the newly created Game.
        It is optional for users to supply player names.

        :return: newly created game as JSON.
        """

        game_id = self.db.incr("game_count")

        player0 = self.get_argument("player0", "player0")
        player1 = self.get_argument("player1", "player1")

        game_meta = {"id": game_id,
                     "player:0": player0,
                     "player:1": player1,
                     "result": None,
                     "next_player": 0}
        self.db.hmset("game:meta:{}".format(game_id), game_meta)

        game_board = {str(i): None for i in range(9)}
        self.db.hmset("game:board:{}".format(game_id), game_board)

        self.db.sadd("game_id_list", game_id)
        logger.info("Game {} is created.".format(game_id))

        game = Game(self.db, game_id)
        self.write(game.to_json())
        self.finish()
