import sqlite3


def select_data():
    with sqlite3.connect('../phase-0/netkeiba.sqlite3') as database:
        cursor = database.cursor()
        sql    = ('SELECT races.id, races.place, races.field, races.distance, races.direction, races.weather, races.field_condition, races.max_prize, '
                  '       results.horse_id, results.jockey_id, results.stable_id, results.trainer_id, results.rank, results.number, results.sex, results.age, results.jockey_class, results.jockey_weight, results.time, results.odds, results.weight '
                  'FROM races '
                  'INNER JOIN results ON results.race_id = races.id '
                  'ORDER BY races.id, results.number')

        return cursor.execute(sql)


def main():
    print('\t'.join(('race_id',
                     'place',
                     'field',
                     'distance',
                     'direction',
                     'weather',
                     'field_condition',
                     'max_prize',
                     'horse',
                     'jockey',
                     'stable',
                     'trainer',
                     'rank',
                     'number',
                     'sex',
                     'age',
                     'jockey_class',
                     'jockey_weight',
                     'time',
                     'odds',
                     'weight')))

    for record in select_data():
        print('\t'.join(map(lambda column: str(column) if column is not None else '', record)))


if __name__ == '__main__':
    main()
