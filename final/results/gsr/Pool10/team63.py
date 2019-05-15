import sys
import random
import signal
import time
import copy
import traceback

class Team63():
	def __init__(self):
		self.bestVal = -10000000
		#best move's location 
		self.bestcell = (-1, -1, -1)
		self.player1 = '-'
		self.player2 = '-'
		#Weight Variables
		self.cellWeight1 = 3
		self.cellWeight2 = 27
		self.celloppweight = 81
		self.smallboardwon = 400
		self.SBWeight1 = 2187
		self.SBWeight2 = 6561
		self.SBWon = 19683 #won the game
		
		#Cell count variables
		self.cellcount1x = 0
		self.cellcount2x = 0 
		self.cellcount3x = 0 
		self.cellcount1o = 0
		self.cellcount2o = 0 
		self.cellcount3o = 0 
		self.cellcountopp = 0

		#SB count variables
		self.SBcount1x = 0
		self.SBcount2x = 0 
		self.SBcount3x = 0 
		self.SBcount1o = 0
		self.SBcount2o = 0 
		self.SBcount3o = 0
		
		self.sbs_score = 0 
		self.game_score = 0
		self.start = 0.0
		self.limit = 23
		self.chance = 0

		self.sb3x3 = 0 #for bonus move

	def move(self, board, old_move, flag):

		self.chance += 1
		self.bestVal = -10000000
		self.bestcell = (-1, -1, -1)

		if (flag == 'x'):
			self.player1 = 'x'
			self.player2 = 'o'
		else:
			self.player1 = 'o'
			self.player2 = 'x'

		# if(self.chance == 1 and self.player1 == 'x'):
		# 	return(0,4,4)
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed 
		cells = board.find_valid_move_cells(old_move)
		#return cells[random.randrange(len(cells))]#instead of this, we have to use the algo to find optimal cell
		for cell in cells:
			#compute evaluation function for this move 
			# board.big_boards_status[cell[0]][cell[1]][cell[2]] = self.player1;
			board.update(old_move, cell, self.player1 )

			if board.small_boards_status[cell[0]] [cell[1]/3] [cell[2]/3] == '-':
				moveVal = self.minimax(board, 0, 1, cell, -10000000, 10000000)
			else:
				moveVal = self.minimax(board, 0, 0, cell, -10000000, 10000000)

			board.big_boards_status[cell[0]] [cell[1]] [cell[2]] = '-';
			board.small_boards_status[cell[0]] [cell[1]/3] [cell[2]/3] = '-';
			# print cell
			# print moveVal

			if (moveVal > self.bestVal):
				self.bestcell = cell
				self.bestVal = moveVal

		print self.bestcell
		print self.bestVal
		

		# age=input("What is ur age")
		return self.bestcell;

	def minimax(self, board, depth, isMax, cell, alpha, beta):

		self.start = time.time()

		if depth == 3:
			score,status = self.heuristic(board, isMax);
			return score
		
		#if max or min player has won
		winner = board.find_terminal_state();
		if(winner[0] == self.player1):
			return 10000000
		if(winner[0] == self.player2):
			return -10000000
		if(winner[1] == 'DRAW'):
			return 0
		if(time.time() - self.start > self.limit):
			return self.bestVal

		# #if it's a draw and no more moves possible
		# if (self.isMovesLeft(board,cell)==0):
		# 	return 0

		if(isMax == 1):
			
			best = -10000000;
			cells = board.find_valid_move_cells(cell)
			
			for i in cells:
				
				# board.big_boards_status[i[0]] [i[1]] [i[2]] = self.player2;
				board.update(cell, i, self.player2 )
				
				if board.small_boards_status[i[0]] [i[1]/3] [i[2]/3] == '-':
					best = max(best, self.minimax(board, depth+1, not(isMax), i, alpha, beta) )
				else:
					best = max(best, self.minimax(board, depth+1, isMax, i, alpha, beta) )
				
				#revert back
				board.big_boards_status[i[0]] [i[1]] [i[2]] = '-';
				board.small_boards_status[i[0]] [i[1]/3] [i[2]/3] = '-';

				alpha = max( alpha, best)
				if (beta <= alpha):
					break
			return best;

		else:
			best = 10000000;
			cells = board.find_valid_move_cells(cell)
			for i in cells:
				
				# board.big_boards_status[i[0]] [i[1]] [i[2]] = self.player1;
				board.update(cell, i, self.player1 )
				if board.small_boards_status[i[0]] [i[1]/3] [i[2]/3] == '-':
					best = min(best, self.minimax(board, depth+1, not(isMax), i, alpha, beta) );
				else:
					best = min(best, self.minimax(board, depth+1, isMax, i, alpha, beta) );

				#revert back
				board.big_boards_status[i[0]] [i[1]] [i[2]] = '-';
				board.small_boards_status[i[0]] [i[1]/3] [i[2]/3] = '-';

				beta = min( beta, best)
				if (beta <= alpha):
					break
			return best;


	#calculating cellcount variables
	def calculate_gameStatus(self, number_of_x, number_of_o):
		if(number_of_x == 1):
			self.SBcount1x += 1;
		elif(number_of_x == 2):
			self.SBcount2x += 1;
		elif(number_of_o == 1):
			self.SBcount1o += 1;
		elif(number_of_o == 2):
			self.SBcount2o += 1;
		elif(number_of_o == 3):
			self.SBcount3o += 1;
		elif(number_of_x == 3):
			self.SBcount3x += 1;

	def reinitialize(self):
		#re-initialize these values for next iteration of smallboards. 
		self.cellcount1x = 0
		self.cellcount2x = 0 
		self.cellcount3x = 0 
		self.cellcount1o = 0
		self.cellcount2o = 0 
		self.cellcount3o = 0
		self.cellcountopp = 0

	def reinitialize_gameStatus(self):
		#re-initialize these values for next iteration of smallboards. 
		self.SBcount1x = 0
		self.SBcount2x = 0 
		self.SBcount3x = 0 
		self.SBcount1o = 0
		self.SBcount2o = 0 
		self.SBcount3o = 0

	#calculating cellcount variables
	def calculate_sbScore(self, number_of_x, number_of_o):
		if(number_of_x == 1 and number_of_o == 0):
			self.cellcount1x  += 1;
		elif(number_of_x == 2 and number_of_o == 0):
			self.cellcount2x  += 1;
		elif(number_of_o == 1 and number_of_x == 0):
			self.cellcount1o  += 1;
		elif(number_of_o == 2 and number_of_x == 0):
			self.cellcount2o  += 1;
		elif(number_of_o == 3):
			self.cellcount3o  += 1;
		elif(number_of_x == 3):
			self.cellcount3x  += 1;
		elif(number_of_o == 2 and number_of_x == 1):
			self.cellcountopp += 1;

	#check if smallboard has been won
	def check_win(self):
		# print("checking win")
		if(self.cellcount3x > 0):
			self.reinitialize();
			# print("smallboardwon")
			total = self.smallboardwon
			self.sb3x3 = 1
			self.sbs_score += total;
			return 1
		
		if(self.cellcount3o > 0):
			self.reinitialize();
			total = self.smallboardwon
			# self.sb3x3 = 1
			self.sbs_score -= total;
			return 1
		
		return 0

	def check_win_gameStatus(self):
		
		if(self.SBcount3x > 0):
			# self.reinitialize_gameStatus();
			total = self.SBWon
			
			self.game_score += total;
			return 1
		if(self.SBcount3o > 0):
			# self.reinitialize_gameStatus();
			total = self.SBWon
			self.game_score -= total
			return 1
		
		return 0

	def heuristic(self, board, isMax):
		
		# original heuristic
		# winner = board.find_terminal_state();
		# if(winner[0] == 'x'):
		# 	return 10;
		# elif(winner[0] == 'o'):
		# 	return -10;
		# else:
		# 	return 0;

		self.sbs_score = 0;
		self.game_score = 0;
		heuristic_score = 0;
		self.sb3x3 = 0;
		
		#calculating smallboard score. We have the board object with us. Let's visit each smallboard and calculate its score
		#There are 3 rows of small boards 
		
		#First row of small boards i.e cell rows(0-2)
		index1 = 0;
		for k in range(2): #Big boards 1 and 2
			
			index2 = 0; #Column number of small boards, gets incremented at the end of this loop. 
			for l in range(3): # Going through 3 small boards in one big board
				
				#Rows of the smallboard
				for i in range(index1, index1+3):
					number_of_x = 0;
					number_of_o = 0;
					for j in range(index2, index2+3):
						if ( board.big_boards_status[k][i][j] == self.player1):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2):
							number_of_o += 1;
					self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][1][1] == 'x' and k==0 and l==0:
				# 	print self.cellcount1x

				#Columns of the smallboard
				for j in range(index2, index2+3):
					number_of_x = 0;
					number_of_o = 0;
					for i in range(index1, index1+3):
						if ( board.big_boards_status[k][i][j] == self.player1):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2):
							number_of_o += 1;
					self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][1][7] == 'x' and k==0 and l==2:
				# 		print self.cellcount1x

				#Major Diagonals of the smallboard
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+3):
					
					for j in range(index2, index2+3):
						if ( board.big_boards_status[k][i][j] == self.player1 and i + index2 == j):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2 and i + index2 == j):
							number_of_o += 1;
				self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][1][7] == 'x' and k==0 and l==2:
				# 	print self.cellcount1x

				#Minor Diagonals of the smallboard
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+3):
					
					for j in range(index2, index2+3):
						if ( board.big_boards_status[k][i][j] == self.player1 and i + j - 2 == index2):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2 and i + j - 2 == index2):
							number_of_o += 1;
				self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][1][7] == 'x' and k==0 and l==2:
				# 	print self.cellcount1x
				# 	print self.cellcount2x

				#checking if smallboard is won
				ans = self.check_win();
				
				if(ans == 0):
				#applying our formula for calculating score for this smallboard
					total_myscore = (self.cellWeight1 * self.cellcount1x * self.cellcount1x) + (self.cellWeight2 * self.cellcount2x * self.cellcount2x) + (self.celloppweight * self.cellcountopp * self.cellcountopp)
					total_oppscore = (self.cellWeight1 * self.cellcount1o * self.cellcount1o) + (self.cellWeight2 * self.cellcount2o * self.cellcount2o)
					total = total_myscore - total_oppscore;

					self.sbs_score += total;

					# if board.big_boards_status[0][0][0] == 'x' and k==0 and l==0:
					# 	print self.cellcount1x
					# 	print self.cellcount2x
					# 	print self.sbs_score

					#re-initialize these values for next iteration of smallboards.
					self.reinitialize();
				#Move on to next smallboard in that row of smallboards i.e cell columns += 3
				index2 += 3;

		#Second row of smallboards i.e cell rows(3-5)
		index1 = 3;
		for k in range(2): #Big boards 1 and 2
			
			index2 = 0; #Column number of small boards, gets incremented at the end of this loop. 
			for l in range(3): # Going through 3 small boards in one big board
				
				#Rows of the smallboard
				for i in range(index1, index1+3):
					number_of_x = 0;
					number_of_o = 0;
					for j in range(index2, index2+3):
						if ( board.big_boards_status[k][i][j] == self.player1):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2):
							number_of_o += 1;
					self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][0][0] == 'x' and k==0 and l==1:
				# 		print self.cellcount1o

				#Columns of the smallboard
				for j in range(index2, index2+3):
					number_of_x = 0;
					number_of_o = 0;
					for i in range(index1, index1+3):
						if ( board.big_boards_status[k][i][j] == self.player1):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2):
							number_of_o += 1;
					self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][0][0] == 'x' and k==0 and l==1:
				# 	print self.cellcount1o

				#Major Diagonals of the smallboard
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+3):
					
					for j in range(index2, index2+3):
						if ( board.big_boards_status[k][i][j] == self.player1 and (i - j) % 3 == 0 ):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2 and (i - j) % 3 == 0 ):
							number_of_o += 1;
				self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][0][0] == 'x' and k==0 and l==1:
				# 	print self.cellcount1o

				#Minor Diagonals of the smallboard
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+3):
					
					for j in range(index2, index2+3):
						if ( board.big_boards_status[k][i][j] == self.player1 and i + j - index2 == 5):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2 and i + j - index2 == 5):
							number_of_o += 1;
				self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][1][7] == 'x' and k==0 and l==2:
				# 	print self.cellcount1x
				# 	print self.cellcount2x

				#checking if smallboard is won
				ans = self.check_win();
				
				if(ans == 0):
				#applying our formula for calculating score for this smallboard
					total_myscore = (self.cellWeight1 * self.cellcount1x * self.cellcount1x) + (self.cellWeight2 * self.cellcount2x * self.cellcount2x) + (self.celloppweight * self.cellcountopp * self.cellcountopp)
					total_oppscore = (self.cellWeight1 * self.cellcount1o * self.cellcount1o) + (self.cellWeight2 * self.cellcount2o * self.cellcount2o)
					total = total_myscore - total_oppscore;

					self.sbs_score += total;

					# if board.big_boards_status[0][0][0] == 'x' and k==0 and l==1:
					# 	print self.cellcount1x
					# 	print self.cellcount2x
					# 	print self.sbs_score

					#re-initialize these values for next iteration of smallboards.
					self.reinitialize();
				#Move on to next smallboard in that row of smallboards i.e cell columns += 3
				index2 += 3;

		#Third row of smallboards i.e cell rows(6-8)
		index1 = 6;
		for k in range(2): #Big boards 1 and 2
			
			index2 = 0; #Column number of small boards, gets incremented at the end of this loop. 
			for l in range(3): # Going through 3 small boards in one big board
				
				#Rows of the smallboard
				for i in range(index1, index1+3):
					number_of_x = 0;
					number_of_o = 0;
					for j in range(index2, index2+3):
						if ( board.big_boards_status[k][i][j] == self.player1):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2):
							number_of_o += 1;
					self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][1][7] == 'x' and k==0 and l==2:
				# 		print self.cellcount1x

				#Columns of the smallboard
				for j in range(index2, index2+3):
					number_of_x = 0;
					number_of_o = 0;
					for i in range(index1, index1+3):
						if ( board.big_boards_status[k][i][j] == self.player1):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2):
							number_of_o += 1;
					self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][1][7] == 'x' and k==0 and l==2:
				# 		print self.cellcount1x

				#Major Diagonals of the smallboard
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+3):
					
					for j in range(index2, index2+3):
						if ( board.big_boards_status[k][i][j] == self.player1 and i - j + index2 == 6):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2 and i - j + index2 == 6):
							number_of_o += 1;
				self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][1][7] == 'x' and k==0 and l==2:
				# 	print self.cellcount1x

				#Minor Diagonals of the smallboard
				number_of_x = 0;
				number_of_o = 0;
				for i in range(index1, index1+3):
					
					for j in range(index2, index2+3):
						if ( board.big_boards_status[k][i][j] == self.player1 and i + j - index2 == 8):
							number_of_x += 1;
						if ( board.big_boards_status[k][i][j] == self.player2 and i + j - index2 == 8):
							number_of_o += 1;
				self.calculate_sbScore(number_of_x, number_of_o)

				# if board.big_boards_status[0][1][7] == 'x' and k==0 and l==2:
				# 	print self.cellcount1x
				# 	print self.cellcount2x

				#checking if smallboard is won
				ans = self.check_win();
				
				if(ans == 0):
				#applying our formula for calculating score for this smallboard
					total_myscore = (self.cellWeight1 * self.cellcount1x * self.cellcount1x) + (self.cellWeight2 * self.cellcount2x * self.cellcount2x) + + (self.celloppweight * self.cellcountopp * self.cellcountopp)
					total_oppscore = (self.cellWeight1 * self.cellcount1o * self.cellcount1o) + (self.cellWeight2 * self.cellcount2o * self.cellcount2o)
					total = total_myscore - total_oppscore;
					
					# if board.big_boards_status[0][1][7] == 'x' and k==0 and l==2:
					# 	print self.cellcount1x
					# 	print self.cellcount2x
					# 	print total_myscore

					self.sbs_score += total;

					#re-initialize these values for next iteration of smallboards.
					self.reinitialize();
				#Move on to next smallboard in that row of smallboards i.e cell columns += 3
				index2 += 3;

		#Okay, now we have calculate score of each smallboard. Now let's calculate game status or game_score!
		#GameStatus ---------------------------------------
		ind1 = 0
		for k in range(2):#BigBoard 1 & 2
			ind2 = 0;
			
			#rows
			for i in range(ind1, ind1+3):
				number_of_x = 0;
				number_of_o = 0;
				for j in range(ind2, ind2+3):
					if ( board.small_boards_status[k][i][j] == self.player1):
						number_of_x += 1;
					if ( board.small_boards_status[k][i][j] == self.player2):
						number_of_o += 1;
				self.calculate_gameStatus(number_of_x, number_of_o)

			#columns
			for i in range(ind1, ind1+3):
				number_of_x = 0;
				number_of_o = 0;
				for j in range(ind2, ind2+3):
					if ( board.small_boards_status[k][j][i] == self.player1):
						number_of_x += 1;
					if ( board.small_boards_status[k][j][i] == self.player2):
						number_of_o += 1;
				self.calculate_gameStatus(number_of_x, number_of_o)

			#major diagonal
			number_of_x = 0;
			number_of_o = 0;
			for i in range(ind1, ind1+3):
				if ( board.small_boards_status[k][i][i] == self.player1):
					number_of_x += 1;
				if ( board.small_boards_status[k][i][i] == self.player2):
					number_of_o += 1;
			self.calculate_gameStatus(number_of_x, number_of_o)

			#minor diagonal
			number_of_x = 0;
			number_of_o = 0;
			for i in range(ind1, ind1+3):
				if ( board.small_boards_status[k][i][2-i] == self.player1):
					number_of_x += 1;
				if ( board.small_boards_status[k][i][2-i] == self.player1):
					number_of_o += 1;
			self.calculate_gameStatus(number_of_x, number_of_o)
			
			ans = self.check_win_gameStatus();
			
			if(ans == 0):

				total_myscore = (self.SBWeight1 * self.SBcount1x * self.SBcount1x) + (self.SBWeight2 * self.SBcount2x * self.SBcount2x)
				total_oppscore = (self.SBWeight1 * self.SBcount1o * self.SBcount1o) + (self.SBWeight2 * self.SBcount2o * self.SBcount2o)
				total = total_myscore - total_oppscore;
		
				self.game_score += total
			
			self.reinitialize_gameStatus();

		#So now we calculate the heuristic score for that node in the tree.
		heuristic_score = self.sbs_score + self.game_score
		game_won = 0
		
		return(heuristic_score, game_won)

	def isMovesLeft(self, board, cell):
		cells = board.find_valid_move_cells(cell)
		if not cells:
			return 0;
		else:
			return 1;










		

