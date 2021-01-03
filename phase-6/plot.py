import matplotlib.pyplot as plot
import lightgbm          as lgb
import numpy             as np
import sys

from data_set import get_data_frame, get_data_set


def main():
    data_frame = get_data_frame().query(f'race_id >= {sys.argv[1]}00000000 and race_id <= {sys.argv[2]}99999999')
    data_set   = get_data_set(data_frame).construct()
    model      = lgb.Booster(model_file=sys.argv[3])
    pred_ys    = model.predict(data_set.get_data(), num_iteration=model.best_iteration)

    plot.scatter(data_set.get_label(), pred_ys, alpha=0.01)
    plot.xlim((np.min(data_set.get_label()) - 0.5, np.max(data_set.get_label()) + 0.5))
    plot.ylim((np.min(data_set.get_label()) - 0.5, np.max(data_set.get_label()) + 0.5))
    plot.show()


if __name__ == '__main__':
    main()
