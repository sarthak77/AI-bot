# Minimax with bonus taken care of. Works for now. New evaluate, new move()
import copy
import time
import random

class Team18():
	def __init__(self):
		self.flag = 0
		self.depth = 0;
		self.time_limit = 20
		self.move_call_count = 0
		self.older_move_call_count = 0
		self.count_to_2 = 0
		self.was_bonus_move = 0
		self.zobrist_table = [[[random.randint(0, 1000) for x in range(2)] for y in range(8)] for z in range(8)]
		self.time_started = 0
		self.time_taken = 0
		self.empty_small_square =  ([['-' for i in range(3)] for j in range(3)], [['-' for i in range(3)] for j in range(3)])

	# def calculate_zobrist_hash_of_current_board (self, board):
	# 	hash = 0
	# 	for index1, cell1 in enumerate(board.big_boards_status):
	# 		for index2, cell2 in enumerate (cell1):
	# 			for index3, cell3 in enumerate (cell2):
	# 				print("cell->", cell3, index1, index2, index3)
	# 				if cell3 is not '-':
	# 					piece = cell3
	# 					print("index1 = ", index1, "index2 = ", index2, "index3 = ", index3)
	# 					hash = hash ^ self.zobrist_table[index1][index2][index3]

	def minimax (self, board, depth, player, old_move, alpha, beta, wasBonus):
		# print("Minimax at depth = ", depth, " player = ", player, " and old move = ", old_move)
		# print("depth = ", depth)

		if depth == 0:
			return self.evaluate (board, player, old_move,(-1,-1,-1))

		cells = board.find_valid_move_cells(old_move)

		self.time_taken = time.time() - self.time_started

		if self.time_taken > self.time_limit:
			# print("breaking cuz no time")
			# print("broken here")
			return self.evaluate (board, player, old_move,(-1,-1,-1))
		
		if player is "x":
			best_case = -100000
			for i in cells:
				self.time_taken = time.time() - self.time_started
				# temp_board = BigBoard() # new board cuz can't update and undo the main board
				temp_board = copy.deepcopy(board)

				a = temp_board.update (old_move, i, 'x')

				if a[1] is False:
					temp_case = self.minimax (temp_board, depth-1, "o", i, alpha, beta, False)
				if a[1] is True:
					if wasBonus is False:
						temp_case = self.minimax (temp_board, depth-1, "x", i, alpha, beta, True)
					elif wasBonus is True:
						temp_case = self.minimax (temp_board, depth-1, "o", i, alpha, beta, False)

				best_case = max(best_case, temp_case)
				alpha = max (alpha, best_case)

				if beta <= alpha:
					# print("pruned")
					# print(self.time_taken)
					break

			return best_case

		elif player is "o":
			best_case = 100000
			for i in cells:
				self.time_taken = time.time() - self.time_started
				# temp_board = BigBoard() # new board cuz can't update and undo the main board
				temp_board = copy.deepcopy (board)

				a = temp_board.update (old_move, i, 'o')

				if a[1] is False:
					temp_case = self.minimax (temp_board, depth-1, "x", i, alpha, beta, False)
				if a[1] is True:
					if wasBonus is False:
						temp_case = self.minimax (temp_board, depth-1, "o", i, alpha, beta, True)
					elif wasBonus is True:
						temp_case = self.minimax (temp_board, depth-1, "x", i, alpha, beta, False)

				best_case = min(best_case, temp_case)
				beta = min(beta, best_case)

				if beta <= alpha:
					break

			return best_case

	def evaluate (self, board, player, move, old_move):
		# print("move is", move)

		state_score = 0 

		terminal_state = board.find_terminal_state()
		if terminal_state[1] == "WON":
			if terminal_state[0] == 'x':
				# state_score += 1000
				return 10000
			elif terminal_state[0] == 'o':
				# state_score += -1000
				return -10000
		if terminal_state[0] == "CONTINUE":
			state_score += 0
			# return 0


		if move[0] in [0,1]:
			if move[1] in [1,4,7]:
				if move[2] in [1,4,7]:
					state_score += 3.5
			if move[1] in [0,2,3,5,6,8]:
				if move[2] in [0,2,3,5,6,8]:
					state_score += 2


		tboard = copy.deepcopy (board)
		t2board = copy.deepcopy (board)
		t3board = copy.deepcopy (board)
		t4board = copy.deepcopy (board)
		t5board = copy.deepcopy (board)

		
		a = tboard.update (old_move, move, player)
		block_score = 0
		if a[1] is True:
			if move[1] in [3,4,5]:
				if move[2] in [3,4,5]:
					block_score = 30
			elif move[1] in [0,1,2]:
				if move[2] in [0,1,2,6,7,8]:
					block_score = 25
			else:
				block_score = 20
			
		state_score += block_score

		if player is "o":
			state_score *= -1


		if player is "x":
			a = t2board.update (old_move, move, "o")
			if a[1] is True:
				state_score += 120
				# print ("blocscore=", state_score)
			else:
				a = t3board.update (old_move, move, player)
				cells = t3board.find_valid_move_cells(move)
				for i in cells:
					x,y,z = i
					if t3board.big_boards_status[x][1+(y/3)*3][1+(z/3)*3] == "o":
						state_score -= 4
					a = t5board.update (move, i, "o")
					if a[1] is True:
						state_score -= 40
					a = t4board.update (move, i, "x")
					if a[1] is True:
						state_score -= 30
			
		else:
			a = t2board.update (old_move, move, "x")
			if a[1] is True:
				state_score -= 120
				# print ("blockedxscore=", state_score)
				# print ("move", move)
			else:
				a = t3board.update (old_move, move, player)
				cells = t3board.find_valid_move_cells(move)
				for i in cells:
					x,y,z = i
					if t3board.big_boards_status[x][1+(y/3)*3][1+(z/3)*3] == "x":
						state_score += 4
					a = t5board.update (move, i, "x")
					if a[1] is True:
						state_score += 40
						# print ("dont send")
					a = t4board.update (move, i, "o")
					if a[1] is True:
						state_score += 30

		
		# print ("finscore=", state_score)

		return state_score

	def move(self, board, old_move, flag):

		# print("move called")

		self.time_started = time.time()

		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed[]

		best_case_x = -100000
		best_case_o = 100000
		best_move_index = -1
		final_best_move_index = -1

		#was bonus?

		cells = board.find_valid_move_cells(old_move)

		for j in range(4):
			self.depth = 3 + j*2;
			# print("starting")

			if flag is 'x':
				for index, cell in enumerate(cells):
					if (time.time() - self.time_started) > self.time_limit:
						break

					temp_board = copy.deepcopy (board)

					a = temp_board.update (old_move, cell, 'x')

					temp_case = self.evaluate(temp_board, flag, cell, old_move)

					# print("1 temp_case = ", temp_case)

					if a[1] is True:
						if self.was_bonus_move is False:
							temp_case += self.minimax (temp_board, self.depth, 'x', cell, -1000000, 1000000, True)
						elif self.was_bonus_move is True:
							temp_case += self.minimax (temp_board, self.depth, 'o', cell, -1000000, 1000000, False)
					elif a[1] is False:
						# print("temp_case = ", temp_case)
						# print("other = ", self.minimax (temp_board, self.depth, 'o', cell, -1000000, 1000000, False))
						temp_case += self.minimax (temp_board, self.depth, 'o', cell, -1000000, 1000000, False)

					# print("temp move = ", temp_case, " at cell ", cells[index])

					# print("temp_case = ", temp_case, "temp cell", cells[index])

					if temp_case >= best_case_x:
						best_case_x = temp_case
						best_move_index = index

			elif flag is 'o':
				for index, cell in enumerate(cells):
					if (time.time() - self.time_started) > self.time_limit:
						break
					
					temp_board = copy.deepcopy (board)
					a = temp_board.update (old_move, cell, 'o')

					print("bitachssss", cell)

					temp_case = self.evaluate(temp_board, flag, cell, old_move)

					if a[1] is True:
						if self.was_bonus_move is False:
							temp_case += self.minimax (temp_board, self.depth, 'o', cell, -1000000, 1000000, True)
						if self.was_bonus_move is True:
							temp_case += self.minimax (temp_board, self.depth, 'x', cell, -1000000, 1000000, False)
					if a[1] is False:
						temp_case += self.minimax (temp_board, self.depth, 'x', cell, -1000000, 1000000, False)

					if temp_case <= best_case_o:
						best_case_o = temp_case
						best_move_index = index

			if (time.time() - self.time_started) > self.time_limit:
				break

			# print("curerntly best move is -> ", best_move_index)



		self.depth = 0

		# if self.was_bonus_move is True:
		# 	self.was_bonus_move = False

		temp_board = copy.deepcopy (board)
		a = temp_board.update (old_move, cells[best_move_index], flag)

		if a[1] is True and self.was_bonus_move is False:
			self.was_bonus_move = True
		else:
			self.was_bonus_move = False

		# print("selected best move ->", best_move_index)
		return cells[best_move_index]
		# return cells [random.randrange(len(cells))]