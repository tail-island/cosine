import numpy      as np
import sys
import tensorflow as tf

from config   import NUM_BLOCKS, D_MODEL, NUM_HEADS, D_FF, MAXIMUM_POSITION, DROPOUT_RATE
from data_set import get_data_frame, get_data_set
from funcy    import identity, juxt
from model    import LearningRateSchedule, op


def main():
    epoch_size  = int(sys.argv[1])
    valid_begin = int(sys.argv[2])
    model_path  =     sys.argv[3]

    data_frame = get_data_frame()

    xs, _              = get_data_set(data_frame)
    train_xs, train_ys = get_data_set(data_frame.query(f'race_id <  {valid_begin}00000000'))
    valid_xs, valid_ys = get_data_set(data_frame.query(f'race_id >= {valid_begin}00000000'))

    model = tf.keras.Model(*juxt(identity, op(NUM_BLOCKS, D_MODEL, NUM_HEADS, D_FF, tuple(map(lambda x_item: np.max(x_item) + 1, xs)), MAXIMUM_POSITION, DROPOUT_RATE))(tuple(map(lambda x_item: tf.keras.Input(shape=np.shape(x_item)[1:]), xs))))
    # model.summary()
    model.compile(optimizer=tf.keras.optimizers.Adam(LearningRateSchedule(D_MODEL), beta_1=0.9, beta_2=0.98, epsilon=1e-9), loss='huber', metrics=('mae',))
    model.fit(train_xs, train_ys, batch_size=256, epochs=epoch_size, validation_data=(valid_xs, valid_ys))

    tf.keras.models.save_model(model, model_path, include_optimizer=False)


if __name__ == '__main__':
    main()
