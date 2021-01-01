import numpy       as np
import pandas      as pd
import scipy.stats as stats


FACTORIZE_FEATURES = ('place', 'field', 'distance', 'direction', 'weather', 'field_condition', 'max_prize',
                      'sex', 'age', 'jockey_class', 'jockey_weight', 'weight')


def get_data_frame():
    data_frame = pd.read_table('netkeiba.tsv', low_memory=False)

    for feature in FACTORIZE_FEATURES:
        data_frame[feature] = pd.factorize(data_frame[feature])[0] + 1

    # タイムは正規化（標準化）しておきます
    data_frame['time'] = stats.zscore(data_frame['time'])

    return data_frame


def get_data_set(data_frame):
    return ((np.array(data_frame[['place'          ]]).astype(np.int32),
             np.array(data_frame[['field'          ]]).astype(np.int32),
             np.array(data_frame[['distance'       ]]).astype(np.int32),
             np.array(data_frame[['direction'      ]]).astype(np.int32),
             np.array(data_frame[['weather'        ]]).astype(np.int32),
             np.array(data_frame[['field_condition']]).astype(np.int32),
             np.array(data_frame[['max_prize'      ]]).astype(np.int32),
             np.array(data_frame[['horse'          ]]).astype(np.int32),
             np.array(data_frame[['jockey'         ]]).astype(np.int32),
             np.array(data_frame[['stable'         ]]).astype(np.int32),
             np.array(data_frame[['trainer'        ]]).astype(np.int32),
             np.array(data_frame[['sex'            ]]).astype(np.int32),
             np.array(data_frame[['age'            ]]).astype(np.int32),
             np.array(data_frame[['jockey_class'   ]]).astype(np.int32),
             np.array(data_frame[['jockey_weight'  ]]).astype(np.int32),
             np.array(data_frame[['weight'         ]]).astype(np.int32)),
            np.array(data_frame[['time']]))
