# Quick Start


## Start tic_tac_toe server
```bash
$ [sudo] docker pull chenyuaz/tic_tac_toe:1.0.0
$ [sudo] docker pull redis
$ [sudo] docker-compose up -d
```


## APIs
* GET /api/games: Return a list of the Games known to the server, as JSON.
* POST /api/games: Create a new Game, assigning it an ID and returning the newly created Game.
* GET /api/games/\<id>: Retrieve a Game by its ID, returning a 404 status code if no game with that ID exists.
* POST /api/games/\<id>: Update the Game with the given ID, replacing its data with the newly POSTed data.


## Examples
A tic_tac_toe server is available at GCE. You can access it with the example below.
```python
import requests
# list all available games
r = requests.get("http://35.185.30.147:8888/api/games/")

# create a new game
r = requests.post("http://35.185.30.147:8888/api/games/")

# create a new game and specify player names
r = requests.post("http://35.185.30.147:8888/api/games/?player0=alpha&player1=beta")

# get game by id
r = requests.get("http://35.185.30.147:8888/api/games/1")

# update game by id
# user can choose a square from 0 to 8
r = requests.post("http://35.185.30.147:8888/api/games/1?square=0")

```


## To Do List
* Use [Redis Transaction](https://redis.io/topics/transactions) to avoid inconsistency.
* Add unit tests.
