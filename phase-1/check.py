import lightgbm as lgb
import numpy    as np
import sys

from data_set import get_data_frame, get_data_set


def main():
    data_frame = get_data_frame().query(f'race_id >= {sys.argv[1]}00000000 and race_id <= {sys.argv[2]}99999999')
    data_set   = get_data_set(data_frame).construct()
    model      = lgb.Booster(model_file=sys.argv[3])
    pred_ys    = model.predict(data_set.get_data(), num_iteration=model.best_iteration)

    expense   = 0
    revenue   = 0
    win_count = 0

    for pred_y, true_y, row in zip(pred_ys, data_set.get_label(), data_frame.iterrows()):
        if np.argmax(pred_y) == true_y:
            win_count += 1
            revenue   += int(100 * row[1][f'odds_{int(true_y) + 1:02d}_0'])

        expense += 100

    print(f'{revenue:,d}, {expense:,d}, {revenue / expense:.3f}, {win_count / len(data_frame):.3f}')


if __name__ == '__main__':
    main()
