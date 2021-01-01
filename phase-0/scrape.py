import re
import requests
import sqlite3
import sys

from bs4      import BeautifulSoup
from funcy    import map, partial
from operator import add
from time     import sleep


def get_race_id(year, place_code, round_number, day_number, race_number):
    return "{:04d}{:02d}{:02d}{:02d}{:02d}".format(year, place_code, round_number, day_number, race_number)


def get_soup(url):
    html = requests.get(url)
    html.encoding = 'EUC-JP'

    return BeautifulSoup(html.text, 'html.parser')


def add_race(soup, race_id, year, race_number):
    if not soup.select('dl#RaceList_DateList dd.Active a'):
        return None

    with sqlite3.connect('netkeiba.sqlite3') as database:
        cursor = database.cursor()

        month, day      = map(int, re.findall(r'\d+', soup.select('dl#RaceList_DateList dd.Active a')[0]['title']))
        place           = soup.select('div.RaceKaisaiWrap li.Active a')[0].get_text()
        field           = soup.select('div.RaceData01 span')[0].get_text().strip()[0]
        distance        = int(soup.select('div.RaceData01 span')[0].get_text().strip()[1:5])
        direction       = re.findall(r'\((.*)\)',  soup.select('div.RaceData01')[0].get_text().strip())[0]
        weather         = re.findall(r'天候:(.*)', soup.select('div.RaceData01')[0].get_text().strip())[0]
        field_condition = re.findall(r'馬場:(.*)', soup.select('div.RaceData01')[0].get_text().strip())[0]
        max_prize       = int(re.findall(r'本賞金:(\d+)', soup.select('div.RaceData02')[0].get_text().strip())[0])

        cursor.execute('INSERT INTO races VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (int(race_id),
                        '{:04d}/{:02d}/{:02d}'.format(year, month, day),
                        place,
                        race_number,
                        field,
                        distance,
                        direction,
                        weather,
                        field_condition,
                        max_prize))

    return True


def add_horse(result_soup):
    with sqlite3.connect('netkeiba.sqlite3') as database:
        cursor = database.cursor()

        name = result_soup.select('span.Horse_Name a')[0]['title'].strip()

        cursor.execute('SELECT id FROM horses WHERE name = ?', (name,))
        row = cursor.fetchone()

        if row:
            return row[0]

        cursor.execute('INSERT INTO horses (name) VALUES (?)', (name,))

        return cursor.lastrowid


def add_jockey(result_soup):
    with sqlite3.connect('netkeiba.sqlite3') as database:
        cursor = database.cursor()

        name = re.sub(r'[▲|△|★|☆|◇|◆]', '', result_soup.select('td.Jockey')[0].get_text().strip())

        cursor.execute('SELECT id FROM jockeys WHERE name = ?', (name,))
        row = cursor.fetchone()

        if row:
            return row[0]

        cursor.execute('INSERT INTO jockeys (name) VALUES (?)', (name,))

        return cursor.lastrowid


def add_stable(result_soup):
    with sqlite3.connect('netkeiba.sqlite3') as database:
        cursor = database.cursor()

        name = result_soup.select('td.Trainer span')[0].get_text().strip()

        cursor.execute('SELECT id FROM stables WHERE name = ?', (name,))
        row = cursor.fetchone()

        if row:
            return row[0]

        cursor.execute('INSERT INTO stables (name) VALUES (?)', (name,))

        return cursor.lastrowid


def add_trainer(result_soup):
    with sqlite3.connect('netkeiba.sqlite3') as database:
        cursor = database.cursor()

        name = result_soup.select('td.Trainer a')[0]['title'].strip()

        cursor.execute('SELECT id FROM trainers WHERE name = ?', (name,))
        row = cursor.fetchone()

        if row:
            return row[0]

        cursor.execute('INSERT INTO trainers (name) VALUES (?)', (name,))

        return cursor.lastrowid


def add_result(result_soup, race_id, horse_id, jockey_id, stable_id, trainer_id):
    with sqlite3.connect('netkeiba.sqlite3') as database:
        cursor = database.cursor()

        rank = result_soup.select('td.Result_Num div')[0].get_text().strip()

        if not rank.isdecimal():
            return

        post                      = int(result_soup.select('td.Num div')[0].get_text().strip())
        number                    = int(result_soup.select('td.Num div')[1].get_text().strip())
        sex                       = result_soup.select('div.Horse_Info_Detail span.Lgt_Txt')[0].get_text().strip()[:1]
        age                       = int(re.findall(r'\d+', result_soup.select('div.Horse_Info_Detail span.Lgt_Txt')[0].get_text().strip())[0])
        jockey_class              = (re.findall(r'[▲|△|★|☆|◇|◆]', result_soup.select('td.Jockey')[0].get_text().strip()) + [''])[0]
        jockey_weight             = float(result_soup.select('span.JockeyWeight')[0].get_text().strip())
        minute, second            = map(float, re.findall(r'[\d\.]+', result_soup.select('span.RaceTime')[0].get_text().strip()))
        margin                    = result_soup.select('span.RaceTime')[1].get_text().strip()
        popularity                = int(result_soup.select('span.OddsPeople')[0].get_text().strip())
        odds                      = float(result_soup.select('td.Odds span')[1].get_text().strip())
        weights                   = re.findall(r'[\d-]+', result_soup.select('td.Weight')[0].get_text().strip())
        weight, weight_difference = map(float, weights) if len(weights) == 2 else (float(weights[0]), 0.0)

        cursor.execute('INSERT INTO results (race_id, horse_id, jockey_id, stable_id, trainer_id, rank, post, number, sex, age, jockey_class, jockey_weight, time, margin, popularity, odds, weight, weight_difference) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (int(race_id),
                        horse_id,
                        jockey_id,
                        stable_id,
                        trainer_id,
                        rank,
                        post,
                        number,
                        sex,
                        age,
                        jockey_class,
                        jockey_weight,
                        minute * 60.0 + second,
                        margin,
                        popularity,
                        odds,
                        weight,
                        weight_difference))

        print('\t'.join(map(str, (race_id, rank, post, number, sex, age, jockey_class, jockey_weight, minute, second, margin, popularity, odds, weight, weight_difference))))


def add_results(race_id, year, race_number):
    soup = get_soup("https://race.netkeiba.com/race/result.html?race_id={}&rf=race_list".format(race_id))

    if not add_race(soup, race_id, year, race_number):
        return False

    for result_soup in soup.select('div.ResultTableWrap tbody tr'):
        horse_id   = add_horse(result_soup)
        jockey_id  = add_jockey(result_soup)
        stable_id  = add_stable(result_soup)
        trainer_id = add_trainer(result_soup)

        add_result(result_soup, race_id, horse_id, jockey_id, stable_id, trainer_id)

    return True


def add_data(year):
    for place_code in map(partial(add, 1), range(10)):
        for round_number in map(partial(add, 1), range(10)):
            for day_number in map(partial(add, 1), range(10)):
                for race_number in map(partial(add, 1), range(12)):
                    race_id = get_race_id(year, place_code, round_number, day_number, race_number)

                    with sqlite3.connect('netkeiba.sqlite3') as database:
                        cursor = database.cursor()

                        if tuple(cursor.execute('SELECT COUNT(*) FROM races WHERE id = ?', (race_id,)))[0][0] > 0:
                            break

                    sleep(1)

                    result = add_results(race_id, year, race_number)

                    if not result:
                        break


def main():
    add_data(int(sys.argv[1]))


if __name__ == '__main__':
    main()
