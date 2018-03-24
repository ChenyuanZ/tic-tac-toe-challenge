# Quick Start

## Create environment
```
$ conda create --name tic_tac_toe
$ source activate tic_tac_toe
(tic_tac_toe)$ conda install -c conda-forge tornado==5.0.1
(tic_tac_toe)$ conda install redis-py==2.10.6
```

## APIs
* GET /api/games: Return a list of the Games known to the server, as JSON.
* POST /api/games: Create a new Game, assigning it an ID and returning the newly created Game.
* GET /api/games/\<id>: Retrieve a Game by its ID, returning a 404 status code if no game with that ID exists.
* POST /api/games/\<id>: Update the Game with the given ID, replacing its data with the newly POSTed data.

## To Do List
* Use [Redis Transaction](https://redis.io/topics/transactions) to avoid inconsistency.
* Add unit tests.