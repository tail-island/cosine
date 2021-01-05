import sqlite3

from funcy    import concat, mapcat, partial
from operator import add


def select_data():
    def create_result_select_items():
        for i in map(partial(add, 1), range(18)):
            yield ', '.join((f'results_{i}.horse_id',
                             f'results_{i}.jockey_id',
                             f'results_{i}.stable_id',
                             f'results_{i}.trainer_id',
                             f'results_{i}.rank',
                             f'results_{i}.sex',
                             f'results_{i}.age',
                             f'results_{i}.jockey_class',
                             f'results_{i}.jockey_weight',
                             f'results_{i}.odds',
                             f'results_{i}.weight'))

    def create_result_join():
        for i in map(partial(add, 1), range(18)):
            yield f'LEFT OUTER JOIN results AS results_{i} ON results_{i}.race_id = races.id AND results_{i}.number = {i}'

    with sqlite3.connect('../phase-0/netkeiba.sqlite3') as database:
        cursor = database.cursor()
        sql    = ' '.join(('SELECT races.id, races.place, races.field, races.distance, races.direction, races.weather, races.field_condition, races.max_prize,',
                           ', '.join(create_result_select_items()),
                           'FROM races',
                           ' '.join(create_result_join()),
                           'ORDER BY races.id'))

        return cursor.execute(sql)


def main():
    print('\t'.join(concat(('race_id',
                            'place',
                            'field',
                            'distance',
                            'direction',
                            'weather',
                            'field_condition',
                            'max_prize'),
                           mapcat(lambda i: (f'horse_{i:02d}',
                                             f'jockey_{i:02d}',
                                             f'stable_{i:02d}',
                                             f'trainer_{i:02d}',
                                             f'rank_{i:02d}',
                                             f'sex_{i:02d}',
                                             f'age_{i:02d}',
                                             f'jockey_class_{i:02d}',
                                             f'jockey_weight_{i:02d}',
                                             f'odds_{i:02d}',
                                             f'weight_{i:02d}'),
                                  map(partial(add, 1), range(18))))))

    for record in select_data():
        print('\t'.join(map(lambda column: str(column) if column is not None else '', record)))


if __name__ == '__main__':
    main()
