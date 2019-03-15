"""
Class for AI bot
"""
import random
import traceback
import sys
import numpy as np
from time import time
from copy import deepcopy

class Team8:
    """ 
    AI implemented 
    """  
    def __init__(self):
        """
        Initialize variables
        """
        self.default=(0,4,4)#default move
        self.limit=20#time limit
        self.start=0#start time
        self.player=0#x=1 o=0
        self.opponent=0
        self.bestmv=(0,0,0)
        self.inf = 1000
        self.bot_player = 1
        self.startdepth=1
        self.movecounter = 0
        self.maxdepth=9*9*9
        self.bonus_move_cur = [0 , 0]
        self.last_function_call = 0
        self.numsteps = 0
        self.dict = {}
        self.player_char = ['o', 'x']
        self.blockweight=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        # self.blockweight=[1,.9,1,.9,1.1,.9,1,.9,1,1,.9,1,.9,1.1,.9,1,.9,1]



    def smallboardutility(self,board,move):
        """
        Find weights of each cell
        """
        board_num = move[0]
        row_num = 3*move[1]
        col_num = 3*move[2]
        cur_big_board = board.big_boards_status[board_num]
        winning_comb = []
        winning_comb.append(np.zeros(4)) #0 for bot
        winning_comb.append(np.zeros(4)) #1 for opposition
        bot_win_cells = 0
        opp_win_cells = 0
        win_chance = np.ones(2)
        prob_chance = np.zeros(2)
        for i in range(3):
            bot_win_cells = 0
            opp_win_cells = 0
            win_chance = np.ones(2)
            prob_chance = np.zeros(2)
            for j in range(3):
                curtictoc = cur_big_board[row_num+i][col_num+j]
                if curtictoc == self.player_char[self.bot_player]:
                    win_chance[1] = 0
                    bot_win_cells+=1
                if curtictoc == self.player_char[self.bot_player^1]:
                    win_chance[0] = 0
                    opp_win_cells+=1
            if win_chance[0] == 1:
                winning_comb[0][bot_win_cells]+=1
            if win_chance[1] == 1:
                winning_comb[1][opp_win_cells]+=1

        bot_win_cells = 0
        opp_win_cells = 0
        win_chance = np.ones(2)
        prob_chance = np.zeros(2)
        for i in range(3):
            bot_win_cells = 0
            opp_win_cells = 0
            win_chance = np.ones(2)
            prob_chance = np.zeros(2)
            for j in range(3):
                curtictoc = cur_big_board[row_num+j][col_num+i]
                if curtictoc == self.player_char[self.bot_player]:
                    win_chance[1] = 0
                    bot_win_cells+=1
                if curtictoc == self.player_char[self.bot_player^1]:
                    win_chance[0] = 0
                    opp_win_cells+=1
            if win_chance[0] == 1:
                winning_comb[0][bot_win_cells]+=1
            if win_chance[1] == 1:
                winning_comb[1][opp_win_cells]+=1 

        bot_win_cells = 0
        opp_win_cells = 0
        win_chance = np.ones(2)
        prob_chance = np.zeros(2)
        for i in range(3):
            #for j in range(3):
            curtictoc = cur_big_board[row_num+i][col_num+i]
            if curtictoc == self.player_char[self.bot_player]:
                win_chance[1] = 0
                bot_win_cells+=1
            if curtictoc == self.player_char[self.bot_player^1]:
                win_chance[0] = 0
                opp_win_cells+=1
        if win_chance[0] == 1:
            winning_comb[0][bot_win_cells]+=1
        if win_chance[1] == 1:
            winning_comb[1][opp_win_cells]+=1 

        bot_win_cells = 0
        opp_win_cells = 0
        win_chance = np.ones(2)
        prob_chance = np.zeros(2)
        for i in range(3):
            #for j in range(3):
            curtictoc = cur_big_board[row_num+i][col_num+2-i]
            if curtictoc == self.player_char[self.bot_player]:
                win_chance[1] = 0
                bot_win_cells+=1
            if curtictoc == self.player_char[self.bot_player^1]:
                win_chance[0] = 0
                opp_win_cells+=1
        if win_chance[0] == 1:
            winning_comb[0][bot_win_cells]+=1
        if win_chance[1] == 1:
            winning_comb[1][opp_win_cells]+=1 

        small_util = 1.2*(winning_comb[0][1] -winning_comb[1][1]) + 4*(winning_comb[0][2] - winning_comb[1][2])
        if winning_comb[0][3] == 1:
            small_util = 17
        if winning_comb[1][3] == 1: 
            small_util = -17
        return(small_util)



    def blockutilityondraw(self,board):
        """
        Calculate utility of each cell of big board
        """
        draw_util = 0
        bot = self.player_char[self.bot_player]
        opp = self.player_char[self.bot_player^1]
        cur_small_board = board.small_boards_status
       	for m in range(2):
               for i in range(3):
                   for j in range(3):
                        if i%2 == 0 and j%2 == 0 and cur_small_board[m][i][j] == self.player_char[self.bot_player]:
                           draw_util += 4
                        elif i%2 == 0 and j%2 == 0 and cur_small_board[m][i][j] == self.player_char[self.bot_player^1]:
                           draw_util -= 4
                        elif i%2 == 1 and j%2 == 1 and cur_small_board[m][i][j] == self.player_char[self.bot_player]:
                            draw_util +=3
                        elif i%2 == 1 and j%2 == 1 and cur_small_board[m][i][j] == self.player_char[self.bot_player^1]:
                            draw_util -=3
                        elif ((i%2 == 0 and j%2 ==1) or (i%2 ==1 and j%2 == 0)) and cur_small_board[m][i][j] == self.player_char[self.bot_player^1]:
                            draw_util -=6
                        elif ((i%2 == 0 and j%2 ==1) or (i%2 ==1 and j%2 == 0)) and cur_small_board[m][i][j] == self.player_char[self.bot_player]:
                            draw_util +=6
        return draw_util



    def check_prob_win_big(self,board,board_num,row_num,col_num,player):
        cur_big_board = board.big_boards_status[board_num]
        for i in range(3):
            player_comb = 0
            for j in range(3):
                if (cur_big_board[3*row_num+i][3*col_num+j] == self.player_char[player]
                    or cur_big_board[3*row_num+i][3*col_num+j] == '-'):
                    player_comb = 1
                else:
                    player_comb = 0
                    break
            if player_comb == 1:
                return 1
        for i in range(3):
            player_comb = 0
            for j in range(3):
                if (cur_big_board[3*row_num+j][3*col_num+i] == self.player_char[player]
                    or cur_big_board[3*row_num+j][3*col_num+i] == '-'):
                    player_comb = 1
                else:
                    player_comb = 0
                    break
            if player_comb == 1:
                return 1
        for i in range(3):
            #for j in range(3):
            player_comb = 0
            if (cur_big_board[3*row_num+i][3*col_num+i] == self.player_char[player]
                or cur_big_board[3*row_num+i][3*col_num+i] == '-'):
                player_comb = 1
            else:
                player_comb = 0
                break
        if player_comb == 1:
            return 1
        for i in range(3):

            if (cur_big_board[3*row_num+i][3*col_num+2-i] == self.player_char[player]
                or cur_big_board[3*row_num+i][3*col_num+2-i] == '-'):
                player_comb = 1
            else:
                player_comb = 0
                break
        if player_comb ==1:
            return 1

        return 0



    def utility(self,board,symbol):
        """
        Heuristic function
        """
        utility=0
        util_bot = 0
        util_opp = 0
        # self.blockweight=[1,.9,1,.9,1.1,.9,1,.9,1,1,.9,1,.9,1.1,.9,1,.9,1]
        self.blockweight=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        winning_comb = []
        winning_comb.append(np.zeros(4)) #0 for bot
        winning_comb.append(np.zeros(4)) #1 for opposition
       
        for m in range(2):
            for i in range(3):
                bot_win_cells = 0
                opp_win_cells = 0
                win_chance = np.ones(2)
                prob_chance = np.zeros(2)
                lookat = []
                for j in range(3):
                    if board.small_boards_status[m][i][j] == self.player_char[self.bot_player]:
                        win_chance[1] = 0
                        bot_win_cells+=1
                    if board.small_boards_status[m][i][j] == self.player_char[self.bot_player^1]:
                        win_chance[0] = 0
                        opp_win_cells+=1
                    if board.small_boards_status[m][i][j] == 'd':
                        win_chance[0] = 0
                        win_chance[1] = 0
                    if board.small_boards_status[m][i][j] == '-':
                        prob_chance[0] =  self.check_prob_win_big(board,m,i,j,self.bot_player)
                        prob_chance[1] =  self.check_prob_win_big(board,m,i,j,self.bot_player^1)
                        if prob_chance[0] == 1 and prob_chance[1] == 1:
                            lookat.append([m,i,j])
                        if prob_chance[0] == 0:
                            win_chance[0] = 0
                        if prob_chance[1] == 0:
                            win_chance[1] = 0
                if win_chance[0] == 1:
                    winning_comb[0][bot_win_cells] +=1
                if win_chance[1] == 1:
                    winning_comb[1][opp_win_cells] +=1
                if win_chance[0]==1 or win_chance[1] ==1:
                    for z in range(len(lookat)):
                        utility+=self.smallboardutility(board,lookat[z])

        #winning_comb.append(np.zeros(4)) #0 for bot
        #winning_comb.append(np.zeros(4)) #1 for opposition
            bot_win_cells = 0
            opp_win_cells = 0
            win_chance = np.ones(2)
            prob_chance = np.zeros(2)
        #for m in range(2):
            for i in range(3):
                bot_win_cells = 0
                opp_win_cells = 0
                win_chance = np.ones(2)
                prob_chance = np.zeros(2)
                lookat = []
                for j in range(3):
                    if board.small_boards_status[m][j][i] == self.player_char[self.bot_player]:
                        win_chance[1] = 0
                        bot_win_cells+=1
                    if board.small_boards_status[m][j][i] == self.player_char[self.bot_player^1]:
                        win_chance[0] = 0
                        opp_win_cells+=1
                    if board.small_boards_status[m][j][i] == 'd':
                        win_chance[0] = 0
                        win_chance[1] = 0
                    if board.small_boards_status[m][j][i] == '-':
                        prob_chance[0] =  self.check_prob_win_big(board,m,j,i,self.bot_player)
                        prob_chance[1] =  self.check_prob_win_big(board,m,j,i,self.bot_player^1)
                        if prob_chance[0] == 1 and prob_chance[1] == 1:
                            lookat.append([m,j,i])
                        if prob_chance[0] == 0:
                            win_chance[0] = 0
                        if prob_chance[1] == 0:
                            win_chance[1] = 0
                if win_chance[0] == 1:
                    winning_comb[0][bot_win_cells] +=1
                if win_chance[1] == 1:
                    winning_comb[1][opp_win_cells] +=1
                if win_chance[0]==1 or win_chance[1] ==1:
                    for z in range(len(lookat)):
                        utility+=self.smallboardutility(board,lookat[z])

        #winning_comb.append(np.zeros(4)) #0 for bot
        #winning_comb.append(np.zeros(4)) #1 for opposition
            bot_win_cells = 0
            opp_win_cells = 0
            win_chance = np.ones(2)
            prob_chance = np.zeros(2)
        #for m in range(2):
            bot_win_cells = 0
            opp_win_cells = 0
            win_chance = np.ones(2)
            prob_chance = np.zeros(2)
            for i in range(3):
                #for j in range(3):
                if board.small_boards_status[m][i][i] == self.player_char[self.bot_player]:
                    win_chance[1] = 0
                    bot_win_cells+=1
                if board.small_boards_status[m][i][i] == self.player_char[self.bot_player^1]:
                    win_chance[0] = 0
                    opp_win_cells+=1
                if board.small_boards_status[m][i][i] == 'd':
                    win_chance[0] = 0
                    win_chance[1] = 0
                if board.small_boards_status[m][i][i] == '-':
                    prob_chance[0] =  self.check_prob_win_big(board,m,i,i,self.bot_player)
                    prob_chance[1] =  self.check_prob_win_big(board,m,i,i,self.bot_player^1)
                    if prob_chance[0] == 1 and prob_chance[1] == 1:
                        lookat.append([m,i,i])
                    if prob_chance[0] == 0:
                        win_chance[0] = 0
                    if prob_chance[1] == 0:
                        win_chance[1] = 0
            if win_chance[0] == 1:
                winning_comb[0][bot_win_cells] +=1
            if win_chance[1] == 1:
                winning_comb[1][opp_win_cells] +=1
            if win_chance[0]==1 or win_chance[1] ==1:
                for z in range(len(lookat)):
                    utility+=self.smallboardutility(board,lookat[z])

        #winning_comb.append(np.zeros(4)) #0 for bot
        #winning_comb.append(np.zeros(4)) #1 for opposition
            bot_win_cells = 0
            opp_win_cells = 0
            win_chance = np.ones(2)
            prob_chance = np.zeros(2)
        #for m in range(2):
            bot_win_cells = 0
            opp_win_cells = 0
            win_chance = np.ones(2)
            prob_chance = np.zeros(2)
            lookat = []
            for i in range(3):
                #for j in range(3):
                if board.small_boards_status[m][i][2-i] == self.player_char[self.bot_player]:
                    win_chance[1] = 0
                    bot_win_cells+=1
                if board.small_boards_status[m][i][2-i] == self.player_char[self.bot_player^1]:
                    win_chance[0] = 0
                    opp_win_cells+=1
                if board.small_boards_status[m][i][2-i] == 'd':
                    win_chance[0] = 0
                    win_chance[1] = 0
                if board.small_boards_status[m][i][2-i] == '-':
                    prob_chance[0] =  self.check_prob_win_big(board,m,i,2-i,self.bot_player)
                    prob_chance[1] =  self.check_prob_win_big(board,m,i,2-i,self.bot_player^1)
                    if prob_chance[0] == 1 and prob_chance[1] == 1:
                        lookat.append([m,i,2-i])
                    if prob_chance[0] == 0:
                        win_chance[0] = 0
                    if prob_chance[1] == 0:
                        win_chance[1] = 0
            if win_chance[0] == 1:
                winning_comb[0][bot_win_cells] +=1
            if win_chance[1] == 1:
                winning_comb[1][opp_win_cells] +=1
            if win_chance[0]==1 or win_chance[1] ==1:
                for z in range(len(lookat)):
                    utility+=self.smallboardutility(board,lookat[z])
        utility += 17* (winning_comb[0][1] -winning_comb[1][1]) + 134* (winning_comb[0][2] - winning_comb[1][2])
        if winning_comb[0][3] == 1:
            utility = self.inf
        if winning_comb[1][3] == 1: 
            utility = -self.inf
        return(utility)

    
        
    def prunealphabeta(self,board,depth,player,player_move,alphaplayer,betaplayer,prev):
        """
        minimax+alphabeta
        """
        if board.find_terminal_state() == (self.player_char[self.bot_player],'WON'):
            return self.inf
        if board.find_terminal_state() == (self.player_char[self.bot_player^1],'WON'):
            return -self.inf
        if board.find_terminal_state() == ('NONE','DRAW'):
            return self.blockutilityondraw(board)
        if  depth == 0:
            return self.utility(board,self.player_char[prev])
        if time() - self.start > self.limit:
            return self.utility(board,self.player_char[prev])
        moves_available = board.find_valid_move_cells(player_move)
        
        tempbonusmove = self.bonus_move_cur[player]
        if player == self.bot_player :
            cur_utility = -self.inf
        else:
            cur_utility = self.inf
        #random.shuffle(moves_available)
        arr2 = []
        for moves in moves_available:
            sort_temp_board = deepcopy(board)
            sort_temp_board.update(player_move,moves,self.player_char[self.bot_player])
            arr2.append((self.utility(sort_temp_board,self.player_char[self.bot_player]),moves)) 
        self.nextmoves = sorted(arr2,key= lambda x:x[0])
        self.nextmoves.reverse()
        myarr = [x[1] for x in self.nextmoves]
        for moves in myarr:
            self.bonus_move_cur[player] = tempbonusmove
            tempboard = deepcopy(board)
            gamepos,status = tempboard.update(player_move,moves,self.player_char[player])
            if not status: #and self.bonus_move_cur[player] == 0:
                self.bonus_move_cur[player] = 0
            elif status:
                self.bonus_move_cur[player] ^= 1
            
            if player == self.bot_player: #bot playing
                if status and self.bonus_move_cur[player] == 1: #bot has bonus 
                    max_minmax = self.prunealphabeta(tempboard,depth-1,
                                        player,moves,alphaplayer,betaplayer,player)
                    cur_utility = max(cur_utility,max_minmax)
                    self.bonus_move_cur[player] = 0
                else:
                    max_minmax = self.prunealphabeta(tempboard,depth-1,
                                        player^1,moves,alphaplayer,betaplayer,player)
                    cur_utility = max(cur_utility,max_minmax)
                alphaplayer = max(alphaplayer,cur_utility)  #recursive minmax
            else:
                if status and self.bonus_move_cur[player] == 1: #opp has bonus
                    min_minmax = self.prunealphabeta(tempboard,depth-1,
                                        player,moves,alphaplayer,betaplayer,player)
                    cur_utility = min(cur_utility,min_minmax)
                    self.bonus_move_cur[player] = 0        
                else:
                    min_minmax = self.prunealphabeta(tempboard,depth-1,
                                        player^1,moves,alphaplayer,betaplayer,player)
                    cur_utility = min(cur_utility,min_minmax)
                betaplayer = min(betaplayer,cur_utility)   #recursive minmax

            
            if(betaplayer <= alphaplayer):
                break
            if time() - self.start > self.limit:
                break
        
        self.bonus_move_cur[player] = tempbonusmove
        return cur_utility



    def alphabetamove(self,board,old_move,player,depth):
        """
        Preprocessing for alphaplayer betaplayer algorithm
        """

        #find all possible moves
        arr = board.find_valid_move_cells(old_move)
         #tells if player has bonus move 
        tempbonusmove = self.bonus_move_cur[player]
        #initialise maximum value
        curmax = -self.inf-1
        arr2 = []
        for moves in arr:
            sort_temp_board = deepcopy(board)
            sort_temp_board.update(old_move,moves,self.player_char[player])
            arr2.append((self.utility(sort_temp_board,self.player_char[player]),moves))
        
        self.nextmoves = sorted(arr2,key= lambda x:x[0])
        self.nextmoves.reverse()
        myarr = [x[1] for x in self.nextmoves]
        for moves in myarr:
            
            self.bonus_move_cur[player] = tempbonusmove

            #checks if any cell won
            tempboard = deepcopy(board)
            gamepos,status = tempboard.update(old_move,moves,self.player_char[player])
            if not status:
                self.bonus_move_cur[player] = 0
            elif status:
                self.bonus_move_cur[player] ^= 1
            
            #check utility after winning 
            if status and (self.bonus_move_cur[player] == 1):
                player_utility = self.prunealphabeta(tempboard,depth,player,moves,-self.inf,self.inf,player)#same player moves
            else:
                player_utility = self.prunealphabeta(tempboard,depth,player^1,moves,-self.inf,self.inf,player)#opponent moves
            
            #restore the board states
            #board.big_boards_status[moves[0]][moves[1]][moves[2]] = "-"
            #board.small_boards_status[moves[0]][moves[1]/3][moves[2]/3] = "-"
            
            if player_utility > curmax:
                cur_best_move = moves
                curmax = player_utility
        
        self.bonus_move_cur[player] = tempbonusmove
        
        return cur_best_move



    def idfs(self,board,oldmv,tree_level,player):
        """
        idfs returns best move
        """

        #if(time()-self.start)>self.limit:
        #    break
        output = self.alphabetamove(board,oldmv,player,self.startdepth)
		
        return output
   


    def move(self,gameboard,oldmove,symbol):
        """
        Main code
        """
    
        #start timer
        self.start=time()
        self.movecounter+=1
        if(self.movecounter > 17 ):
            self.startdepth+=1
            self.movecounter = 0
        #initialising players
        if symbol=='x':
            self.bot_player=1
            self.player=1
            self.opponent=0
        else:
            self.bot_player=0
            self.player=0
            self.opponent=1

        try:
            #if first move
            if oldmove == (-1,-1,-1):
                return self.default
        
            #calculate from hash tables
            depth=1

            tempboard=deepcopy(gameboard)
            self.bonus_move_cur=[0,0]
            if(self.last_function_call):
                self.bonus_move_cur[self.bot_player]^=1
            else:
                self.bonus_move_cur[self.bot_player]=0

            tempmove=self.idfs(tempboard,oldmove,depth,self.player)
            last_check_board = deepcopy(tempboard)
            gamepos,status=last_check_board.update(oldmove,tempmove,self.player_char[self.player])

            if not status:
                self.last_function_call = 0
            elif status:
                self.last_function_call ^=1

            #restore the board states
            #tempboard.big_boards_status[tempmove[0]][tempmove[1]][tempmove[2]] = "-"
            #tempboard.small_boards_status[tempmove[0]][tempmove[1]/3][tempmove[2]/3] = "-"
            #print time()-self.start

    	    cells = gameboard.find_valid_move_cells(oldmove)
            if tempmove not in cells:
        		return cells[random.randrange(len(cells))]
            return tempmove

        except Exception as e:
            print 'Exception occurred ', e
            print 'Traceback printing ', sys.exc_info()
            print traceback.format_exc()