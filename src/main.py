import pdb
import time
from collections import deque

from insert_row import insert_row
from LiveGame import update_games
from get_coefs import get_live_games

if __name__ == "__main__":
    games = get_live_games()
    sended = deque(maxlen=20)
    while True:
        later_games = get_live_games()
        cur = update_games(games, later_games)

        # Delete ended games
        for c_g in cur:
            if c_g.is_end() and c_g.has_coefs():
                if c_g.get_teams() not in sended:
                    insert_row(c_g.get_row())
                    sended.append(c_g.get_teams())
                cur.remove(c_g)
            elif c_g.is_end():
                cur.remove(c_g)
        # print(games)

        for g in cur:
            print(g.get_row())

        games = cur
