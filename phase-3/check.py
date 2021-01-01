import numpy      as np
import sys
import tensorflow as tf

from data_set import get_data_frame, get_data_set


def main():
    valid_begin = int(sys.argv[1])
    model_path  =     sys.argv[2]

    data_frame  = get_data_frame().query(f'race_id >= {valid_begin}00000000')
    xs, true_ys = get_data_set(data_frame)
    pred_ys     = tf.keras.models.load_model(model_path).predict(xs, batch_size=len(data_frame))

    expense   = 0
    revenue   = 0
    win_count = 0

    for pred_y, true_y, row in zip(pred_ys, true_ys, data_frame.iterrows()):
        if np.argmax(pred_y) == true_y:
            win_count += 1
            revenue   += int(100 * row[1][f'odds_{int(true_y) + 1:02d}'])

        expense += 100

    print(f'{revenue:,d}, {expense:,d}, {revenue / expense:.3f}, {win_count / len(data_frame):.3f}')


if __name__ == '__main__':
    main()
