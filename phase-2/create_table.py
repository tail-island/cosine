import sqlite3

from config   import HISTORY_COUNT
from funcy    import concat, map, mapcat, partial
from operator import add


def select_data():
    def create_result_select_items():
        for i in map(partial(add, 1), range(18)):
            for j in range(1 + HISTORY_COUNT):
                yield ', '.join((f'results_{i}_{j}.horse_id',
                                 f'results_{i}_{j}.jockey_id',
                                 f'results_{i}_{j}.stable_id',
                                 f'results_{i}_{j}.trainer_id',
                                 f'results_{i}_{j}.rank',
                                 f'results_{i}_{j}.post',
                                 f'results_{i}_{j}.number',
                                 f'results_{i}_{j}.sex',
                                 f'results_{i}_{j}.age',
                                 f'results_{i}_{j}.jockey_class',
                                 f'results_{i}_{j}.jockey_weight',
                                 f'results_{i}_{j}.time',
                                 f'results_{i}_{j}.margin',
                                 f'results_{i}_{j}.popularity',
                                 f'results_{i}_{j}.odds',
                                 f'results_{i}_{j}.weight',
                                 f'results_{i}_{j}.weight_difference'))

    def create_result_join():
        for i in map(partial(add, 1), range(18)):
            yield f'LEFT OUTER JOIN results AS results_{i}_0 ON results_{i}_0.race_id = races.id AND results_{i}_0.number = {i}'

            for j in map(partial(add, 1), range(HISTORY_COUNT)):
                yield ' '.join((f'LEFT OUTER JOIN results AS results_{i}_{j} ON results_{i}_{j}.id = (',
                                'SELECT temp_results.id',
                                'FROM results AS temp_results',
                                'INNER JOIN races AS temp_races ON temp_races.id = temp_results.race_id',
                                f'WHERE temp_results.horse_id = results_{i}_0.horse_id AND temp_races.date <= races.date ORDER BY temp_races.date DESC LIMIT 1 OFFSET {j})'))

    with sqlite3.connect('../phase-0/netkeiba.sqlite3') as database:
        cursor = database.cursor()
        sql    = ' '.join(('SELECT races.id, races.date, races.place, races.race_number, races.field, races.distance, races.direction, races.weather, races.field_condition, races.max_prize,',
                           ', '.join(create_result_select_items()),
                           'FROM races',
                           ' '.join(create_result_join()),
                           'ORDER BY races.id'))

        return cursor.execute(sql)


def main():
    print('\t'.join(concat(('race_id',
                            'date',
                            'place',
                            'race_number',
                            'field',
                            'distance',
                            'direction',
                            'weather',
                            'field_condition',
                            'max_prize'),
                           mapcat(lambda i: mapcat(lambda j: (f'horse_{i:02d}_{j}',
                                                              f'jockey_{i:02d}_{j}',
                                                              f'stable_{i:02d}_{j}',
                                                              f'trainer_{i:02d}_{j}',
                                                              f'rank_{i:02d}_{j}',
                                                              f'post_{i:02d}_{j}',
                                                              f'number_{i:02d}_{j}',
                                                              f'sex_{i:02d}_{j}',
                                                              f'age_{i:02d}_{j}',
                                                              f'jockey_class_{i:02d}_{j}',
                                                              f'jockey_weight_{i:02d}_{j}',
                                                              f'time_{i:02d}_{j}',
                                                              f'margin_{i:02d}_{j}',
                                                              f'popularity_{i:02d}_{j}',
                                                              f'odds_{i:02d}_{j}',
                                                              f'weight_{i:02d}_{j}',
                                                              f'weight_difference_{i:02d}_{j}'),
                                                   range(1 + HISTORY_COUNT)),
                                  map(partial(add, 1), range(18))))))

    for record in select_data():
        print('\t'.join(map(lambda column: str(column) if column is not None else '', record)))


if __name__ == '__main__':
    main()
