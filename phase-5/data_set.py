import lightgbm    as lgb
import pandas      as pd
import scipy.stats as stats

from funcy import complement, concat


FACTORIZE_FEATURES   = ('place', 'field', 'direction', 'weather', 'field_condition', 'sex', 'jockey_class')
CATEGORICAL_FEATURES = tuple(concat(FACTORIZE_FEATURES, ('horse', 'jockey', 'stable', 'trainer')))
REMOVING_FEATURES    = ('race_id', 'rank', 'number', 'time', 'odds')


def get_data_frame():
    data_frame = pd.read_table('netkeiba.tsv', low_memory=False)

    # 文字列のカラムを数値に変換します。
    for feature in FACTORIZE_FEATURES:
        data_frame[feature] = pd.factorize(data_frame[feature])[0] + 1  # NaNが-1になると面倒なので、+1しておきます。

    # タイムは正規化（標準化）しておきます
    data_frame['time'] = stats.zscore(data_frame['time'])

    return data_frame


def get_data_set(data_frame):
    xs = data_frame.drop(columns=list(REMOVING_FEATURES))
    ys = data_frame['time']

    return lgb.Dataset(xs, label=ys, categorical_feature=list(filter(complement(set(REMOVING_FEATURES)), CATEGORICAL_FEATURES)), free_raw_data=False)
