import tensorflow as tf
import numpy as np

import sys 

from model import model
from util import fen_to_matrix, invert_fen

TRAIN_MOVE_FROM = True

BATCH_SIZE = 1024
VAL_SIZE = BATCH_SIZE * 10
EPOCHS = 100
STEPS_PER_EPOCH = 10_000

def number_to_board(num):
    row = num // 8 
    col = num % 8

    a = np.zeros((8, 8))
    a[row][col] = 1
    return a

def preprocess(inp):
    def helper(inp):
        fen, moved_from, moved_to = inp.numpy().decode().split('  ')
        moved_from = int(moved_from) 
        moved_to = int(moved_to) 

        fen = fen.split()
        col = fen[1]
        fen = fen[0]

        if col == 'b':
            fen = invert_fen(fen)
            moved_from = 63 - moved_from
            moved_to = 63 - moved_to

        if TRAIN_MOVE_FROM:
            moved_from_board = number_to_board(num=moved_from)
        else:
            moved_to_board = number_to_board(num=moved_to)

        board = fen_to_matrix(fen=fen)

        if col == 'b':
            if TRAIN_MOVE_FROM:
                moved_from_board = np.flip(moved_from_board, axis=1)
            else:
                moved_to_board = np.flip(moved_to_board, axis=1)

        if TRAIN_MOVE_FROM:
            return board, moved_from_board
        else:
            return board, moved_to_board
    
    # return tf.random.normal((8, 8))
    return tf.py_function(func=helper, inp=[inp], Tout=[tf.int32, tf.int32])

ds = tf.data.TextLineDataset('gm.txt').repeat()
ds = ds.shuffle(buffer_size=1000)
# ds = ds.batch(BATCH_SIZE)
ds = ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)

train = ds.skip(VAL_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
val = ds.take(VAL_SIZE).batch(BATCH_SIZE)

class SaveModel(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        name = 'gm_from/model{}.h5'.format(epoch + 1)
        self.model.save(name, overwrite=True,)

cbk = SaveModel()

tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir='logs/callback',
    profile_batch='10,14',
)

# print('Fitting...')

# model.load_weights('checkpoints/ckpt')

model.fit(
    train,
    epochs=EPOCHS, 
    steps_per_epoch=STEPS_PER_EPOCH, 
    validation_data=val,
    callbacks=[tensorboard_callback],
    verbose=0,
)

# https://us-central1-spearsx.cloudfunctions.net/chesspic-fen-image/rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR
