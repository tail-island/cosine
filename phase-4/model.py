import numpy      as np
import tensorflow as tf

from funcy import concat, func_partial, rcompose


def op(num_blocks, d_model, num_heads, d_ff, x_vocab_size, maximum_position, dropout_rate):
    def dense(units):
        return tf.keras.layers.Dense(units)

    def dropout(rate):
        return tf.keras.layers.Dropout(rate)

    def embedding(input_dim, output_dim):
        return tf.keras.layers.Embedding(input_dim, output_dim)

    def layer_normalization():
        return tf.keras.layers.LayerNormalization(epsilon=1e-6)

    def relu():
        return tf.keras.layers.ReLU()

    def reshape(target_shape):
        return tf.keras.layers.Reshape(target_shape)

    def transpose(perm):
        return func_partial(tf.transpose, perm=perm)

    ####

    def scaled_dot_product_attention(x):
        query, key, value, mask = x

        return tf.matmul(tf.nn.softmax(tf.matmul(query, key, transpose_b=True) / tf.math.sqrt(tf.cast(d_model, tf.float32)) + mask * -1e9, axis=-1), value)

    def multi_head_attention(d_model, num_heads):
        split  = rcompose(reshape((-1, num_heads, d_model // num_heads)),
                          transpose((0, 2, 1, 3)))
        concat = rcompose(transpose((0, 2, 1, 3)),
                          reshape((-1, d_model)))

        def op(inputs):
            q, k, v, mask = inputs

            o = scaled_dot_product_attention((split(dense(d_model)(q)),
                                              split(dense(d_model)(k)),
                                              split(dense(d_model)(v)),
                                              mask))
            o = concat(o)
            o = dense(d_model)(o)

            return o

        return op

    def point_wise_feed_forward(d_model, d_ff):
        return rcompose(dense(d_ff),
                        relu(),
                        dense(d_model))

    def encoder_block(d_model, num_heads, d_ff, dropout_rate):
        def op(inputs):
            x, mask = inputs

            o = layer_normalization()(dropout(dropout_rate)(multi_head_attention(d_model, num_heads)((x, x, x, mask))) + x)
            o = layer_normalization()(dropout(dropout_rate)(point_wise_feed_forward(d_model, d_ff)(o))                 + o)

            return o

        return op

    def get_positional_encoding(maximum_position, d_model):
        result = np.empty((maximum_position, d_model), dtype=np.float32)

        angles = np.arange(maximum_position)[:, np.newaxis] / np.power(10000, 2 * np.arange(d_model // 2) / d_model)

        result[:, 0::2] = np.sin(angles)  # 偶数はsin
        result[:, 1::2] = np.cos(angles)  # 奇数はcos
        result = tf.cast(result[np.newaxis, ...], dtype=tf.float32)

        return result

    def encoder(num_blocks, d_model, num_heads, d_ff, x_vocab_size, maximum_position, dropout_rate):
        normalize_factor    = tf.math.sqrt(tf.cast(d_model, tf.float32))
        positional_encoding = get_positional_encoding(maximum_position, d_model)

        def op(inputs):
            x, mask = inputs

            o = dropout(dropout_rate)(tf.concat(tuple(concat((embedding(1, d_model)(tf.zeros((tf.shape(x[0])[0], 1))),),
                                                             map(lambda x_item_vocab_size, x_item: embedding(x_item_vocab_size, d_model)(x_item), x_vocab_size, x))),
                                                axis=1) *
                                      normalize_factor +
                                      positional_encoding[:, :tf.constant(1) + sum(map(lambda x_item: tf.shape(x_item)[1], x)), :])

            for _ in range(num_blocks):
                o = encoder_block(d_model, num_heads, d_ff, dropout_rate)((o, mask))

            return o

        return op

    def get_padding_mask(x):  # 今回はいらないのですけど、とりあえずこのままで
        x = tf.concat((tf.ones((tf.shape(x[0])[0], 1)), *x), axis=1)

        return tf.cast(tf.math.equal(x, 0), tf.float32)[:, tf.newaxis, tf.newaxis, :]

    def op(inputs):
        x = inputs

        return dense(1)(encoder(num_blocks, d_model, num_heads, d_ff, x_vocab_size, maximum_position, dropout_rate)((x, get_padding_mask(x)))[:, 0])

    return op


class LearningRateSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):
    def __init__(self, d_model, warmup_steps=4000):
        super(LearningRateSchedule, self).__init__()

        self.d_model      = tf.cast(d_model, tf.float32)
        self.warmup_steps = warmup_steps

    def __call__(self, step):
        return self.d_model ** -0.5 * tf.math.minimum(step ** -0.5, step * self.warmup_steps ** -1.5)
