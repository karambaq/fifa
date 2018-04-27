import requests
from lxml.html import fromstring


def get_times():
    url = requests.get('http://1xstavka.ru').url + '/cyber/FIFA/'
    # url = "https://1xboum.top/cyber/FIFA/"
    html_doc = requests.get(url).text
    tree = fromstring(html_doc)

    teams = [g.get("title").strip() for g in tree.xpath('//span[@class="n"]')]
    unscraped_times = [
        times.text for times in tree.xpath('//div[@class="c-events__item"]//span')
    ]
    # NEEDS TO TEST!!
    # Inspect elements where mets ':' or None value, after this, replacing None values with the blank
    times = list(
        map(
            lambda x: "" if x is None else x,
            list(filter(lambda x: x is None or ":" in x, unscraped_times)),
        )
    )
    time_dict = {teams: time for teams, time in zip(teams, times)}

    return time_dict
