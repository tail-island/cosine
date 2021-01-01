import lightgbm as lgb
import numpy    as np
import pandas   as pd

from config   import HISTORY_COUNT
from funcy    import complement, concat, filter, partial, map, mapcat
from operator import add


FACTORIZE_FEATURES   = tuple(concat(('place', 'field', 'direction', 'weather', 'field_condition'),
                                    mapcat(lambda i: mapcat(lambda j: (f'sex_{i:02d}_{j}', f'jockey_class_{i:02d}_{j}', f'margin_{i:02d}_{j}'),
                                                            range(1 + HISTORY_COUNT)),
                                           map(partial(add, 1), range(18)))))

CATEGORICAL_FEATURES = tuple(concat(FACTORIZE_FEATURES,
                                    mapcat(lambda i: mapcat(lambda j: (f'horse_{i:02d}_{j}', f'jockey_{i:02d}_{j}', f'stable_{i:02d}_{j}', f'trainer_{i:02d}_{j}'),
                                                            range(1 + HISTORY_COUNT)),
                                           map(partial(add, 1), range(18)))))

REMOVING_FEATURES    = tuple(concat(('race_id', 'date'),
                                    mapcat(lambda i: (f'rank_{i:02d}_0', f'time_{i:02d}_0', f'margin_{i:02d}_0'), map(partial(add, 1), range(18))),
                                    mapcat(lambda i: mapcat(lambda j: (f'horse_{i:02d}_{j}',),
                                                            map(partial(add, 1), range(HISTORY_COUNT))),
                                           map(partial(add, 1), range(18)))))


def get_data_frame():
    data_frame = pd.read_table('netkeiba.tsv', low_memory=False)

    # 文字列のカラムを数値に変換します。
    for feature in FACTORIZE_FEATURES:
        data_frame[feature] = pd.factorize(data_frame[feature])[0] + 1  # NaNが-1になると面倒なので、+1しておきます。

    # 中止になったレースを除去します。
    data_frame = data_frame.drop(data_frame.index[data_frame['rank_01_0'].isnull() &
                                                  data_frame['rank_02_0'].isnull() &
                                                  data_frame['rank_03_0'].isnull() &
                                                  data_frame['rank_04_0'].isnull() &
                                                  data_frame['rank_05_0'].isnull() &
                                                  data_frame['rank_06_0'].isnull() &
                                                  data_frame['rank_07_0'].isnull() &
                                                  data_frame['rank_08_0'].isnull() &
                                                  data_frame['rank_09_0'].isnull() &
                                                  data_frame['rank_10_0'].isnull() &
                                                  data_frame['rank_11_0'].isnull() &
                                                  data_frame['rank_12_0'].isnull() &
                                                  data_frame['rank_13_0'].isnull() &
                                                  data_frame['rank_14_0'].isnull() &
                                                  data_frame['rank_15_0'].isnull() &
                                                  data_frame['rank_16_0'].isnull() &
                                                  data_frame['rank_17_0'].isnull() &
                                                  data_frame['rank_18_0'].isnull()])

    return data_frame


def get_data_set(data_frame):
    xs = data_frame.drop(columns=list(REMOVING_FEATURES))
    ys = np.nanargmin(data_frame[list(map(lambda i: f'rank_{i:02d}_0', map(partial(add, 1), range(18))))], axis=1)

    return lgb.Dataset(xs, label=ys, categorical_feature=list(filter(complement(set(REMOVING_FEATURES)), CATEGORICAL_FEATURES)), free_raw_data=False)
