import logging
import tornado.web
from game import Game

logger = logging.getLogger(__name__)


class GameHandler(tornado.web.RequestHandler):
    """
    Handles one specific game.
    """

    @property
    def db(self):
        return self.application.db

    def get(self, game_id):
        """
        Retrieve a Game by its ID, returning a 404 status code if no game with that ID exists.

        :param game_id: game id
        :return: JSON representation of a game if game exists; 404 otherwise.
        """

        game = Game(self.db, game_id)

        # check if game exits
        if self._exits(game):
            self.write(game.to_json())
            self.finish()

    def post(self, game_id):
        """
        Update the Game with the given ID, replacing its data with the newly POSTed data.

        :param game_id: game id
        """

        game = Game(self.db, game_id)

        # check if game exits
        if self._exits(game):

            # check if game has ended
            if game.ended:
                message = "Game Already Ended."
                logger.info(message)
                self.finish({"message": message})
                return

            # check if user provides a valid next move
            square = self.get_argument("square", None)
            if square is None or not square.isdigit():
                message = "{} did not make a valid move. Try again.".format(game.meta["next_player"])
                logger.info(message)
                self.finish({"message": message})
                return

            square = int(square)
            # check if square is occupied
            if game.square_is_occupied(square):
                message = "Square is occupied. Try again."
                logger.info(message)
                self.finish({"message": message})
            else:
                game.move(square)
                game.persist()
                logger.info("Success.")
                self.finish()

    def _exits(self, game):
        """
        Verify if game exists.

        :param game: game instance.
        :return: true if game exists; false otherwise.
        """

        if not game.exits:
            logger.info("Game {} doesn't exist.".format(game.game_id))
            self.set_status(404)
            self.finish({"message": "Not Found"})
            return False

        logger.info("Game {} exist.".format(game.game_id))
        return True
