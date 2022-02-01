import tensorflow as tf
import numpy as np

import sys 

from util import fen_to_matrix, invert_fen

model = tf.keras.models.load_model('combined/model11.h5')
model = tf.keras.models.load_model('combined_to/model7.h5')

# fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0' # 51 is d4
# fen = 'rnb1kbnr/pppp1ppp/8/4p1q1/4P3/3P4/PPP2PPP/RNBQKBNR w KQkq - 1 3' # 58
# fen = 'rnb1kbnr/1ppp1ppp/p4q2/4p1B1/4P3/3P4/PPP2PPP/RN1QKBNR w KQkq - 0 4' # 30 
# fen = 'r1bqkbnr/ppp2ppp/2np4/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 4' # 31
# fen = 'rnbqkb1r/pppp1ppp/8/4p3/3PP3/2N2N2/PPP2PPn/R1BQKB1R w KQkq - 0 5' # 45 or 63

# fen = 'r1bqkbnr/pppp1ppp/2n5/4p1N1/4P3/8/PPPP1PPP/RNBQKB1R b KQkq - 3 3' # 3
fen = 'rnbqkbnr/pppp1ppp/B7/4p3/4P3/8/PPPP1PPP/RNBQK1NR b KQkq - 1 2' # 1 or 9

col = fen.split()[1]

if col == 'w':
	a = fen_to_matrix(fen, reshape=True)
else:
	fen = invert_fen(fen)
	a = fen_to_matrix(fen, reshape=True)

p = model.predict([a,])
p = p.reshape((8, 8))

if col == 'b':
	p = np.flip(p, axis=0)

print(np.around(p, decimals=2))
ans = np.argmax(p)

print(ans) 