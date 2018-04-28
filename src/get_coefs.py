import json
import requests
from LiveGame import LiveGame



def get_live_games():
    # url = requests.get('http://1xstavka.ru').url + '/LiveFeed/GetCyberGamesZip?lng=ru&mode=4'
    url = requests.get('http://1xstavka.ru').url + '/LiveFeed/Get1x2_Zip?sports=85&count=20&mode=4&'
    data = json.loads(requests.get(url).text)
    games = []

    for record in data["Value"]:
        league = record["L"]
        if "FIFA" in league:
            # print(league)
            first_team = record["O1"]
            second_team = record["O2"]
            try:
                state = record["SC"]["I"]
            except Exception as e:
                # print(record)
                half = record["SC"].get("CP", 1)
                # print('%s - %s is live.' % (first_team, second_team))

                if len(record["E"]) > 2:
                    coefs = [record["E"][i]["C"] for i in range(0, 3)]
                    score = [
                        record["SC"]["FS"].get("S1", 0), record["SC"]["FS"].get("S2", 0)
                    ]

                    games.append(
                        LiveGame(league, first_team, second_team, score, coefs)
                    )
                else:
                    pass
            # print('No coefs for: %s - %s' % (first_team, second_team))
            else:
                if state == "Перерыв":
                    if len(record["E"]) > 2:
                        coefs = [record["E"][i]["C"] for i in range(0, 3)]
                        score = [
                            record["SC"]["FS"].get("S1", 0),
                            record["SC"]["FS"].get("S2", 0),
                        ]

                        games.append(
                            LiveGame(league, first_team, second_team, score, coefs)
                        )
                    else:
                        pass
                # print('%s - %s halftime.\n' % (first_team, second_team))
                elif state == "Матч завершён":
                    if len(record["E"]) > 2:
                        coefs = [record["E"][i]["C"] for i in range(0, 3)]
                        score = [
                            record["SC"]["FS"].get("S1", 0),
                            record["SC"]["FS"].get("S2", 0),
                        ]

                        games.append(
                            LiveGame(
                                league, first_team, second_team, score, coefs, "End"
                            )
                        )
                    else:
                        pass
    # print('%s - %s is end.\n' % (first_team, second_team))
    # TODO:
    # Check that game in our database and send it if yes
    # print(games)
    return games
