import tensorflow as tf

def conv(x, filters, skip_connection=None):
	"""
	Conv2D, Batch Norm, and ReLu layers
	"""
	if skip_connection is not None:
		x = tf.keras.layers.concatenate([x, skip_connection], axis=-1)

	x = tf.keras.layers.Conv2D(filters=filters, kernel_size=3, padding='same', kernel_initializer='he_normal')(x)
	x = tf.keras.layers.BatchNormalization()(x)
	x = tf.keras.layers.Activation('relu')(x)

	return x

def affine(x, neurons):
	"""
	Affine layer, Batch Norm 
	"""
	x = tf.keras.layers.Dense(neurons, activation='relu')(x)
	x = tf.keras.layers.BatchNormalization()(x)

	return x