import numpy as np
import pygame
import random
import chess

from globals import square_size
import globals

class HumanPlayer:
	def __init__(self, colour):
		self.colour = colour 
		self.move_from_square = None

	def move(self, board, event, human_white):
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			square = self.coordinates_to_square(coords=pygame.mouse.get_pos(), human_white=human_white)
			
			if self.move_from_square is None:
				legal_moves = list(map(lambda move: move.uci()[: 2] == square, board.legal_moves))
				if not any(legal_moves):
					return False

				self.move_from_square = square 

				globals.from_square = self.coordinates_to_numbers(pygame.mouse.get_pos())

				return False

			else:
				move_uci = self.move_from_square + square
				move_is_legal = move_uci in list(map(lambda move: move.uci()[: 4], board.legal_moves))

				if not move_is_legal:
					self.move_from_square = square

					try:
						piece = board.piece_at(chess.parse_square(square))
						if piece:
							globals.from_square = self.coordinates_to_numbers(pygame.mouse.get_pos())
						else:
							globals.from_square = None
					except:
						pass

					return False

				move = chess.Move.from_uci(move_uci)

				piece = board.piece_at(chess.parse_square(move_uci[: 2]))
				if piece.piece_type == 1:
					if (piece.color and move_uci[3] == '8') or (not piece.color and move_uci[3] == '1'):
						move.promotion = chess.QUEEN

				board.push(move)

				self.move_from_square = None

				globals.to_square = self.coordinates_to_numbers(pygame.mouse.get_pos())

				return True

	@staticmethod 
	def coordinates_to_numbers(coords):
		row = coords[0] // square_size 
		col = coords[1] // square_size 

		return row, col
	
	@staticmethod
	def coordinates_to_square(coords, human_white):
		letter = ord('a') + coords[0] // square_size
		number = coords[1] // square_size + 1

		if human_white:
			number = 9 - number
		else:
			letter = 2 * ord('a') + 7 - letter

		letter = chr(letter)

		return '{}{}'.format(letter, number)

class AIPlayer:
	def __init__(self, colour, from_model, to_model):
		self.colour = colour 

		self.from_model = from_model
		self.to_model = to_model
	
	def move(self, board, human_white):
		fen = board.fen()

		if self.colour == 'black':
			fen = self.invert_fen(fen=fen)

		arr = self.fen_to_matrix(fen=fen)
		arr = arr.reshape((1,) + arr.shape)

		from_matrix = self.from_model.predict(arr).reshape((8, 8))
		to_matrix = self.to_model.predict(arr).reshape((8, 8))

		if self.colour == 'black':
			from_matrix = np.flip(from_matrix, axis=0)
			to_matrix = np.flip(to_matrix, axis=0)

		moves = []
		for move in list(board.legal_moves):
			from_row, from_col, to_row, to_col = self.uci_to_row_col(move.uci())
			
			score = from_matrix[from_row][from_col] * to_matrix[to_row][to_col]
			moves.append((move, score))
		moves.sort(key=lambda x: x[1], reverse=True)

		if board.fullmove_number < 4:
			rand_idx = random.randint(0, 5)
			move = moves[rand_idx][0]
		else:
			move = moves[0][0]

		board.push(move)

		uci = move.uci()
		globals.from_square = [int(ord(uci[0]) - ord('a')), int(uci[1]) - 1]
		globals.to_square = [int(ord(uci[2]) - ord('a')), int(uci[3]) - 1]

		if human_white:
			globals.from_square[1] = 7 - globals.from_square[1]
			globals.to_square[1] = 7 - globals.to_square[1]
		else:
			globals.from_square[0] = 7 - globals.from_square[0]
			globals.to_square[0] = 7 - globals.to_square[0]

	@staticmethod
	def uci_to_row_col(uci):
		sq_from = uci[: 2]
		sq_to = uci[2 :]

		def parse_square(sq):
			col = ord(sq[0]) - ord('a')
			row = 7 - (int(sq[1]) - 1)

			return row, col

		return parse_square(sq_from) + parse_square(sq_to)

	@staticmethod
	def fen_to_matrix(fen):
		fen = fen.split()[0]
		
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

	@staticmethod
	def invert_fen(fen):
		fen = fen.split()[0]

		rows = fen.split('/')
		rows.reverse()
		for i in range(8):
			rows[i] = rows[i].swapcase()
		return '/'.join(rows)
