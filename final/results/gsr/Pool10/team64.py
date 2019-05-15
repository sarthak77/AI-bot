import sys
import random
import signal
import time
import copy
import traceback
from copy import deepcopy

class Team64:
    def __init__(self):
        patterns = []
        for i in range(8):
            patterns.append([])

        # row wise and #column wise
        for i in range(3):
            for j in range(3):
                patterns[i].append((i, j))  # row wise
                patterns[3+i].append((j, i))
        self.start = 0

        # diagonal wise
        patterns[6] = [(0, 0), (1, 1), (2, 2)]
        patterns[7] = [(0, 2), (1, 1), (2, 0)]
        self.patterns = patterns
        self.small_board_scores=  ([[0 for i in range(3)] for j in range(3)], [[0 for i in range(3)] for j in range(3)])
        self.big_boards_scores=  [0,0]
        self.cell_weight = [(3, 2, 3), (2, 4, 2), (3, 2, 3)]
       
    def move(self, board, old_move, flag):
        #print "me"
        self.start =  time.time()
        if old_move == (-1, -1, -1):
            return (1, 4, 4)

        validCells = board.find_valid_move_cells(old_move) 
        minDepth = 2
        best_move = validCells[0]         
       
        try:
            # while True:
            board1 = deepcopy(board)
            alpha = float("-inf")
            beta = float("inf")
            best_move, val = self.minimax(board1, True, minDepth, flag, validCells, alpha, beta)
                # if val==-1:
                #     break
                # if time.time()-self.start >= 14:
                #     break
                # print minDepth
                # minDepth+=1
        except Exception as e:
            print e
            pass
        print best_move
        return best_move

    def minimax(self, board, maxim, d, flag, validCells, alpha, beta):
        if(time.time()-self.start >= 14):
            return validCells[0],-1
        #checkGoal = board.find_terminal_state()

		
        opp = 'x'
        if flag == 'x':
            opp = 'o'
        if maxim == True:
            retVal = float("-inf")
            retMove = validCells[0]
            for move in validCells:
                
                ans=self.update(board,move,flag) 
                who,what=board.find_terminal_state()
                if what=='DRAW':
                    val=0
                elif what=='WON' and who==flag:
                    val=float("inf")
                elif what=='WON' and who!=flag:
                    val=float("-inf")
                else:
                    if ans:
                        opp1=flag
                        m2=maxim
                        val=500
                    else:
                        opp1=opp
                        m2=~maxim
                        val=0
                    children=board.find_valid_move_cells(move)
                    if children==[] or d==0:
                        val+=self.heuristic(board,flag)-self.heuristic(board,opp)
                        
                        #print "move =", move,val1,val2
                    else:
                        mov, val1 = self.minimax(board, m2, d-1,
                                        opp1,children , alpha, beta)
                        val+=val1                
                self.deupdate(board,move,flag)

                if(time.time()-self.start >= 14):
                    return move,-1  
                if val == -1:
                    return move,-1
                if val > retVal:
                    retVal = val
                    retMove = move
                alpha = max(alpha, retVal)
                if beta <= alpha:
                    break
            return retMove, retVal
        else:
            retVal=float("inf")
            retMove=validCells[0]
            for move in validCells:
                ans=self.update(board,move,flag) 

                who,what=board.find_terminal_state()
                if what=='DRAW':
                    val=0
                elif what=='WON' and who!=flag: #here flag is our opp
                    val=float("inf")
                elif what=='WON' and who==flag:
                    val=float("-inf")
                else:
                    if ans:
                        opp1=flag
                        m2=maxim
                        val=-500
                    else:
                        opp1=opp
                        m2=~maxim
                        val=0
                    children=board.find_valid_move_cells(move)
                    if children==[] or d==0:
                        val+=self.heuristic(board,opp)-self.heuristic(board,flag)
                    else:
                        mov, val1 = self.minimax(board, m2, d-1,
                                        opp1,children , alpha, beta)
                        val+=val1
                
                self.deupdate(board,move,flag)

                if(time.time()-self.start >= 14):
                    return move,-1
                if val == -1:
                    return move,-1
                if val < retVal:
                    retVal = val
                    retMove = move
                beta = min(beta, retVal)
                if beta <= alpha:
                    break
           
            return retMove, retVal


    def small_board_score(self,board, flag,box):
        score = 0
        x = 5

        for pattern in self.patterns:
            opp = 0
            me = 0
            empty = 0
            for i in range(3):
                c = board.big_boards_status[box[0]][3*box[1] + pattern[i][0]][3*box[2] +pattern[i][1]]
                if c == flag:
                    me += 1
                elif c == '-':
                    empty += 1
                else:
                    opp += 1
            if me == 3:
                score += 200*x
            elif me == 2:
                if empty == 1:
                    score +=49*x
                elif opp == 1:
                    score -=40*x
            elif me == 1:
                if empty == 2:
                    score += 15*x
                elif opp==2:
                    score -=33*x
                elif opp==1:
                    score -=20*x
            else:
                if opp==3:
                    score-=200*x
                elif opp==2:
                    score-=29.5*x
                elif opp==1:
                    score-=15*x
                elif opp==0:
                    score += 0

        for i in range(3):
            for j in range(3):
                req = board.big_boards_status[box[0]][3*box[1]+i][3*box[2]+j]
                if req == flag:
                    score += self.cell_weight[i][j] 
                
        
        return score

    def big_boards_score(self,board,flag,box):
        score = 0
        x = 5

        for pattern in self.patterns:
            me = 0
            opp = 0
            empty = 0
            for i in range(3):
                c = board.small_boards_status[box[0]][pattern[i][0]][pattern[i][1]]
                if c == flag:
                    me += 1
                elif c == '-':
                    empty += 1
                else:
                    opp += 1
            if me == 3:
                score += 200*x
            elif me == 2:
                if empty == 1:
                    score +=49*x
                elif opp == 1:
                    score -=40*x
            elif me == 1:
                if empty == 2:
                    score += 15*x
                elif opp==2:
                    score -=33*x
                elif opp==1:
                    score -=20*x
            else:
                if opp==3:
                    score-=200*x
                elif opp==2:
                    score-=29.5*x
                elif opp==1:
                    score-=15*x
                elif opp==0:
                    score += 0

                

        return score


    
    def heuristic(self, board, flag):
        #given this state => what is the probabilty of winning from this state
        for k in range(2):
            for i in range(3):
                for j in range(3):
                    self.small_board_scores[k][i][j] =  self.small_board_score(board, flag,[k,i,j]) #bloc
        for k in range(2):
            self.big_boards_scores[k] = self.big_boards_score(board, flag,[k])
        
        total = 0
        total1 = 0
        scale = 1

        for k in range(2):
            for i in range(3):
                for j in range(3):
                    total +=0.05*self.cell_weight[i][j] *self.small_board_scores[k][i][j]
        
        for k in range(2):
            total1 += self.big_boards_scores[k]

        x =  total + (scale)*total1
        #print total,"bigscore",total1
        
        return x


    def update(self,board,move,flag):
        board.big_boards_status[move[0]][move[1]][move[2]] = flag

        x = move[1]/3
        y = move[2]/3
        k = move[0]

        # checking if a small_board has been won or drawn or not after the current move
        bs = board.big_boards_status[k]
        for i in range(3):
            # checking for horizontal pattern(i'th row)
            if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == flag):
                board.small_boards_status[k][x][y] = flag
                return True
            # checking for vertical pattern(i'th column)
            if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == flag):
                board.small_boards_status[k][x][y] = flag
                return  True
        # checking for diagonal patterns
        # diagonal 1
        if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == flag):
            board.small_boards_status[k][x][y] = flag
            return True
        # diagonal 2
        if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == flag):
            board.small_boards_status[k][x][y] = flag
            return True
        # checking if a small_board has any more cells left or has it been drawn
        for i in range(3):
            for j in range(3):
                if bs[3*x+i][3*y+j] == '-':
                    return False
        board.small_boards_status[k][x][y] = 'd'
        return False
    
    def deupdate(self,board,move,flag):
        board.big_boards_status[move[0]][move[1]][move[2]] = '-'
        x = move[1]/3
        y = move[2]/3
        k = move[0]
        board.small_boards_status[k][x][y]='-'
        
       