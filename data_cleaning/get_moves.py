import numpy as np

import sys 

def fen_to_matrix(fen):
        fen = fen.split()[0]
        
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

        row_arr = []

        rows = fen.split('/')
        for row in rows:
            arr = []
            for ch in str(row):
                if ch.isdigit():
                    for _ in range(int(ch)):
                        arr.append(piece_dict['.'])
                else:
                    arr.append(piece_dict[ch])
            row_arr.append(arr)

        mat = np.array(row_arr)

        return mat

prev = None
prev_fen = None
cnt = 0

with open(sys.argv[1]) as in_file:
    with open(sys.argv[2], 'w') as out_file:
        for l in in_file:
            cnt += 1
            
            if cnt % 50_000 == 0:
                print('Done', cnt)

            fen = l.rstrip().split(' ')[0]
            cur = np.argmax(fen_to_matrix(fen), axis=-1)

            if prev is not None:
                dif = cur - prev
                lo = np.argmin(dif)
                hi = np.argmax(dif)
                out_file.write('{}  {}  {}\n'.format(prev_fen, lo, hi))

            prev = cur
            prev_fen = fen
