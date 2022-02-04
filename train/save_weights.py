import tensorflow as tf 

model = tf.keras.models.load_model('gm_to/model26.h5', compile=False)
model.save_weights('checkpoints/ckpt')