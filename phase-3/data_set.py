import numpy  as np
import pandas as pd

from funcy    import concat, mapcat, partial
from operator import add


FACTORIZE_FEATURES = tuple(concat(('place', 'field', 'distance', 'direction', 'weather', 'field_condition', 'max_prize'),
                                  mapcat(lambda i: (f'sex_{i:02d}', f'age_{i:02d}', f'jockey_class_{i:02d}', f'jockey_weight_{i:02d}', f'weight_{i:02d}'),
                                         map(partial(add, 1), range(18)))))


def get_data_frame():
    data_frame = pd.read_table('netkeiba.tsv', low_memory=False)

    for feature in FACTORIZE_FEATURES:
        data_frame[feature] = pd.factorize(data_frame[feature])[0] + 1

    data_frame = data_frame.drop(data_frame.index[data_frame['rank_01'].isnull() &
                                                  data_frame['rank_02'].isnull() &
                                                  data_frame['rank_03'].isnull() &
                                                  data_frame['rank_04'].isnull() &
                                                  data_frame['rank_05'].isnull() &
                                                  data_frame['rank_06'].isnull() &
                                                  data_frame['rank_07'].isnull() &
                                                  data_frame['rank_08'].isnull() &
                                                  data_frame['rank_09'].isnull() &
                                                  data_frame['rank_10'].isnull() &
                                                  data_frame['rank_11'].isnull() &
                                                  data_frame['rank_12'].isnull() &
                                                  data_frame['rank_13'].isnull() &
                                                  data_frame['rank_14'].isnull() &
                                                  data_frame['rank_15'].isnull() &
                                                  data_frame['rank_16'].isnull() &
                                                  data_frame['rank_17'].isnull() &
                                                  data_frame['rank_18'].isnull()])

    return data_frame


def get_data_set(data_frame):
    return ((np.array(data_frame[['place'                                                                     ]]          ).astype(np.int32),
             np.array(data_frame[['field'                                                                     ]]          ).astype(np.int32),
             np.array(data_frame[['distance'                                                                  ]]          ).astype(np.int32),
             np.array(data_frame[['direction'                                                                 ]]          ).astype(np.int32),
             np.array(data_frame[['weather'                                                                   ]]          ).astype(np.int32),
             np.array(data_frame[['field_condition'                                                           ]]          ).astype(np.int32),
             np.array(data_frame[['max_prize'                                                                 ]]          ).astype(np.int32),
             np.array(data_frame[list(map(lambda i: f'horse_{i:02d}',         map(partial(add, 1), range(18))))].fillna(0)).astype(np.int32),
             np.array(data_frame[list(map(lambda i: f'jockey_{i:02d}',        map(partial(add, 1), range(18))))].fillna(0)).astype(np.int32),
             np.array(data_frame[list(map(lambda i: f'stable_{i:02d}',        map(partial(add, 1), range(18))))].fillna(0)).astype(np.int32),
             np.array(data_frame[list(map(lambda i: f'trainer_{i:02d}',       map(partial(add, 1), range(18))))].fillna(0)).astype(np.int32),
             np.array(data_frame[list(map(lambda i: f'sex_{i:02d}',           map(partial(add, 1), range(18))))].fillna(0)).astype(np.int32),
             np.array(data_frame[list(map(lambda i: f'age_{i:02d}',           map(partial(add, 1), range(18))))].fillna(0)).astype(np.int32),
             np.array(data_frame[list(map(lambda i: f'jockey_class_{i:02d}',  map(partial(add, 1), range(18))))].fillna(0)).astype(np.int32),
             np.array(data_frame[list(map(lambda i: f'jockey_weight_{i:02d}', map(partial(add, 1), range(18))))].fillna(0)).astype(np.int32),
             np.array(data_frame[list(map(lambda i: f'weight_{i:02d}',        map(partial(add, 1), range(18))))].fillna(0)).astype(np.int32)),
            np.argmin(np.array(data_frame[list(map(lambda i: 'rank_{:02d}'.format(i), map(partial(add, 1), range(18))))].fillna(99)), axis=1))
