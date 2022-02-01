import tensorflow as tf 

model = tf.keras.models.load_model('models/1100-elo/to.h5')
model.save_weights('checkpoints/ckpt')