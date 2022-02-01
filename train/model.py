import tensorflow as tf 

from model_parts import conv, affine

board = tf.keras.Input(shape=(8, 8, 12))
c1 = conv(x=board, filters=32)
c2 = conv(x=c1, filters=64)
c3 = conv(x=c2, filters=256)
c4 = conv(x=c3, filters=256, skip_connection=c3)
c5 = conv(x=c4, filters=256, skip_connection=c2)
c6 = conv(x=c5, filters=256, skip_connection=c1)
x = affine(x=c6, neurons=256)
x = affine(x=x, neurons=64)
x = affine(x=x, neurons=1)
x = tf.keras.layers.Softmax(axis=[1, 2])(x)

model = tf.keras.Model(inputs=[board,], outputs=x)

model.compile('adam', 'categorical_crossentropy')

model.summary()
