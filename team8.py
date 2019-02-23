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


    def idfs(self,board,oldmv,symbol,depth):
        """
        idfs,minmax,alpha beta pruning implemented
        """
     
        if depth>self.maxdepth:
            return

        cells = board.find_valid_move_cells(oldmv)

        for mv in cells:
            # print mv,depth

            self.makemv(board,oldmv,mv,symbol)
            tempboard=deepcopy(board)
            self.idfs(tempboard,mv,symbol,depth+1)
            self.reverse(board,mv)

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


    

