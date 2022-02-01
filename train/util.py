import numpy as np

def fen_to_matrix(fen, reshape=False, debug=False):
	fen = fen.split()[0]
	
	if not debug:
		piece_dict = {
			'p' : [1,0,0,0,0,0,0,0,0,0,0,0],
			'P' : [0,0,0,0,0,0,1,0,0,0,0,0],
			'n' : [0,1,0,0,0,0,0,0,0,0,0,0],
			'N' : [0,0,0,0,0,0,0,1,0,0,0,0],
			'b' : [0,0,1,0,0,0,0,0,0,0,0,0],
			'B' : [0,0,0,0,0,0,0,0,1,0,0,0],
			'r' : [0,0,0,1,0,0,0,0,0,0,0,0],
			'R' : [0,0,0,0,0,0,0,0,0,1,0,0],
			'q' : [0,0,0,0,1,0,0,0,0,0,0,0],
			'Q' : [0,0,0,0,0,0,0,0,0,0,1,0],
			'k' : [0,0,0,0,0,1,0,0,0,0,0,0],
			'K' : [0,0,0,0,0,0,0,0,0,0,0,1],
			'.' : [0,0,0,0,0,0,0,0,0,0,0,0],
		}
	else:
		piece_dict = {
			'p' : [0,1,0,0,0,0,0,0,0,0,0,0,0],
			'P' : [0,0,0,0,0,0,0,1,0,0,0,0,0],
			'n' : [0,0,1,0,0,0,0,0,0,0,0,0,0],
			'N' : [0,0,0,0,0,0,0,0,1,0,0,0,0],
			'b' : [0,0,0,1,0,0,0,0,0,0,0,0,0],
			'B' : [0,0,0,0,0,0,0,0,0,1,0,0,0],
			'r' : [0,0,0,0,1,0,0,0,0,0,0,0,0],
			'R' : [0,0,0,0,0,0,0,0,0,0,1,0,0],
			'q' : [0,0,0,0,0,1,0,0,0,0,0,0,0],
			'Q' : [0,0,0,0,0,0,0,0,0,0,0,1,0],
			'k' : [0,0,0,0,0,0,1,0,0,0,0,0,0],
			'K' : [0,0,0,0,0,0,0,0,0,0,0,0,1],
			'.' : [0,0,0,0,0,0,0,0,0,0,0,0,0],
		}

	mat = []

	rows = fen.split('/')
	for row in rows:
		a = []
		for ch in str(row):
			if ch.isdigit():
				for _ in range(int(ch)):
					a.append(piece_dict['.'])
			else:
				try:	
					a.append(piece_dict[ch])
				except:
					pass
		mat.append(a)

	mat = np.array(mat)
	if reshape:
		mat = np.reshape(mat, (1,) + mat.shape)
	
	return mat

def invert_fen(fen):
	fen = fen.split()[0]

	rows = fen.split('/')
	rows.reverse()
	for i in range(8):
		rows[i] = rows[i].swapcase()
	return '/'.join(rows)
