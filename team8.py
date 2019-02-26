"""
Class for AI bot
"""
import random
import traceback
import sys
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
        self.default=(1,1,1)#default move
        self.limit=23
        self.start=0
        self.ps=''
        self.os=''
        self.maxdepth=0

        self.bestmv=(0,0,0)
        self.initial_level = 2
        #self.endtime = 23
        self.inf = 100000000
        #self.starttime = 0
        self.max_player = 1
        self.map_symbol = ['o', 'x']
        self.zob_store = []
        self.hash_store = []
        self.bonus_move_cur = [0 , 0]
        #self.maxlen = 0
        #self.mindepth = 9
        self.last_blk_won = 0
        for i in range(3):
            self.hash_store.append([0]*3)
        self.numsteps = 0
        for i in range(36):
            self.zob_store.append(2**i)
        self.dict = {}

    def smallboardutility(self,board,symbol):
        """
        Find small board utility
        """
        for b in range(2):

            #r1 r2 r3 c1 c2 c3 d1 d2
            utilityvector=[]
            
            #check r1 r2 r3
            for i in range(3):
                row=[]
                row.append(board.small_boards_status[b][i][0])
                row.append(board.small_boards_status[b][i][1])
                row.append(board.small_boards_status[b][i][2])
                utilityvector.append(self.calculatewincomb(row,symbol))

            #check c1 c2 c3
            for i in range(3):
                col=[]
                col.append(board.small_boards_status[b][0][i])
                col.append(board.small_boards_status[b][1][i])
                col.append(board.small_boards_status[b][2][i])
                utilityvector.append(self.calculatewincomb(col,symbol))

            #check dig1
            dig=[]
            dig.append(board.small_boards_status[b][0][0])
            dig.append(board.small_boards_status[b][1][1])
            dig.append(board.small_boards_status[b][2][2])
            utilityvector.append(self.calculatewincomb(dig,symbol))

            #check dig2
            dig=[]
            dig.append(board.small_boards_status[b][0][2])
            dig.append(board.small_boards_status[b][1][1])
            dig.append(board.small_boards_status[b][2][0])
            utilityvector.append(self.calculatewincomb(dig,symbol))

        #modify later
        return(sum(utilityvector))


    def calculatewincomb(self,v,symbol):
        """
        Calculate status of each row,column,dig
        """
        if symbol=='x':
            opp='o'
        else:
            opp='x'

        if (symbol in v) and (opp not in v):
            return 1
        if (opp in v) and (symbol not in v):
            return -1
        if ('-' in v) and (symbol not in v) and (opp not in v):
            return .5
        if (symbol in v) and (opp in v):
            return 0 


    def blockutility(self,board,b,r,c,symbol):
        """
        Calculate utility of each cell of big board
        """
        #r1 r2 r3 c1 c2 c3 d1 d2
        utilityvector=[]

        #check r1 r2 r3
        for i in range(3):
            row=[]
            row.append(board.big_boards_status[b][r+i][c])
            row.append(board.big_boards_status[b][r+i][c+1])
            row.append(board.big_boards_status[b][r+i][c+2])
            utilityvector.append(self.calculatewincomb(row,symbol))


        #check c1 c2 c3
        for i in range(3):
            col=[]
            col.append(board.big_boards_status[b][r][c+i])
            col.append(board.big_boards_status[b][r+1][c+i])
            col.append(board.big_boards_status[b][r+2][c+i])
            utilityvector.append(self.calculatewincomb(col,symbol))

        #check dig1
        dig=[]
        dig.append(board.big_boards_status[b][r][c])
        dig.append(board.big_boards_status[b][r+1][c+1])
        dig.append(board.big_boards_status[b][r+2][c+2])
        utilityvector.append(self.calculatewincomb(dig,symbol))

        #check dig2
        dig=[]
        dig.append(board.big_boards_status[b][r][c+2])
        dig.append(board.big_boards_status[b][r+1][c+1])
        dig.append(board.big_boards_status[b][r+2][c])
        utilityvector.append(self.calculatewincomb(dig,symbol))

        return(sum(utilityvector))


    def utility(self,board,symbol):
        """
        Heuristic function
        """
        utility=0
        #calculating big board utility 
        for i in range(2):
            for j in range(3):
                for k in range(3):
                    utility+=self.blockutility(board,i,3*j,k*3,symbol)

        #calculating small board utility
        utility+=self.smallboardutility(board,symbol)

        return(utility)


    def makemv(self,board,oldmv,mv,symbol):
        """
        Function to make move for state change
        """
        # board.print_board()
        board.update(oldmv,mv,symbol)
        # board.print_board()

    def reverse(self,board,mv):
        """
        Function for reversing the move for backtracking
        """
        board.big_boards_status[mv[0]][mv[1]][mv[2]]="-"

    def initialise_hashtable(self , board):
        self.dict = {}
        for m in range(2):
            for i in range(3):
                for j in range(3):
                    cur_hash =0
                    cnt = 0
                    for k in range(3):
                        for l in range(3):
                            x = board.big_boards_status[m][3*i+k][3*j+l]
                            if (x == self.map_symbol[self.max_player]):
                                cur_hash ^= self.zob_store[2*cnt]
                            elif (x == self.map_symbol[(self.max_player)^1]):
                                cur_hash ^= self.zob_store[2*cnt+1]
                            cnt +=1
                    self.hash_store[m][i][j] = cur_hash
        #print self.hash_store

    def update_hashtable(self,move,player):
    	#print "Update function called"
    	#print self.hash_store
        board_no = move[0]
        row_no = move[1]/3
        col_no = move[2]/3
        x = 3*(move[1]%3) + (move[2]%3)
    

        if (player == self.max_player):        
            self.hash_store[board_no][row_no][col_no] ^= self.zob_store[2*x]
        else:
            self.hash_store[board_no][row_no][col_no] ^= self.zob_store[2*x+1]

    def idfs(self,board,oldmv,symbol,depth):
        """
        idfs,minmax,alpha beta pruning implemented
        """
        maxDepth=9*9
        for depth in range(1,maxdepth+1):
			self.transpositionTable={}
            if(time()-self.start)>self.limit:
                break
            output = self.alphabetamove(board,old_move,player,depth)
			finalMove = move
		return finalMove

        ######sarthak's function
        # if depth>self.maxdepth:
        #     return

        # cells = board.find_valid_move_cells(oldmv)

        # for mv in cells:
        #     # print mv,depth

        #     self.makemv(board,oldmv,mv,symbol)
        #     tempboard=deepcopy(board)
        #     self.idfs(tempboard,mv,symbol,depth+1)
        #     self.reverse(board,mv)

    def alphabetamove(self,board,old_move,player,depth):
        """
        Deciding best move
        """

        self.nextmoves = board.find_valid_move_cells(old_move)
        
        trymove = self.nextmoves[random.randrange(len(self.nextmoves))]
        
        curmax = -self.inf
        
        ###
        
        data = self.bonus_move_cur[player]
        
        for moves in self.nextmoves:
            self.bonus_move_cur[player] = data
            self.update_hashtable(moves,player)
            
            gamepos,status = board.update(old_move,moves,player)
            if status:
                self.bonus_move_cur[player] ^= 1
            else:
                self.bonus_move_cur[player] = 0
            
            if status and (self.bonus_move_cur[player] == 1):
                player_utility == self.prunealphabeta(board,depth - 1,player,moves,
                                                        -self.inf,self.inf,player)
            else:
                player_utility = self.prunealphabeta(board,depth-1,player^1,moves,
                                                        -self.inf,self.inf,player)
            
            #restore the board states
            board.big_boards_status[moves[0]][moves[1]][moves[2]] = "-"
            board.small_boards_status[moves[0]][moves[1]/3][moves[2]/3] = "-"
            self.update_hashtable(moves,player)

            if(player_utility > curmax):
                cur_best_move = moves
                curmax = player_utility
        
        self.bonus_move_cur[player] = data
            
    def prunealphabeta(self,board,depth,player,player_move,alpha,beta,prev):
        """
        alpha beta algorithm recursive
        """

        if time() - self.start > self.limit:
            ##return evaluated heuristic value
        if board.find_terminal_state() != ('CONTINUE','-'):
            ##return evaluated heuristic value

        moves_available = board.find_valid_move_cells(player_move)
        
        #if player is maximizing :
            #cur_utility = -self.inf
        #else:
            #cur_utility = self.inf

        data = self.bonus_move_cur[player]
        
        for moves in moves_available:
            self.bonus_move_cur[player] = data
            self.update_hashtable(moves,player)
            gamepos,status = board.update(old_move,moves,player)
            if status:
                self.bonus_move_cur[player] ^= 1
            else:
                self.bonus_move_cur[player] = 0
            
            if player = self.max_player:
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
                alpha = min(alpha,cur_utility)

            self.update_hashtable(moves,player)
            board.big_boards_status[moves[0]][moves[1]][moves[2]] = "-"
            board.small_boards_status[moves[0]][moves[1]/3][moves[2]/3] = "-"
            if datetime.datetime.utcnow() - self.begin > self.limit:
                break
            if(beta <= alpha):
                break
        

        self.bonus_move_cur[player] = data
        return cur_utility



    def move(self,gameboard,oldmove,symbol):
        """
        Main code
        """
        if symbol=='x':
            self.ps='x'
            self.os='o'
        else:
            self.ps='o'
            self.os='x'

        try:
            if oldmove == (-1,-1,-1):
                return self.default
            
            self.start=time()
            # print self.start

            print "oldmove::"
            print oldmove

            cells = gameboard.find_valid_move_cells(oldmove)
            print cells
            mvp = raw_input()

            tempboard=deepcopy(gameboard)
            self.idfs(tempboard,oldmove,symbol,0)
            print self.utility(tempboard,symbol)

            return cells[random.randrange(len(cells))]

        #
        #       preprocessing...
        #
        # for depth in range(...):
        #      minimax()
        #   return nxtmv
        #
        #
        #
        #
        #
        #
        #
        #

        
        except Exception as e:
            print 'Exception occurred ', e
            print 'Traceback printing ', sys.exc_info()
            print traceback.format_exc()


    

