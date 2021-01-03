import matplotlib.pyplot as plot
import numpy             as np
import sys
import tensorflow        as tf

from data_set import get_data_frame, get_data_set


def main():
    valid_begin = int(sys.argv[1])
    model_path  =     sys.argv[2]

    data_frame  = get_data_frame().query(f'race_id >= {valid_begin}00000000')
    xs, true_ys = get_data_set(data_frame)
    pred_ys     = tf.keras.models.load_model(model_path).predict(xs, batch_size=len(data_frame))

    plot.scatter(true_ys, pred_ys, alpha=0.01)
    plot.xlim((np.min(true_ys) - 0.5, np.max(true_ys) + 0.5))
    plot.ylim((np.min(true_ys) - 0.5, np.max(true_ys) + 0.5))
    plot.show()


if __name__ == '__main__':
    main()
