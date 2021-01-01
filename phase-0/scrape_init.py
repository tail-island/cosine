import sqlite3


def init_database():
    with sqlite3.connect('netkeiba.sqlite3') as database:
        cursor = database.cursor()

        cursor.execute('CREATE TABLE races ('
                       '    id                      INTEGER PRIMARY KEY,'
                       '    date                    TEXT    NOT NULL,'
                       '    place                   TEXT    NOT NULL,'
                       '    race_number             INTEGER NOT NULL,'
                       '    field                   TEXT    NOT NULL,'
                       '    distance                INTEGER NOT NULL,'
                       '    direction               INTEGER NOT NULL,'
                       '    weather                 TEXT    NOT NULL,'
                       '    field_condition         TEXT    NOT NULL,'
                       '    max_prize               INTEGER NOT NULL'
                       ')')

        cursor.execute('CREATE TABLE horses ('
                       '    id                      INTEGER PRIMARY KEY AUTOINCREMENT,'
                       '    name                    TEXT    NOT NULL'
                       ')')

        cursor.execute('CREATE TABLE jockeys ('
                       '    id                      INTEGER PRIMARY KEY AUTOINCREMENT,'
                       '    name                    TEXT    NOT NULL'
                       ')')

        cursor.execute('CREATE TABLE stables ('
                       '    id                      INTEGER PRIMARY KEY AUTOINCREMENT,'
                       '    name                    TEXT    NOT NULL'
                       ')')

        cursor.execute('CREATE TABLE trainers ('
                       '    id                      INTEGER PRIMARY KEY AUTOINCREMENT,'
                       '    name                    TEXT    NOT NULL'
                       ')')

        cursor.execute('CREATE TABLE results ('
                       '    id                      INTEGER PRIMARY KEY AUTOINCREMENT,'
                       '    race_id                 INTEGER NOT NULL,'
                       '    horse_id                INTEGER NOT NULL,'
                       '    jockey_id               INTEGER NOT NULL,'
                       '    stable_id               INTEGER NOT NULL,'
                       '    trainer_id              INTEGER NOT NULL,'
                       '    rank                    INTEGER NOT NULL,'
                       '    post                    INTEGER NOT NULL,'
                       '    number                  INTEGER NOT NULL,'
                       '    sex                     TEXT    NOT NULL,'
                       '    age                     INTEGER NOT NULL,'
                       '    jockey_class            TEXT    NOT NULL,'
                       '    jockey_weight           INTEGER NOT NULL,'
                       '    time                    FLOAT   NOT NULL,'
                       '    margin                  TEXT    NOT NULL,'
                       '    popularity              INTEGER NOT NULL,'
                       '    odds                    FLOAT   NOT NULL,'
                       '    weight                  INTEGER NOT NULL,'
                       '    weight_difference       INTEGER NOT NULL,'
                       '    FOREIGN KEY(race_id)    REFERENCES races(id),'
                       '    FOREIGN KEY(horse_id)   REFERENCES horses(id),'
                       '    FOREIGN KEY(jockey_id)  REFERENCES jockeys(id),'
                       '    FOREIGN KEY(trainer_id) REFERENCES trainers(id)'
                       ')')

        cursor.execute('CREATE UNIQUE INDEX index_horses_name   ON horses(name)')
        cursor.execute('CREATE UNIQUE INDEX index_jockeys_name  ON jockeys(name)')
        cursor.execute('CREATE UNIQUE INDEX index_stables_name  ON stables(name)')
        cursor.execute('CREATE UNIQUE INDEX index_trainers_name ON trainers(name)')

        cursor.execute('CREATE INDEX index_races_date     ON races(date)')
        cursor.execute('CREATE INDEX index_results_number ON results(number)')



def main():
    init_database()


if __name__ == '__main__':
    main()
