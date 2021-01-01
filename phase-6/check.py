import lightgbm as lgb
import numpy    as np
import sys

from data_set import get_data_frame, get_data_set
from funcy    import first, group_by, map, second


def main():
    data_frame = get_data_frame().query(f'race_id >= {sys.argv[1]}00000000 and race_id <= {sys.argv[2]}99999999')
    data_set   = get_data_set(data_frame).construct()
    model      = lgb.Booster(model_file=sys.argv[3])
    pred_ys    = model.predict(data_set.get_data(), num_iteration=model.best_iteration)

    expense     = 0
    revenue     = 0
    win_count   = 0
    total_count = 0

    for race_indexes in group_by(first, zip(data_frame['race_id'], np.arange(len(data_frame)))).values():
        indexes = tuple(map(second, race_indexes))

        pred_winner_index = np.argmin(np.reshape(pred_ys[list(indexes)], (-1,)))
        race_data_frame   = data_frame[min(indexes): max(indexes) + 1]

        if race_data_frame.iloc[pred_winner_index]['rank'] == 1:
            win_count += 1
            revenue   += int(race_data_frame.iloc[pred_winner_index]['odds'] * 100)

        expense     += 100
        total_count += 1

    print(f'{revenue:,d}, {expense:,d}, {revenue / expense:.3f}, {win_count / total_count:.3f}')


if __name__ == '__main__':
    main()
