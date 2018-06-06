import time
from collections import deque

from termcolor import colored
from hist import check_is_end
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
        # for c_g in cur:
        #     if c_g.is_end() and c_g.has_coefs():
        #         if c_g.get_teams() not in sended:
        #             insert_row(c_g.get_row())
        #             sended.append(c_g.get_teams())
        #         cur.remove(c_g)
        #     elif c_g.is_end():
        #         cur.remove(c_g)

        for c_g in games:
            if check_is_end(c_g.get_league(), c_g.get_teams(), c_g.get_score()) and c_g.has_coefs():
                if c_g.get_row() not in sended:
                    c_g.set_end()
                    print(colored('Sending %s' % c_g.get_row(), 'red'))
                    with open('hist.txt', 'w') as f:
                        f.write(str(c_g.get_row()))
                    insert_row(c_g.get_row())
                    sended.append(c_g.get_row())
                cur.remove(c_g)
            elif c_g.is_end():
                cur.remove(c_g)

        # print(games)
        for g in games:
            print(g.get_row())

        games = cur
