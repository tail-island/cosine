import numpy      as np
import sys
import tensorflow as tf

from data_set import get_data_frame, get_data_set
from funcy    import first, group_by, map, second


def main():
    valid_begin = int(sys.argv[1])
    model_path  =     sys.argv[2]

    data_frame  = get_data_frame().query(f'race_id >= {valid_begin}00000000')
    xs, _       = get_data_set(data_frame)
    pred_ys     = tf.keras.models.load_model(model_path).predict(xs, batch_size=len(data_frame))

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
