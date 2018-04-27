import json
import requests
from datetime import datetime

def check_is_end(league, teams, score):
    url = 'https://1xboum.top/getTranslate/ViewGameResultsGroup'
    headers = {'content-type': 'application/json'}
    data = '{"Language":"ru"}{"Params":["%s", null, 85, null, null, 180]}{"Vers":6}{"Adult": false}' % datetime.today().isoformat()[:10]
    teams = teams.split()
    
    response = json.loads(requests.post(url, data=data, headers=headers).text)
    
    for l in response.get('Data')[0].get('Elems'):
        last_couple = l.get('Elems')[-10:]
        for g in last_couple:
            league_str, teams_str = g.get('Head')[4:6]
            teams_str = teams_str.split()
            score_str = [int(g.get('Head')[6][0]), int(g.get('Head')[6][2])]
            print('Out:')
            print([league_str, teams_str, score_str])
            print('In:')
            print([league, teams, score])
            print()
            if [league_str, teams_str[0], teams_str[2], score_str] == [league, teams[0], teams[2], score]:
                return True
    return False

