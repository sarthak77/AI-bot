import random

class Team43:
    def __init__(self):
        self.ids = 3
        self.maxdepth = 1
        self.inf = 1e9  # 1e9
        self.half_inf = 1e7
        self.moveno = 0

        # for a symbol present at this position
        self.pos_weight = [
            [
                [3, 2, 3], [2, 4, 2], [3, 2, 3]
            ],
            [
                [300, 200, 300], [200, 400, 200], [300, 200, 300]
            ]
        ]

        # points that will be earned by playing at this position
        self.pos_points = [
            [
                [40, 60, 40], [60, 30, 40], [40, 60, 40]
            ],
            [
                [400, 600, 400], [600, 300, 400], [400, 600, 400]
            ]
        ]

        # based on how many symbols out of 3 present in a pattern
        self.pattern_points = [
            [0, 50, 1e4], [100, 1e4, self.half_inf]
        ]

        self.block_points = 5000

        # d1,d2
        self.pattern_present = [
        	[[1,0],[0,0],[0,1]],
        	[[0,0],[1,1],[0,0]],
        	[[0,1],[0,0],[1,0]]
        ]

    def move(self, board, old_move, flag):
        print 'Enter your move: <format:board row column> (you\'re playing with', flag + ")"
        self.moveno += 1

        # else apply minimax at current node
        all_moves = board.find_valid_move_cells(old_move)

        if self.moveno == 1:
            return all_moves[random.randrange(len(all_moves))]

        ret_move = []
        if flag == "x":
            v = -self.inf
            # for iterative deepening
            for i in range(self.ids):
            	self.maxdepth = i+1
            	for move in all_moves:
                    board.update(old_move,move,flag)
                    points = self.minimax(board, False, 1, -self.inf,self.inf, move, flag)
                    if v < points:
	                    ret_move = move
	                    v = points
                    board.big_boards_status[move[0]][move[1]][move[2]] = '-'
                    board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'
	                # board.big_boards_status[move[0]][move[1]][move[2]] = '-'
        else:
            v = self.inf
            for i in range(self.ids):
            	self.maxdepth = i+1
            	for move in all_moves:
                    board.update(old_move,move,flag)
                    points = self.minimax(board, True, 1, -self.inf,self.inf, move, flag)
                    if v > points:
	                    ret_move = move
	                    v = points
                    board.big_boards_status[move[0]][move[1]][move[2]] = '-'
                    board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'

        return (ret_move)

    def minimax(self, board, isMaxPlayer, depth, alpha, beta, old_move, ply):

        if self.maxdepth == depth:
            joffrey = self.calculate_heuristic(
                board, ply, isMaxPlayer, old_move, depth)
            return joffrey

        all_moves = board.find_valid_move_cells(old_move)
        random.shuffle(all_moves)

        if isMaxPlayer == True:
            v = -self.inf
            for move in all_moves:
                board.big_boards_status[move[0]][move[1]][move[2]] = ply

                val = self.minimax(
                    board, False, depth+1, alpha, beta, move, 'o')
                board.big_boards_status[move[0]][move[1]][move[2]] = '-'
                v = max(v, val)
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        else:
            v = self.inf
            for move in all_moves:
                board.big_boards_status[move[0]][move[1]][move[2]] = ply

                val = self.minimax(
                    board, True, depth+1, alpha, beta, move, 'x')
                board.big_boards_status[move[0]][move[1]][move[2]] = '-'
                v = min(v, val)
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

    def calculate_heuristic(self, board, ply, isMaxPlayer, played_move,depth):
        # b1 = utility value of bigBoard1
        # b2 = utility value of bigBoard2
        # small board - board, x1, y1, typ, ply, board number
        # big board - board, x1, y1, typ, ply
        b1 = 0
        for i in range(3):
            for j in range(3):
                # if (played_move[1] in range(3*i,3*i+3)) and (played_move[2] in range(3*j,3*j+3)):
                    b1 += self.calc_small_board(board, 3*i, 3*j, 0, ply, 0,depth,played_move)
        r1 = [self.find_complete(board, 0, 0, 0),
              self.find_complete(board, 0, 3, 0),
              self.find_complete(board, 0, 6, 0)]
        r2 = [self.find_complete(board, 3, 0, 0),
              self.find_complete(board, 3, 3, 0),
              self.find_complete(board, 3, 6, 0)]
        r3 = [self.find_complete(board, 6, 0, 0),
              self.find_complete(board, 6, 3, 0),
              self.find_complete(board, 6, 6, 0)]
        
        arr1 = [r1, r2, r3]
        b1 += self.calc_big_board(arr1, 1, ply,depth,played_move)

        b2 = 0
        for i in range(3):
            for j in range(3):
                if (played_move[1] in range(3*i,3*i+3)) and (played_move[2] in range(3*j,3*j+3)):
                    b2 += self.calc_small_board(board, 3*i, 3*j, 0, ply, 1,depth,played_move)
        r1 = [self.find_complete(board, 0, 0, 1),
              self.find_complete(board, 0, 3, 1),
              self.find_complete(board, 0, 6, 1)]
        r2 = [self.find_complete(board, 3, 0, 1),
              self.find_complete(board, 3, 3, 1),
              self.find_complete(board, 3, 6, 1)]
        r3 = [self.find_complete(board, 6, 0, 1),
              self.find_complete(board, 6, 3, 1),
              self.find_complete(board, 6, 6, 1)]
        arr1 = [r1, r2, r3]
        b2 += self.calc_big_board(arr1, 1, ply,depth,played_move)

        if abs(b1) > abs(b2):
            return b1
        else:
            return b2

    def calc_small_board(self, board, x1, y1, typ, ply, k,depth,played_move):
        # small board - board, x1, y1, typ, ply, k(=board number)
        # typ = 0 for SmallBoard
        # k = board number
        a = self.pattern_points[typ]
        w = self.pos_weight[typ]
        total_score = 0
        xx, yy = played_move[1]%3, played_move[2]%3
        
        if (played_move[1] in range(x1,x1+3)) and (played_move[2] in range(y1,y1+3)):
            # hor patterns
            flag = False
            c1, c2 = 0, 0
            for j in range(3):
                if board.big_boards_status[k][played_move[1]][j+y1] == 'x':
                    c1 += 1
                elif board.big_boards_status[k][played_move[1]][j+y1] == 'o':
                    c2 += 1
            if c2 == 0 and c1 > 0:
                total_score += a[c1-1]
            elif c1 == 0 and c2 > 0:
                total_score -= a[c2-1]

        if (played_move[1] in range(x1,x1+3)) and (played_move[2] in range(y1,y1+3)):
            # vertical patterns
            flag = False
            c1, c2 = 0, 0
            for j in range(3):
                if board.big_boards_status[k][j+x1][played_move[2]] == 'x':
                    c1 += 1
                elif board.big_boards_status[k][j+x1][played_move[2]] == 'o':
                    c2 += 1
            if c2 == 0 and c1 > 0:
                total_score += a[c1-1]
            elif c1 == 0 and c2 > 0:
                total_score -= a[c2-1]

        if (played_move[1] in range(x1,x1+3)) and (played_move[2] in range(y1,y1+3)) and (self.pattern_present[xx][yy][0]==1):
            # for diagonal pattern1
            c1, c2 = 0,0
            flag = False
            for i in range(3):
                if board.big_boards_status[k][x1+i][y1+i] == 'x':
                    c1 += 1
                elif board.big_boards_status[k][x1+i][y1+i] == 'o':
                    c2 += 1
            if c2 == 0 and c1 > 0:
                total_score += a[c1-1]
            elif c1 == 0 and c2 > 0:
                total_score -= a[c2-1]

        if (played_move[1] in range(x1,x1+3)) and (played_move[2] in range(y1,y1+3)) and (self.pattern_present[xx][yy][1]==1):
            # for diagonal pattern1
            c1, c2 = 0,0
            flag = False
            for i in range(3):
                if board.big_boards_status[k][x1+i][y1+2-i] == 'x':
                    c1 += 1
                elif board.big_boards_status[k][x1+i][y1+2-i] == 'o':
                    c2 += 1
            if c2 == 0 and c1 > 0:
                total_score += a[c1-1]
            elif c1 == 0 and c2 > 0:
                total_score -= a[c2-1]

        # taken into consideration weights of smaller boards
        for i in range(3):
            for j in range(3):
                if board.big_boards_status[k][i+x1][j+y1] == 'x':
                    total_score += w[i][j]
                elif board.big_boards_status[k][i+x1][j+y1] == 'o':
                    total_score -= w[i][j]

    	tempo = 0
        if depth == 1 and (played_move[1] in range(x1,x1+3)) and (played_move[2] in range(y1,y1+3)):
        	not_ply = 'o' if ply=='x' else 'x'
    		xx,yy = played_move[1]%3, played_move[2]%3

    		# vertical
    		c1,c2,t=0,0,0
    		for i in range(3):
    			if board.big_boards_status[k][i+x1][played_move[2]] == 'x':
    				c1 += 1
    			elif board.big_boards_status[k][i+x1][played_move[2]] == 'o':
    				c2 += 1
			if c2==2 and c1==1:
				t = self.block_points if ply == 'x' else -self.block_points
				tempo += t
    		
    		# horizontal
			c1,c2=0,0
			for i in range(3):
				if board.big_boards_status[k][played_move[1]][y1+i] == 'x':
					c1 += 1
				elif board.big_boards_status[k][played_move[1]][y1+i] == 'o':
					c2 += 1
			if c2==2 and c1==1:
				t = self.block_points if ply == 'x' else -self.block_points
				tempo += t
    		if self.pattern_present[xx][yy][0] == 1:
    			c1,c2,t=0,0,0
    			for i in range(3):
    				if board.big_boards_status[k][i+x1][y1+i] == 'x':
    					c1 += 1
    				elif board.big_boards_status[k][i+x1][y1+i] == 'o':
    					c2 += 1
    			if c2==2 and c1==1:
    				t = self.block_points if ply == 'x' else -self.block_points
    				tempo += t
    		if self.pattern_present[xx][yy][1] == 1:
    			c1,c2,t=0,0,0
    			for i in range(3):
    				if board.big_boards_status[k][i+x1][y1+2-i] == 'x':
    					c1 += 1
    				elif board.big_boards_status[k][i+x1][y1+2-i] == 'o':
    					c2 += 1
    			if c2==2 and c1==1:
    				t = self.block_points if ply == 'x' else -self.block_points
    				tempo += t
        total_score += tempo

        tempo = 0

        if depth == 2 and (played_move[1] in range(x1,x1+3)) and (played_move[2] in range(y1,y1+3)):
            # ply ka count 3 -> return same sign thing -> -inf for 'o' and inf for 'x' 

            xx,yy = played_move[1]%3, played_move[2]%3
            
            # horizontal
            c1=0
            for i in range(3):
                if board.big_boards_status[k][played_move[1]][y1+i] == ply:
                    c1 += 1
            if c1==3:
                if ply == 'x':
                    total_score += self.half_inf
                else:
                    total_score += (-self.half_inf)

            # vertical
            c1=0
            for i in range(3):
                if board.big_boards_status[k][x1+i][played_move[2]] == ply:
                    c1 += 1
            if c1==3:
                if ply == 'x':
                    total_score += self.half_inf
                else:
                    total_score += (-self.half_inf)             

            if self.pattern_present[xx][yy][0] == 1:
                c1 = 0
                for i in range(3):
                    if board.big_boards_status[k][x1+i][y1+i] == ply:
                        c1 += 1
                if c1==3:
                    if ply == 'x':
                        total_score += self.half_inf
                    else:
                        total_score += (+self.half_inf)

            if self.pattern_present[xx][yy][1] == 1:
                c1 = 0
                for i in range(3):
                    if board.big_boards_status[k][x1+i][y1+2-i] == ply:
                        c1 += 1
                if c1==3:
                    if ply == 'x':
                        total_score += self.half_inf
                    else:
                        total_score += (-self.half_inf)
        return total_score

    def find_complete(self, board, x, y, k):
        c1, c2, c3 = 0, 0, 0
        for i in range(3):
            for j in range(3):
                if board.big_boards_status[k][x+i][y+j] == 'x':
                    c1 += 1
                elif board.big_boards_status[k][x+i][y+j] == 'o':
                    c2 += 1
                else:
                    c3 += 1
        if c1 == 9:
            return 'x'
        elif c2 == 9:
            return 'o'
        else:
            return '-'

    def calc_big_board(self, board, typ, ply,depth,played_move):
        # big board - board, x1, y1, typ, ply
        # typ = 1 for BigBoard

        a = self.pattern_points[typ]
        w = self.pos_weight[typ]

        xx, yy = played_move[1]/3,played_move[2]/3

        # hor patterns
        total_score= 0
        flag = False
        c1, c2 = 0, 0
        for j in range(3):
            if board[xx][j] == 'x':
                c1 += 1
            elif board[xx][j] == 'o':
                c2 += 1
        if c2 == 0 and c1 > 0:
            total_score += a[c1-1]
        elif c1 == 0 and c2 > 0:
            total_score -= a[c2-1]

        # vertical patterns
        flag = False
        c1, c2 = 0, 0
        for j in range(3):
            if board[j][yy] == 'x':
                c1 += 1
            elif board[j][yy] == 'o':
                c2 += 1
        if c2 == 0 and c1 > 0:
            total_score += a[c1-1]
        elif c1 == 0 and c2 > 0:
            total_score -= a[c2-1]

        # for diagonal pattern1
        if self.pattern_present[xx][yy][0]==1:
            c1, c2 = 0,0
            flag = False
            for i in range(3):
                if board[i][i] == 'x':
                    c1 += 1
                elif board[i][i] == 'o':
                    c2 += 1

            if c2 == 0 and c1 > 0:
                total_score += a[c1-1]
            elif c1 == 0 and c2 > 0:
                total_score -= a[c2-1]

        # for diagonal pattern2
        if self.pattern_present[xx][yy][1]==1:
            c1, c2 = 0,0
            flag = False
            for i in range(3):
                if board[i][2-i] == 'x':
                    c1 += 1
                elif board[i][2-i] == 'o':
                    c2 += 1
            if c2 == 0 and c1 > 0:
                total_score += a[c1-1]
            elif c1 == 0 and c2 > 0:
                total_score -= a[c2-1]

        # taken into consideration weights of smaller boards
        for i in range(3):
            for j in range(3):
                if board[i][j] == 'x':
                    total_score += w[i][j]
                elif board[i][j] == 'o':
                    total_score -= w[i][j]

        return total_score
