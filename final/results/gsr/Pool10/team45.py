import random
from copy import deepcopy
import time



class Team45:
    def __init__(self):
        self.initial_move = (0, 4, 4)
        self.valid_cells = ()
        self.me = ''
        self.other = ''
        self.no_move = (-1, -1, -1)
        self.reward_max = 100000
        self.reward_min = -100000
        self.positive_infinity = float("inf")
        self.negative_infinity = float("-inf")
        self.winning_small_board_points = 500
        # self.big_board_pattern_mul = (1, 3, 70)
        # self.big_board_pattern_mul = (1, 3, 50)
        self.big_board_pattern_mul = (0, 1, 20, 50)

        # self.small_board_pattern_mul = (0, 8, 10)
        self.small_board_pattern_mul = (0, 0, 30, 40)

        self.board_position_weights = ((4,6,4), (6,3,6), (4,6,4))
        # self.board_position_weights = ((3,2,3), (2,4,2), (3,2,3))
        self.block_position_weights = ((3,2,3), (2,4,2), (3,2,3))
        # self.big_board_heuristic_store

        self.winning_patterns = []

        # self.winning_patterns.append(((0, 0, 0), (0, 1, 1), (0, 2, 2)))
        # self.winning_patterns.append(((1, 0, 0), (1, 1, 1), (1, 2, 2)))
        # self.winning_patterns.append(((0, 0, 2), (0, 1, 1), (0, 2, 0)))
        # self.winning_patterns.append(((1, 0, 2), (1, 1, 1), (1, 2, 0)))

        # for i in range(2):
        #     self.winning_patterns.append(((i, 0, 0), (i, 1, 1), (i, 2, 2)))
        #     self.winning_patterns.append(((i, 0, 2), (i, 1, 1), (i, 2, 0)))
        #     for j in range(3):
        #         self.winning_patterns.append(((i, j, 0), (i, j, 1), (i, j, 2)))
        #         self.winning_patterns.append(((i, 0, j), (i, 1, j), (i, 2, j)))

        self.winning_patterns.append(((0, 0), (1, 1), (2, 2)))
        self.winning_patterns.append(((0, 2), (1, 1), (2, 0)))
        for j in range(3):
            self.winning_patterns.append(((j, 0), (j, 1), (j, 2)))
            self.winning_patterns.append(((0, j), (1, j), (2, j)))

        self.winning_patterns = tuple(self.winning_patterns)


        self.board_heu = {}
        self.block_heur = {}
        self.random_tab = [[[[long(0) for _ in xrange(2)] for _ in xrange(2) ] for _ in xrange(9)] for _ in xrange(9) ]
        self.boards_hash = long(0)
        self.blocks_hash = [[[long(0) for _ in xrange(2)] for _ in xrange(3)] for _ in xrange(3)]


        for row in xrange(9):
            for column in xrange(9):
                for num in xrange(2):
                    for player in xrange(2):
                        self.random_tab[row][column][num][player] = long(random.randint(1, 2**64))

        pass

    def add_move_to_hash(self, cell, player):
        num = cell[0]
        x = cell[1]
        y = cell[2]
        self.boards_hash ^= self.random_tab[x][y][num][player]
        # print cell

        self.blocks_hash[cell[1]/3][cell[2]/3][num] ^= self.random_tab[x][y][num][player]

    def value_of_pattern(self, num, pattern, small_boards_scores):
        value = 0
        count = 0
        for position in pattern:
            temp = small_boards_scores[num][position[0]][position[1]]
            if temp < 0:
                return 0
            value += temp
            if temp == self.winning_small_board_points:
                count += 1

        return value * self.big_board_pattern_mul[count]

    def block_pattern_checker(self, symbol, small_board, pos_arr):
        count = 0
        for pos in pos_arr:
            if small_board[pos[0]][pos[1]] == symbol:
                count += 1
            elif small_board[pos[0]][pos[1]] == self.opposite_symbol(symbol):
                return 0

        return self.small_board_pattern_mul[count]

    def block_heuristic(self, symbol, small_board):
        blockHeur = 0

        for pos_arr in self.winning_patterns:
            blockHeur += self.block_pattern_checker(symbol, small_board, pos_arr)

        for i in xrange(3):
            for j in xrange(3):
                if small_board[i][j] == symbol:
                    blockHeur += (0.1) * self.block_position_weights[i][j]

        return blockHeur

    def board_heuristic(self, small_boards_scores):
        value = 0
        for num in range(2):
            for i in xrange(3):
                for j in xrange(3):
                    if small_boards_scores[num][i][j] > 0:
                        value += 0.02 * self.board_position_weights[i][j] * small_boards_scores[num][i][j]

        return value

    def heuristics(self, board, ply):
        if (self.boards_hash, ply) in self.board_heu:
            return self.board_heu[(self.boards_hash, ply)]
        small_boards_scores = [[[0 for _ in xrange(3)] for _ in xrange(3)] for _ in xrange(2)]

        for i in xrange(2):
            for j in xrange(3):
                for k in range(3):
                    if board.small_boards_status[i][j][k] == ply:
                        # exit(0)
                        small_boards_scores[i][j][k] = self.winning_small_board_points
                    elif board.small_boards_status[i][j][k] == self.opposite_symbol(ply) or board.small_boards_status[i][j][k] == 'd':
                        small_boards_scores[i][j][k] = -1
                    else:
                        # small_boards_scores[i][j][k] = 0
                        # block = tuple([tuple(board[i][3 * j + x][4 * j:4 * (j + 1)]) for x in xrange(4)])
                        # small_board = tuple([tuple(board[i][3*j + x][3*k:3*(k+1)]) for x in xrange(3)])
                        # print board[i]
                        # board.print_board()
                        small_board = board.big_boards_status[i][3*j:3*(j+1)][3*k:3*(k+1)]
                        row = 3*j
                        column = 3*k
                        small_board = []
                        for row in range(3*j, 3*j+3):
                            small_board.append(board.big_boards_status[i][row][column:column+3])
                        # print small_board
                        # print i, j, k
                        if (self.blocks_hash[j][k][i], ply) in self.block_heur:
                            small_boards_scores[i][j][k] = self.block_heur[(self.blocks_hash[j][k][i], ply)]
                        else:
                            small_boards_scores[i][j][k] = self.block_heuristic(ply, small_board)
                            self.block_heur[(self.blocks_hash[j][k][i], ply)] = small_boards_scores[i][j][k]

        value = 0
        for i in range(2):
            for pattern in self.winning_patterns:
                value += self.value_of_pattern(i, pattern, small_boards_scores)

        value += self.board_heuristic(small_boards_scores)
        self.board_heu[(self.boards_hash, ply)] = value

        # print 'val', value

        return value




    def print_winning_patterns(self):
        print "Diamond patterns"
        print self.winning_patterns[0]
        print self.winning_patterns[1]
        print "Row patterns"
        for i in range(1,4):
            print self.winning_patterns[2*i]
        print "Column patterns"
        for i in range(1,4):
            print self.winning_patterns[2*i+1]



    def small_pattern_checker(self):
        pass


    def minimax(self, board, is_max, depth, max_depth, old_move, alpha, beta, start_time):

        check_status = board.find_terminal_state()

        if check_status[1] == 'WON':
            if check_status[0] == self.me:
                return self.no_move, self.positive_infinity
            else:
                return self.no_move, self.negative_infinity

        elif check_status[1] == 'DRAW':
            return self.no_move, self.reward_min



        if depth == max_depth:
            if is_max:
                sign = 1
            else:
                sign = -1
            # return self.no_move, sign*self.heuristics(board, self.player_symbol(is_max))
            return self.no_move, self.heuristics(board, self.me) - self.heuristics(board, self.opposite_symbol(self.me))

        valid_cells = board.find_valid_move_cells(old_move)

        if is_max:
            max_value = self.negative_infinity
            index = 0
            for i in xrange(len(valid_cells)):
                cell = valid_cells[i]
                if time.time() - start_time > 21:
                    break
                board.update(old_move, cell, self.player_symbol(is_max))
                self.add_move_to_hash(cell, 1)
                value = self.minimax(board, not is_max, depth+1, max_depth, cell, alpha, beta, start_time)[1]
                if value > max_value:
                    max_value = value
                    index = i
                if max_value > alpha:
                    alpha = max_value

                board.big_boards_status[cell[0]][cell[1]][cell[2]] = '-'
                board.small_boards_status[cell[0]][cell[1]/3][cell[2]/3] = '-'
                self.add_move_to_hash(cell, 1)
                if alpha >= beta:
                    break

            return valid_cells[index], max_value

        else:
            min_value = self.positive_infinity
            index = 0
            for i in xrange(len(valid_cells)):
                cell = valid_cells[i]
                if time.time() - start_time > 21:
                    break
                board.update(old_move, cell, self.player_symbol(is_max))
                self.add_move_to_hash(cell, 0)
                value = self.minimax(board, not is_max, depth+1, max_depth, cell, alpha, beta, start_time)[1]
                if value < min_value:
                    min_value = value
                    index = i
                if min_value < beta:
                    beta = min_value

                board.big_boards_status[cell[0]][cell[1]][cell[2]] = '-'
                board.small_boards_status[cell[0]][cell[1] / 3][cell[2] / 3] = '-'
                self.add_move_to_hash(cell, 0)
                if alpha >= beta:
                    break
            return valid_cells[index], min_value


    def player_symbol(self, is_max):
        return self.me if is_max else self.other


    @staticmethod
    def opposite_symbol(symbol):
        return 'x' if symbol == 'o' else 'x'


    def move(self, board, old_move, symbol):
        # print 'symbol', symbol
        # print 'old_move', old_move
        start = time.time()
        self.me = symbol
        self.other = self.opposite_symbol(symbol)

        if old_move[0] == -1:
            self.add_move_to_hash(self.initial_move, 1)
            return self.initial_move
        else:
            if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == self.opposite_symbol(symbol):
                self.add_move_to_hash(old_move, 0)

        max_depth = 4

        valid_cells = board.find_valid_move_cells(old_move)
        # print 'valid cell moves', self.valid_cells

        temp_board = deepcopy(board)
        best_move = valid_cells[0]
        while True:
            if time.time()-start >= 21:
                # exit(0)
                break
            print max_depth
            best_move = self.minimax(temp_board, True, 0, max_depth, old_move, self.negative_infinity, self.positive_infinity, start)[0]
            max_depth += 1


        self.add_move_to_hash(best_move, 1)
        return best_move