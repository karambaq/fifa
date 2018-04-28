import pytz
from hist import check_is_end
from datetime import datetime
from itertools import product
from get_time import get_times
from insert_row import insert_row


class LiveGame:

    def __init__(self, league, first_team, second_team, score, coefs, state="Live"):
        self._league = league
        self._first_team = first_team
        self._second_team = second_team
        self._teams = "%s — %s" % (first_team, second_team)
        self._score = score
        self._coefs = coefs
        self._w1 = coefs[0]
        self._x = coefs[1]
        self._w2 = coefs[2]
        self._goals = []
        self._first_half_goals = []
        self._second_half_goals = []
        self._state = state
        local = pytz.timezone("Europe/Moscow")
        moscow_now = datetime.now(local)
        print(moscow_now)
        self._date = '%s %s' % (datetime.today().isoformat()[:10], datetime.today().time().isoformat()[:5])

    def __str__(self):
        return "%s\n%s\n%s\nП1:%s Х:%s П2:%s\n%s" % (
            self._league,
            self._teams,
            self._score,
            self._w1,
            self._x,
            self._w2,
            self._state,
        )

    def __repr__(self):
        return "%s\n%s\n%s\nП1:%s Х:%s П2:%s\n%s" % (
            self._league,
            self._teams,
            self._score,
            self._w1,
            self._x,
            self._w2,
            self._state,
        )

    def get_league(self):
        return self._league

    def get_teams(self):
        return self._teams

    def get_first_team(self):
        return self._first_team

    def get_second_team(self):
        return self._second_team

    def get_first_score(self):
        return self._score[0]

    def get_second_score(self):
        return self._score[1]

    def get_score(self):
        return self._score

    def get_score_sum(self):
        return sum(int(s) for s in self._score)

    def set_score(self, score):
        self._score = score

    def add_goal(self, team, time, new_score):
        print("Sum: %s" % int(len(self._goals) / 2))
        print("New score: %s" % sum(int(s) for s in new_score))
        if len(self._goals)  == sum(int(s) for s in new_score) - 1:
            self._goals.append('%s %s' % (team, time))

    def get_row(self):
        row = [
            self._date,
            self._league,
            self._first_team,
            self._second_team,
            self._w1,
            self._x,
            self._w2,
        ]
        if self._first_half_goals and self._second_half_goals:
            row.extend(self._first_half_goals)
            row.append('%s:%s' % (self._first_half_score[0], self._first_half_score[1]))
            row.extend(self._second_half_goals)
            row.append('%s:%s' % (self._second_half_score[0], self._second_half_score[1]))
        else:
            row.extend(self._goals)
        row.append('%s:%s' % (self._score[0], self._score[1]))
#         if self.is_end():
#             row.append("End")
        return row

    def is_halftime(self):
        return self._state == "Halftime"

    def is_end(self):
        return self._state == "End"

    def has_goals(self):
        return bool(self._goals)

    def has_coefs(self):
        return bool(self._coefs)

    #  def set_halftime(self):
    #      print('Setting halftime for %s' % self._teams)
    #      self._first_half_count_goals = int(len(self._goals) / 2)
    #      self._first_half_goals = self._goals
    #      count_goals = len(self._first_half_goals)
    #      for i in range(len(self._goals), 6):
    #          self._first_half_goals.append('')
    #          self._first_half_goals.append('')

    def set_end(self):
        # if 'self._first_half_count_goals' in locals():
        print("Setting end for %s" % self._teams)
        self._first_half_goals = list(filter(lambda g: g != 0 and int(g[-2:]) <= 45, self._goals))
        self._first_half_score = [sum(g[0] == '1' for g in self._first_half_goals), sum(g[0] == '2' for g in self._first_half_goals)]
        for i in range(len(self._first_half_goals), 6):
            self._first_half_goals.append(0)

        self._second_half_goals = list(filter(lambda g: g != 0 and int(g[-2:]) > 45, self._goals))
        self._second_half_score = [sum(g[0] == '1' for g in self._second_half_goals), sum(g[0] == '2' for g in self._second_half_goals)]
        for i in range(len(self._second_half_goals), 6):
            self._second_half_goals.append(0)

        self._state = "End"


def is_new_goal(first_game, second_game):
    return first_game.get_teams() == second_game.get_teams() and first_game.get_score() != second_game.get_score()


def update_games(prev_games, cur_games):
    times = get_times()
    seen = set()

    # Add new games
    for c_g in cur_games:
        if c_g.get_teams() not in [p_g.get_teams() for p_g in prev_games]:
            prev_games.append(c_g)

    # print('prev_games %s' % prev_games)
    # print('cur_games %s' % cur_games)
    print()
    for p_g, c_g in product(prev_games, cur_games):
        if (p_g, c_g) not in seen and (c_g, p_g) not in seen:
            if is_new_goal(p_g, c_g):
                print("Goal in %s on %s" % (p_g.get_teams(), times[c_g.get_teams()]))
                if c_g.get_first_score() != p_g.get_first_score():
                    # print(times[c_g.get_teams()])
                    # print(str(times[c_g.get_teams()]).split())
                    p_g.add_goal(
                        '1', times[c_g.get_teams()].split(':')[0], c_g.get_score()
                    )
                    p_g.set_score(c_g.get_score())
                elif c_g.get_second_score() != p_g.get_second_score():
                    # print(times[c_g.get_teams()])
                    # print(str(times[c_g.get_teams()]).split())
                    p_g.add_goal(
                            '2', times[c_g.get_teams()].split(':')[0], c_g.get_score()
                    )
                    p_g.set_score(c_g.get_score())
                print("Row: %s" % p_g.get_row())
                print()

            if c_g.get_teams() == p_g.get_teams() and c_g.is_end() and c_g.has_coefs():
                p_g.set_end()

            seen.add((p_g, c_g))
            seen.add((c_g, p_g))
    return prev_games
