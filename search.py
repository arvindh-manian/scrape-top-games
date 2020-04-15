import json
from datetime import datetime
def search(min_year, max_year, min_usescore, min_metascore, include_tbd, sortby, descending):
    games = []
    for year in range(min_year, max_year + 1):
        with open(f'datasets/{year}.json', 'r') as file:
            dictionary = json.loads(file.read())
            for game in dictionary:
                if dictionary[game]['scores']['userscore'] == 'tbd':
                    if include_tbd:
                        pass
                    else:
                        continue
                else:
                    if float(dictionary[game]['scores']['userscore']) < min_usescore:
                        continue
                if float(dictionary[game]['scores']['metascore']) < min_metascore:
                    continue
                games.append(dictionary[game])

    if sortby == 'userscore':
        games = sorted(games, key = lambda i: i['scores']['userscore'])
    elif sortby == 'metascore':
        games = sorted(games, key = lambda i: i['scores']['userscore'])
    elif sortby == 'release':
        games = sorted(games, key = lambda i: datetime.strptime(i['date'], '%B %d, %Y'))
    elif sortby == 'title':
        games = sorted(games, key = lambda i: i['title'])
    if descending:
        games.reverse()
    return games

