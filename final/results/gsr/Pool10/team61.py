import numpy as np
from copy import deepcopy
import time
import random


#Tasks left to do:1.Complete the bonus move part i.e it should be available only for 2 consecutive times.Consider making alpha and beta inf and neg inf after best move
#2.Fix and finish off the heuristic values


class Team61:
    def __init__(self):
       	self.pos_utilities = np.array([[300,200,300],[200,400,200],[300,200,300]]) # utilities of winning position[i][j]
        self.pattern_heuristic1 = {}
        self.pattern_heuristic2 = {}
        self.hash_board_table = [[[long(0) for k in range(2)] for j in range(18)] for i in range(9)]
        self.hash_block = [[[long(0) for k in range(3)] for j in range(3)] for i in range(2)]
        self.hash_block_table = [[[long(0) for k in range(2)] for j in range(6)] for i in range(3)]
        self.level = np.zeros(15, dtype = 'int')
        self.symbol = 'x'
        self.opp_symbol = 'o'
        self.blank = '-'
        self.timeout_time = 20
        self.levels = np.zeros(6,dtype='int')
        self.init_flag=0
        self.hash_of_board={}
        self.hash_of_block1={}
        self.hash_of_block2={}
        self.start=0

        self.win=0
        pat = []
        for i in xrange(3):
            row_array = [] # i'th row
            col_array = [] # i'th column
            for j in xrange(3):
                row_array.append((i,j))
                col_array.append((j,i))
            pat.append(tuple(row_array))
            pat.append(tuple(col_array))
        pat.append(tuple([(0,0),(1,1),(2,2)]))
        pat.append(tuple([(2,0),(1,1),(0,2)]))
        self.pat=pat
        
        self.dep=4
        self.hash = long(0)
        self.fill_pattern_heuristic()
        self.zobrist_hash_initial_table()

    def hash_value(self,val):
        if val==self.symbol: return 4
        elif val == self.opp_symbol: return 1
        else: return 0

    def fill_pattern_heuristic(self):
        symbol_val = self.hash_value(self.symbol)
        oppsymb_val = self.hash_value(self.opp_symbol)
        blank_val = self.hash_value(self.blank)
        self.pattern_heuristic1[symbol_val+symbol_val+symbol_val] = 300
        self.pattern_heuristic1[blank_val+blank_val+blank_val] = 0
        self.pattern_heuristic1[symbol_val+symbol_val+oppsymb_val] = 0
        self.pattern_heuristic1[symbol_val+symbol_val+blank_val] = 106#################
        self.pattern_heuristic1[symbol_val+blank_val+blank_val] = 43####################
        self.pattern_heuristic1[symbol_val+oppsymb_val+blank_val] = 0
        self.pattern_heuristic1[oppsymb_val+oppsymb_val+oppsymb_val] = 00
        self.pattern_heuristic1[oppsymb_val+oppsymb_val+blank_val] = 0###########
        self.pattern_heuristic1[oppsymb_val+blank_val+blank_val] = 0
        self.pattern_heuristic1[oppsymb_val+oppsymb_val+symbol_val] = 50###################
        #####################



    def compute_smallboard_heuristic(self,board,in0,in1,in2,sym,op):
        if sym==self.symbol:
            if self.hash_block[in0][in1][in2] in self.hash_of_block1:
                return self.hash_of_block1[self.hash_block[in0][in1][in2]]
        else:
             if self.hash_block[in0][in1][in2] in self.hash_of_block2:
                return self.hash_of_block2[self.hash_block[in0][in1][in2]]


        board_copy = deepcopy(board)
        board_copy[board_copy==sym] = 4
        board_copy[board_copy==op] = 1
        board_copy[board_copy==self.blank] = 0
        board_copy=np.array(board_copy).astype(np.int64)
        cols = board_copy.sum(axis=0)
        rows = board_copy.sum(axis=1)
        sum1=0
        sum1 = self.pattern_heuristic1[rows[0]]
        sum1 = max(sum1,self.pattern_heuristic1[rows[1]])
        sum1 = max(sum1,self.pattern_heuristic1[rows[2]])
        sum1 = max(sum1,self.pattern_heuristic1[cols[0]])
        sum1 = max(sum1,self.pattern_heuristic1[cols[1]])
        sum1 = max(sum1,self.pattern_heuristic1[cols[2]])
        sum1 = max(sum1,self.pattern_heuristic1[board_copy[0][0]+board_copy[1][1]+board_copy[2][2]])
        sum1 = max(sum1,self.pattern_heuristic1[board_copy[0][2]+board_copy[1][1]+board_copy[2][0]])
        # sum1 = self.pattern_heuristic1[rows[0]]-self.pattern_heuristic2[rows[0]]
        # sum1 = max(sum1,self.pattern_heuristic1[rows[1]]-self.pattern_heuristic2[rows[1]])
        # sum1 = max(sum1,self.pattern_heuristic1[rows[2]]-self.pattern_heuristic2[rows[2]])
        # sum1 = max(sum1,self.pattern_heuristic1[cols[0]]-self.pattern_heuristic2[cols[0]])
        # sum1 = max(sum1,self.pattern_heuristic1[cols[1]]-self.pattern_heuristic2[cols[1]])
        # sum1 = max(sum1,self.pattern_heuristic1[cols[2]]-self.pattern_heuristic2[cols[2]])
        # sum1 = max(sum1,self.pattern_heuristic1[board_copy[0][0]+board_copy[1][1]+board_copy[2][2]]-self.pattern_heuristic2[board_copy[0][0]+board_copy[1][1]+board_copy[2][2]])
        # sum1 = max(sum1,self.pattern_heuristic1[board_copy[0][2]+board_copy[1][1]+board_copy[2][0]]-self.pattern_heuristic2[board_copy[0][2]+board_copy[1][1]+board_copy[2][0]])

        
        if sym==self.symbol:
            self.hash_of_block1[self.hash_block[in0][in1][in2]] =sum1
        else:
            self.hash_of_block2[self.hash_block[in0][in1][in2]] =sum1
        return sum1

    # incomplete.Need to see how to consider patterns also
    def compute_largeboard_heuristic(self,board,sym,op):#check patterns
        sum1=0
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j]==sym:
                    sum1+=0.0002*board[i][j]*self.pos_utilities[i][j]###########################

       
        for i in self.pat:
            yo=0
            cnt=0
            cnt1=0
            cnt2=0
            cnt3=0
            for j in xrange(3):
                if board[i[j]]<0:
                    cnt1+=1
                    yo=0
                    break
                elif board[i[j]]==300:
                    cnt+=1
                    yo+=300
                else:
                    yo+=board[i[j]]
            if cnt==2 and cnt1==1:
                sum1+=yo*0##########################
            elif cnt==2 and cnt1==0:
                sum1+=yo*1
            elif cnt==1 and cnt1==2:
                sum1+=yo*0.5
            elif cnt==1 and cnt1==1:
                sum1+=yo*0#################
            elif cnt==1 and cnt1==0:
                sum1+=yo*0.4#################

            elif cnt==0:
                sum1+=yo
                
            elif cnt==3:
                sum1+=5000
            # yo=0
            # for j in range(2):
            #     yo+=board[i[j]]

        # print sum1
        return sum1


    def compute_heuristic(self, board,sym,op):
        heurs = 0
        small_board_status = []
        small_board_status.append(deepcopy((board.small_boards_status[0])))
        small_board_status.append(deepcopy((board.small_boards_status[1])))
        big_board_status = []
        big_board_status.append(np.array(board.big_boards_status[0]))
        big_board_status.append(np.array(board.big_boards_status[1]))
        for k in range(0,2):
            for i in range(0,3):
                for j in range(0,3):
                    if small_board_status[k][i][j] == '-':
                        small_board_status[k][i][j]= self.compute_smallboard_heuristic(np.array(big_board_status[k][3*i:3*i+3,3*j:3*j+3]),k,i,j,sym,op)
                    elif small_board_status[k][i][j] == sym:
                        small_board_status[k][i][j]=300
                    elif small_board_status[k][i][j] == op:
                        small_board_status[k][i][j]=-1########    
                    else:
                        small_board_status[k][i][j]=-1#########


        heurs = self.compute_largeboard_heuristic(np.array(small_board_status[0]),sym,op)
        heurs = max(heurs,self.compute_largeboard_heuristic(np.array(small_board_status[1]),sym,op))
        return heurs

    #k=0 for me, k=1 for opposition
    def zobrist_hash_initial_table(self):
        for i in range(0,9):
            for j in range(0,18):
                for k in range(0,2):
                    self.hash_board_table[i][j][k] = long(random.randint(0,2**128-1))
        for i in range(0,3):
            for j in range(0,6):
                for k in range(0,2):
                    self.hash_block_table[i][j][k] = long(random.randint(0,2**128-1))

    def minimax(self,board, depth, maxi, mini, old_move, alpha, beta):
        #1 if maxi node,0 if mini for maxi node
        terminal = board.find_terminal_state()
        self.level[depth] +=1
        #need to change to infinity and neg infinity
        if terminal[0] == self.symbol and terminal[1] == 'WON':
            return 10000000, old_move
        elif terminal[0] == self.opp_symbol and terminal[1] == 'WON':
            return -10000000, old_move##################################### 0 or -10000000
        elif terminal[1] == 'DRAW':
            return 0 ,old_move
        
        if depth == 0:
            if self.hash in self.hash_of_board:
                return self.hash_of_board[self.hash],old_move

            heuristic = self.compute_heuristic(board,self.symbol,self.opp_symbol)-self.compute_heuristic(board,self.opp_symbol,self.symbol)
            self.hash_of_board[self.hash]=heuristic 
            return heuristic, old_move

        valid_cells = board.find_valid_move_cells(old_move)
        if maxi == 1:
            best_value = float("-inf")
            for i in range(0,len(valid_cells)):
                # tt=time.time()
                # if tt-self.start>18:
                #     break
                new_move = valid_cells[i]
                new_state_details = board.update(old_move, new_move,self.symbol)
                self.hash ^= self.hash_board_table[new_move[1]][9*new_move[0]+new_move[2]][0]
                self.hash_block[new_move[0]][new_move[1]/3][new_move[2]/3]^=self.hash_block_table[new_move[1]%3][new_move[2]%3][0]


                if new_state_details[1] and self.win==0:
                    utility, dummy = self.minimax(board, depth-1, 1, 0, new_move,alpha,beta)
                    self.win+=1
                else:
                    self.win=0
                    utility, dummy = self.minimax(board, depth-1, 0, 1, new_move,alpha,beta)

                board.big_boards_status[new_move[0]][new_move[1]][new_move[2]] ='-'
                board.small_boards_status[new_move[0]][new_move[1]/3][new_move[2]/3]='-'

                self.hash ^= self.hash_board_table[new_move[1]][9*new_move[0]+new_move[2]][0]

                self.hash_block[new_move[0]][new_move[1]/3][new_move[2]/3]^=self.hash_block_table[new_move[1]%3][new_move[2]%3][0]

                if utility > best_value:
                    best_value = utility
                    best_move = new_move

                alpha = max(alpha, best_value)
                if beta<= alpha: break

            return best_value, best_move

        elif mini == 1:
            best_value = float("inf")
            for i in range(0,len(valid_cells)):
                # tt=time.time()
                # if tt-self.start>18:
                #     break
                new_move = valid_cells[i]
                new_state_details = board.update(old_move, new_move,self.opp_symbol)

                self.hash ^= self.hash_board_table[new_move[1]][9*new_move[0]+new_move[2]][1]
                # self.hash_block[new_move[0]][new_move[1]/3][new_move[2]/3]^=self.hash_board_table[new_move[1]][9*new_move[0]+new_move[2]][1]
                self.hash_block[new_move[0]][new_move[1]/3][new_move[2]/3]^=self.hash_block_table[new_move[1]%3][new_move[2]%3][1]

                if new_state_details[1] and self.win==0:
                    self.win+=1
                    utility, dummy = self.minimax(board, depth-1, 0, 1, new_move,alpha,beta)
                else:
                    self.win=0
                    utility, dummy = self.minimax(board, depth-1, 1, 0, new_move,alpha,beta)

                board.big_boards_status[new_move[0]][new_move[1]][new_move[2]] ='-'
                board.small_boards_status[new_move[0]][new_move[1]/3][new_move[2]/3]='-'

                self.hash ^= self.hash_board_table[new_move[1]][9*new_move[0]+new_move[2]][1]
                # self.hash_block[new_move[0]][new_move[1]/3][new_move[2]/3]^=self.hash_board_table[new_move[1]][9*new_move[0]+new_move[2]][1]
                self.hash_block[new_move[0]][new_move[1]/3][new_move[2]/3]^=self.hash_block_table[new_move[1]%3][new_move[2]%3][1]

                if utility < best_value:
                    best_value = utility
                    best_move = new_move

                beta = min(beta, best_value)
                if beta<=alpha: break

            return best_value, best_move

    def move(self,board, old_move, flag):
        # self.count+=1
        #setting the symbols the very first time
        self.start=time.time()
        if self.init_flag==0:
            self.init_flag = 1
            self.symbol = flag
            if flag == 'x': self.opp_symbol = 'o'
            else: self.opp_symbol = 'x'
        if self.symbol == board.big_boards_status[old_move[0]][old_move[1]][old_move[2]]:
            self.win=1
            # print "yoyo",old_move
        # if old_move == (-1,-1,-1):
        #     self.hash ^= self.hash_board_table[4][4][0]
        #     self.hash_block[0][1][1]^=self.hash_block_table[1][1][0]

        #     return (0,4,4)

        if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == self.opp_symbol: #is this if condition even necessary????
            self.hash ^= self.hash_board_table[old_move[1]][9*old_move[0]+old_move[2]][1]
            self.hash_block[old_move[0]][old_move[1]/3][old_move[2]/3]^=self.hash_block_table[old_move[1]%3][old_move[2]%3][1]
        start_time = time.time()
        val, move = self.minimax(board,self.dep,1,0,old_move,float("-inf"),float("inf"))
        self.hash ^= self.hash_board_table[move[1]][9*move[0]+move[2]][0]
        self.hash_block[move[0]][move[1]/3][move[2]/3]^=self.hash_block_table[move[1]%3][move[2]%3][0]
        # print self.level, time.time() - start_time
        self.level[:] = 0
        return move
