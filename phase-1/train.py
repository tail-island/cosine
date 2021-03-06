import lightgbm as lgb
import numpy    as np
import pandas   as pd
import sys

from data_set import get_data_frame, get_data_set


def get_data_sets(data_frame, train_begin, train_end, valid_begin, valid_end):
    return map(get_data_set, (data_frame.query(f'race_id >= {train_begin}00000000 and race_id <= {train_end}99999999'),
                              data_frame.query(f'race_id >= {valid_begin}00000000 and race_id <= {valid_end}99999999')))


def main():
    train_set, valid_set = get_data_sets(get_data_frame(), sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    params = {
        'objective': 'multiclass',
        'metric': 'multi_logloss',
        'num_class': 18,
        'force_row_wise': True,

        'learning_rate': 0.05
    }

    model = lgb.train(params, train_set=train_set, valid_sets=(train_set, valid_set), num_boost_round=1000, early_stopping_rounds=20)

    print(model.params)
    print(pd.DataFrame(model.feature_importance(), index=train_set.feature_name, columns=['importance']).sort_values('importance', ascending=False)[:50])
    print(f'train accuracy: {np.sum(train_set.get_label() == np.argmax(model.predict(train_set.get_data(), num_iteration=model.best_iteration), axis=1)) / len(train_set.get_label()):.3f}')
    print(f'valid accuracy: {np.sum(valid_set.get_label() == np.argmax(model.predict(valid_set.get_data(), num_iteration=model.best_iteration), axis=1)) / len(valid_set.get_label()):.3f}')

    model.save_model(sys.argv[5])


if __name__ == '__main__':
    main()
