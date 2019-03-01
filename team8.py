"""
Class for AI bot
"""
import random
import traceback
import sys
import numpy as np
from time import time
from copy import deepcopy

class Player8:
    """ 
    AI implemented 
    """
    
    def __init__(self):
        """
        Initialize variables
        """
        self.default=(0,4,4)#default move
        self.limit=6#time limit
        self.start=0#start time
        # self.maxdepth=3
        self.maxdepth=9*9*9
        self.player=0#x=1 o=0
        self.opponent=0
        self.bestmv=(0,0,0)
        self.inf = 10000000000
        self.max_player = 1
        self.map_symbol = ['o', 'x']
        self.zob_store = []
        self.hash_store = [[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
        self.bonus_move_cur = [0 , 0]
        self.last_blk_won = 0
        self.numsteps = 0
        self.dict = {}
        self.blockweight=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        # self.blockweight=[1,.9,1,.9,1.1,.9,1,.9,1,1,.9,1,.9,1.1,.9,1,.9,1]
        for i in range(36):
            self.zob_store.append(2**i)



    def smallboardutility(self,board,symbol):
        """
        Find weights of each cell
        """

        for b in range(2):

            #check r1 r2 r3
            for i in range(3):
                row=[]
                row.append(board.small_boards_status[b][i][0])
                row.append(board.small_boards_status[b][i][1])
                row.append(board.small_boards_status[b][i][2])
                
                temp=self.calculatewincombsb(row,symbol)
                
                self.blockweight[b*9+i*3]+=temp
                self.blockweight[b*9+i*3+1]+=temp
                self.blockweight[b*9+i*3+2]+=temp

            #check c1 c2 c3
            for i in range(3):
                col=[]
                col.append(board.small_boards_status[b][0][i])
                col.append(board.small_boards_status[b][1][i])
                col.append(board.small_boards_status[b][2][i])

                temp=self.calculatewincombsb(col,symbol)

                self.blockweight[b*9+i]+=temp
                self.blockweight[b*9+i+3]+=temp
                self.blockweight[b*9+i+6]+=temp


            #check dig1
            dig=[]
            dig.append(board.small_boards_status[b][0][0])
            dig.append(board.small_boards_status[b][1][1])
            dig.append(board.small_boards_status[b][2][2])
            
            temp=self.calculatewincombsb(dig,symbol)

            self.blockweight[b*9]+=temp
            self.blockweight[b*9+4]+=temp
            self.blockweight[b*9+8]+=temp

            #check dig2
            dig=[]
            dig.append(board.small_boards_status[b][0][2])
            dig.append(board.small_boards_status[b][1][1])
            dig.append(board.small_boards_status[b][2][0])

            temp=self.calculatewincombsb(dig,symbol)
            
            self.blockweight[b*9+2]+=temp
            self.blockweight[b*9+4]+=temp
            self.blockweight[b*9+6]+=temp



    def calculatewincombsb(self,v,symbol):
        """
        Calculate weight from each row,column,dig
        """

        weight=0

        if symbol=='x':
            opp='o'
        else:
            opp='x'

        #checking edge case
        if v.count(symbol)==2 and v.count('-')==1:
            weight=100
        elif v.count(symbol)==3:
            weight=1000
        elif v.count(opp)==2 and v.count('-')==1:
            weight=-110
        elif v.count(opp)==3:
            weight=-1010

        #checking normal cases
        if 'd' in v:
            weight=-0.5
        elif ((symbol in v) and (opp in v)):
            weight=-0.5 
        elif (symbol in v) and (opp not in v):
            weight+=5
        elif (opp in v) and (symbol not in v):
            weight+=-5
        elif ('-' in v) and (symbol not in v) and (opp not in v):
            weight+=0   
           
        return weight



    def calculatewincomb(self,v,symbol,blkno):
        """
        Calculate status of each row,column,dig
        """

        blkwt=self.blockweight[blkno]
        utility=200

        if symbol=='x':
            opp='o'
        else:
            opp='x'

        #checking edge cases
        if v.count(symbol)==2 and v.count('-')==1:
            utility+=10
            if blkwt<0:
                blkwt+=-blkwt+10000
            else:
                blkwt+=10000

        elif v.count(symbol)==3:
            utility+=100
            if blkwt<0:
                blkwt+=-blkwt+100000
            else:
                blkwt+=100000

        elif v.count(opp)==2 and v.count('-')==1:
            utility-=10
            if blkwt<0:
                blkwt+=-10100
            else:
                blkwt+=-blkwt-10100

        elif v.count(opp)==3:
            utility-=100
            if blkwt<0:
                blkwt+=-110000
            else:
                blkwt+=-blkwt-110000

       #checking normal cases
        if (symbol in v) and (opp not in v):
            utility+=1
            blkwt+=.5
        elif (opp in v) and (symbol not in v):
            utility+=-1.1
            blkwt-=.5
        elif ('-' in v) and (symbol not in v) and (opp not in v):
            utility+=.5
        elif (symbol in v) and (opp in v):
            utility+=0
            blkwt-=.3 
           

        self.blockweight[blkno]=blkwt
        return utility



    def blockutility(self,board,b,r,c,symbol):
        """
        Calculate utility of each cell of big board
        """

        #r1 r2 r3 c1 c2 c3 d1 d2
        utilityvector=[]
        blkno=9*b+(3*r+c)/3
      
        #check r1 r2 r3
        for i in range(3):
            row=[]
            row.append(board.big_boards_status[b][r+i][c])
            row.append(board.big_boards_status[b][r+i][c+1])
            row.append(board.big_boards_status[b][r+i][c+2])

            temp=self.calculatewincomb(row,symbol,blkno)
            utilityvector.append(temp)
            

        #check c1 c2 c3
        for i in range(3):
            col=[]
            col.append(board.big_boards_status[b][r][c+i])
            col.append(board.big_boards_status[b][r+1][c+i])
            col.append(board.big_boards_status[b][r+2][c+i])

            temp=self.calculatewincomb(col,symbol,blkno)
            utilityvector.append(temp)
            


        #check dig1
        dig=[]
        dig.append(board.big_boards_status[b][r][c])
        dig.append(board.big_boards_status[b][r+1][c+1])
        dig.append(board.big_boards_status[b][r+2][c+2])

        temp=self.calculatewincomb(dig,symbol,blkno)
        utilityvector.append(temp)
        


        #check dig2
        dig=[]
        dig.append(board.big_boards_status[b][r][c+2])
        dig.append(board.big_boards_status[b][r+1][c+1])
        dig.append(board.big_boards_status[b][r+2][c])

        temp=self.calculatewincomb(dig,symbol,blkno)
        utilityvector.append(temp)
        


        return(sum(utilityvector))



    def utility(self,board,symbol):
        """
        Heuristic function
        """
        utility=0
        # self.blockweight=[1,.9,1,.9,1.1,.9,1,.9,1,1,.9,1,.9,1.1,.9,1,.9,1]
        self.blockweight=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        #calculating weights of each block
        self.smallboardutility(board,symbol)
        
        #calculating big board utility 
        for i in range(2):
            for j in range(3):
                for k in range(3):
                    a=self.blockutility(board,i,3*j,k*3,symbol)
                    b=self.blockweight[9*i+j*3+k]
                    utility+=a*b

       

        # if symbol!=self.map_symbol[self.player]:
            # utility=-utility
        

########TESTING##################################
        # print "###############board vs utility####################33"
        # board.print_board()
        # print utility
        # print "###############board vs utility####################33"
        # print
        # print
        # print
        # a=raw_input()
#################TESTING############################################

        return(utility)


    def initialise_hashtable(self , board):
        self.dict = {}
        for m in range(2):
            for i in range(3):
                for j in range(3):
                    hash_value =0
                    if(m == 0):
                        hash_variable = 0
                    else:
                        hash_variable = 8
                    for k in range(3):
                        for l in range(3):
                            x = board.big_boards_status[m][3*i+k][3*j+l]
                            if (x == self.map_symbol[self.max_player]):
                                hash_value ^= self.zob_store[2*hash_variable]
                            elif (x == self.map_symbol[(self.max_player)^1]):
                                hash_value ^= self.zob_store[2*hash_variable+1]
                            hash_variable +=1
                    self.hash_store[m][i][j] = hash_value
        #print self.hash_store



    def update_hashtable(self,move,player):
    	#print "Update function called"
    	#print self.hash_store
        board_num = move[0]
        row_num = move[1]/3
        col_num = move[2]/3
        if(board_num == 0):
            hash_var = 3*(move[1]%3) + (move[2]%3)
        else:
            hash_var = 3*(move[1]%3) + (move[2]%3)+8
        if (player == self.max_player):        
            self.hash_store[board_num][row_num][col_num] ^= self.zob_store[2*hash_var]
        else:
            self.hash_store[board_num][row_num][col_num] ^= self.zob_store[2*hash_var+1]
    
    
        
    def prunealphabeta(self,board,depth,player,player_move,alpha,beta,prev):
        """
        minimax+alphabeta
        """

##########################testing#################################
        # print "#############testing###################33"
        # print "self_player"
        # print self.player
        # print "player"
        # print prev
        # a=raw_input()
        # print "#############testing###################33"
##########################testing#################################

        if time() - self.start > self.limit:
            return self.utility(board,self.map_symbol[self.player])

        if board.find_terminal_state() != ('CONTINUE','-') or depth == 0:
            return self.utility(board,self.map_symbol[self.player])

        moves_available = board.find_valid_move_cells(player_move)
        
        if player == self.max_player :
            cur_utility = -self.inf
        else:
            cur_utility = self.inf

        tempbonusmove = self.bonus_move_cur[player]
        
        for moves in moves_available:

            self.bonus_move_cur[player] = tempbonusmove

            self.update_hashtable(moves,player)
            
            gamepos,status = board.update(player_move,moves,self.map_symbol[player])
            if status:
                self.bonus_move_cur[player] ^= 1
            else:
                self.bonus_move_cur[player] = 0
            
            if player == self.max_player:
                if status and self.bonus_move_cur[player] == 1:
                    cur_utility = max(cur_utility,self.prunealphabeta(board,depth-1,
                                        player,moves,alpha,beta,player))
                    self.bonus_move_cur[player] = 0
                else:
                    cur_utility = max(cur_utility,self.prunealphabeta(board,depth-1,
                                        player^1,moves,alpha,beta,player))
                alpha = max(alpha,cur_utility)
            else:
                if status and self.bonus_move_cur[player] == 1:
                    cur_utility = min(cur_utility,self.prunealphabeta(board,depth-1,
                                        player,moves,alpha,beta,player))
                    self.bonus_move_cur[player] = 0
                else:
                    cur_utility = min(cur_utility,self.prunealphabeta(board,depth-1,
                                        player^1,moves,alpha,beta,player))
                beta = min(beta,cur_utility)

            self.update_hashtable(moves,player)

            board.big_boards_status[moves[0]][moves[1]][moves[2]] = "-"
            board.small_boards_status[moves[0]][moves[1]/3][moves[2]/3] = "-"
            
            if(beta <= alpha):
                break
            if time() - self.start > self.limit:
                break
        
        self.bonus_move_cur[player] = tempbonusmove
        return cur_utility



    def alphabetamove(self,board,old_move,player,depth):
        """
        Preprocessing for alpha beta algorithm
        """

        #find all possible moves
        self.nextmoves = board.find_valid_move_cells(old_move)
        
        #initialise maximum value
        curmax = -self.inf

        #tells if player has bonus move 
        tempbonusmove = self.bonus_move_cur[player]
        
        for moves in self.nextmoves:

            self.bonus_move_cur[player] = tempbonusmove

            self.update_hashtable(moves,player)
            
            #checks if any cell won
            gamepos,status = board.update(old_move,moves,self.map_symbol[player])
            if status:
                self.bonus_move_cur[player] ^= 1
            else:
                self.bonus_move_cur[player] = 0
            
            #check utility after winning 
            if status and (self.bonus_move_cur[player] == 1):
                player_utility = self.prunealphabeta(board,depth - 1,player,moves,-self.inf,self.inf,player)#same player moves
            else:
                player_utility = self.prunealphabeta(board,depth-1,player^1,moves,-self.inf,self.inf,player)#opponent moves
            
            #restore the board states
            board.big_boards_status[moves[0]][moves[1]][moves[2]] = "-"
            board.small_boards_status[moves[0]][moves[1]/3][moves[2]/3] = "-"
            
            self.update_hashtable(moves,player)


            if player_utility > curmax and player==self.max_player:
                cur_best_move = moves
                curmax = player_utility
           


##########################testing#################################
            # print "############curmax test###############33"
            # print player_utility
            # print "curmax is below"
            # print curmax
            # print "############curmax test###############33"
            # a=raw_input()
##########################testing#################################
        
        self.bonus_move_cur[player] = tempbonusmove
        
##########################testing#################################
        # print "##########final utility##################"
        # print curmax
        # a=raw_input()
        # print "##########final utility##################"
##########################testing#################################

        return cur_best_move
   

    def idfs(self,board,oldmv,tree_level,player):
        """
        idfs returns best move
        """

        for depth in range(1,self.maxdepth):

			# self.transpositionTable={}

#####################testing###########################
            # print "######depth test#########"
            # print depth
            # print "######depth test#########"
            # a=raw_input()
#####################testing###########################

            if(time()-self.start)>self.limit:
                break
            output = self.alphabetamove(board,oldmv,player,depth)
		
        return output
   


    def move(self,gameboard,oldmove,symbol):
        """
        Main code
        """
    
        #start timer
        self.start=time()

        #initialising players
        if symbol=='x':
            self.max_player=1
            self.player=1
            self.opponent=0
        else:
            self.max_player=0
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
            if(self.last_blk_won):
                self.bonus_move_cur[self.max_player]^=1
            else:
                self.bonus_move_cur[self.max_player]=0

            tempmove=self.idfs(tempboard,oldmove,depth,self.player)

            status,blk_won=tempboard.update(oldmove,tempmove,self.map_symbol[self.player])

            if blk_won:
                self.last_blk_won^=1
            else:
                self.last_blk_won=0

            #restore the board states
            tempboard.big_boards_status[tempmove[0]][tempmove[1]][tempmove[2]] = "-"
            tempboard.small_boards_status[tempmove[0]][tempmove[1]/3][tempmove[2]/3] = "-"


            print time()-self.start
            return tempmove

        except Exception as e:
            print 'Exception occurred ', e
            print 'Traceback printing ', sys.exc_info()
            print traceback.format_exc()