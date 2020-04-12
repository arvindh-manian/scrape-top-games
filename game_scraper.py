import urllib3
from bs4 import BeautifulSoup
import json
import sys
import os
from tqdm import tqdm
import threading
import time


def clear():
    if os.name == 'nt':  # windows
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def scrape_games(year):
    global boo
    global pbar
    url = "https://www.metacritic.com/browse/" + "games/score/metascore/year/" + \
        "all/filtered?view=detailed&sort=desc&year_selected=" + str(year)
    my_url = urllib3.PoolManager().request('GET', url).data
    soup = BeautifulSoup(my_url, 'lxml')
    body = soup.find('div', attrs={'class': 'body'})
    try:
        table = body.findChildren('table', attrs={'class': 'clamp-list'})[0]
    except:
        if boo:
            clear()
            print('Error: Metacritic has gotten too many connections from you')
            print("I'll still gather as many as I can")
        boo = False
        quit()
    rows = table.findChildren('td', attrs={'class': 'clamp-summary-wrap'})
    final_dict = {}
    i = 1
    for row in rows:
        game = {}
        link = row.findChildren('a', attrs={'class': 'title'})[0]
        # print(link)
        content = link.findChildren('h3')[0]
        title = content.contents[0].strip()
        date = row.findChildren('div', attrs={'class': 'clamp-details'})[1]
        summary = row.findChildren('div', attrs={'class': 'summary'})[
            0].contents[0]
        summary = summary.replace('\\n', '\n')
        summary = summary.replace('\\r', '\r')
        scores = row.findChildren(
            'div', attrs={'class': 'browse-score-clamp'})[0]
        metascore = scores.findChildren(
            'div', attrs={'class': 'clamp-metascore'})[0]
        metascore_raw = metascore.findChildren('div')[0].contents[0]
        userscore = scores.findChildren(
            'div', attrs={'class': 'clamp-userscore'})[0]
        userscore_raw = userscore.findChildren('div')[0].contents[0]
        scores_obj = {'metascore': metascore_raw, 'userscore': userscore_raw}
        game['title'] = title
        game['date'] = date.findChildren('span')[0].contents[0]
        game['summary'] = summary.strip()
        game['scores'] = scores_obj
        final_dict[i] = game
        i += 1
        pbar.update(1)
    with open(f'datasets/{year}.json', 'w+') as outfile:
        outfile.write(json.dumps(final_dict, indent=4))


clear()
try:
    os.mkdir('datasets')
except:
    print('/datasets already exists, would you like to continue?')
    ask = input('Input "yes" to do so\n')
    if ask != 'yes':
        quit()
    clear()
if len(sys.argv) != 3:
    print('Error: unexpected number of arguments')
    print('Usage: python3 game_scraper.py [start] [end] -- inclusive')
    print('Ex: $ python3 game_scraper 2007 2020')
    quit()
try:
    start = int(sys.argv[1])
except:
    print('Error: start should be an int')
    quit()
try:
    end = int(sys.argv[2])
except:
    print('Error: end should be an int')
    quit()
start, end = min([start, end]), max([start, end])
if end - start >= 10:
    print('This has a high change of failing.')
    yesorno = input(
        'Are you sure you want to continue? ' + 'Input "yes" to do so\n')
    if yesorno != 'yes':
        quit()
    clear()
if start < 1996:
    print('Error: start must be at least 1996')
    quit()
if end > 2020:
    print('Error: end must be at most 2020')
print(f'Gathering games from {start} to {end}, inclusive')
total_iter = 100 * (end - start + 1)

# yeah, this part is ugly
# the data set is incomplete for 1996-1999 though
# I just decided to support them
if start == 1996:
    total_iter -= 256
if start == 1997:
    total_iter -= 176
if start == 1998:
    total_iter -= 103
if start == 1999:
    total_iter -= 48

pbar = tqdm(total=total_iter, file=sys.stdout)  # progress bar
pbar.set_description('Total games')
threads = []
boo = True  # whether or not 429
for year in range(start, end + 1):
    thread = threading.Thread(target=scrape_games, args=(year,))
    threads.append(thread)
for thread in threads:
    thread.start()
    time.sleep(1)
for thread in threads:
    thread.join()
pbar.close()
