import tensorflow as tf 

model = tf.keras.models.load_model('gm_to/model3.h5')
model.save_weights('checkpoints/ckpt')