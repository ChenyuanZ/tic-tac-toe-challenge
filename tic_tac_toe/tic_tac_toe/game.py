import functools
import json
import logging

logger = logging.getLogger(__name__)


def decode(data):
    """
    Explicitly decode with utf-8.
    """

    if type(data) is dict:
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()}
    elif type(data) is set:
        return [item.decode('utf-8') for item in data]


class Game(object):
    """
    class Game represents a game.

    """

    def __init__(self, db, game_id):
        self.db = db
        self.game_id = game_id
        self.meta_id = "game:meta:{}".format(game_id)
        self.board_id = "game:board:{}".format(game_id)

        if self.exits:
            self.meta = {k: v if v != "None" else None for k, v in decode(self.db.hgetall(self.meta_id)).items()}
            self.board = {int(k): int(v) if v != "None" else None for k, v in
                          decode(self.db.hgetall(self.board_id)).items()}

    @property
    def game(self):
        """
        Read-only attribute.
        :return: dictionary representation of a game.
        """

        game = self.meta
        game["board"] = self.board

        return game

    @property
    def win_combination(self):
        """
        :return: all possible winning combinations
        """

        return [[0, 1, 2],
                [0, 3, 6],
                [0, 4, 8],
                [1, 4, 7],
                [2, 4, 6],
                [2, 5, 8],
                [3, 4, 5],
                [6, 7, 8]]

    @property
    def exits(self):
        """
        Check if a game exists.
        :return: true if game exists in Redis; false otherwise.
        """

        return self.db.sismember("game_id_list", self.game_id)

    @property
    def ended(self):
        """
        Check if a game is ended.
        :return: true if game is ended; false otherwise.
        """

        return self.meta["result"] is not None

    def square_is_occupied(self, square):
        """
        Check if a square is occupied.
        :param square: square to check
        :return: true if it is occupied; false otherwise.
        """

        return self.board[square] is not None

    def move(self, square):
        """
        Pre-condition:
            1. square is not occupied.
            2. game is not ended.

        Assign square to the next_player.
        Assign the other player as next_player to take turns.
        Update result.

        :param square: a square in a board.
        """

        current_player_code = int(self.meta["next_player"])

        self.board[square] = current_player_code
        self.meta["next_player"] = 1 if current_player_code == 0 else 0
        logger.info("{} made a move at {}".format(self.meta["player:{}".format(current_player_code)], square))

        # compute result
        status = {0: list(),
                  1: list()}
        for k, v in self.board.items():
            if v is not None:
                status[v].append(k)

        for k, v in status.items():
            v.sort()
            if v in self.win_combination:
                self.meta["result"] = "{} win.".format(self.meta["player:{}".format(k)])
                return

        if functools.reduce(lambda x, y: x + y, map(lambda z: len(z), status.values())) == 9:
            self.meta["result"] = "draw"

    def persist(self):
        """
        Persists game in Redis.
        """

        self.db.hmset(self.meta_id, self.meta)
        self.db.hmset(self.board_id, self.board)
        logger.info("Game {} is persisted.".format(self.game_id))

    def to_json(self):
        """
        JSON representation of a game.
        :return: {id: game_id,
                  player:0: player0_name,
                  player:1: player1_name,
                  result: game_result,
                  next_player: next_player_name,
                  board: { 0: square0_owner,
                           1: square1_owner,
                           2: square2_owner,
                           3: square3_owner,
                           4: square4_owner,
                           5: square5_owner,
                           6: square6_owner,
                           7: square7_owner,
                           8: square8_owner}
                  }
        """

        return json.dumps(self.game)
