
from copy import deepcopy
from time import time

class Team68:

    def __init__(self):
        
       
        self.my_flag_int = 0
        self.start_time = 0
        self.first = True
        self.win_utility = 10000000
        self.lose_utility = -1*self.win_utility
        self.score_block = 1000.0
        self.oneattc = self.score_block/10
        self.twoattc = self.oneattc/10
        self.attack_weight = 0.5
        self.game_weight = 1 / 3000
        self.max_time = 23
        self.mvgavg = 0.0
        self.size = 0.0
        self.patterns = [[0,1,2],[0,3,6],[0,4,8],[1,4,7],[2,4,8],[2,4,6],[3,4,5],[6,7,8]]
        self.patterns_X_Y = [[[0,0] ,[0,1] ,[0,2]],[[0,0] ,[1,0],[2,0]],[[0,0],[1,1],[2,2]],[[0,1],[1,1],[2,1]],[[0,2],[1,2],[2,2]],[[0,2],[1,1],[2,0]],[[1,0],[1,1],[1,2]],[[2,0],[2,1],[2,2]]]


    def opposite_flag(self, flag):
        if flag == 'x':
            return 'o'
        return 'x'

    def flag_to_int(self, flag):
        if flag == 'x':
            return 1
        else:
            return 0
    
    def int_to_flag(self,x):
        if x == 0:
            return 'o'
        else:
            return 'x'

    def update(self, board, old_move, new_move, ply):
        board.big_boards_status[new_move[0]][new_move[1]][new_move[2]] = ply
        for i in range(3):
            if board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + i][3 * (new_move[2]/3)] == board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + i][3 * (new_move[2]/3) + 1] == board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + i][3 * (new_move[2]/3) + 2] and board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + i][3 * (new_move[2]/3)] == ply:
                board.small_boards_status[new_move[0]][(new_move[1]/3)][(new_move[2]/3)] = ply
                return True
            if board.big_boards_status[new_move[0]][3 * (new_move[1]/3)][3 * (new_move[2]/3) + i] == board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + 1][3 * (new_move[2]/3) + i] == board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + 2][3 * (new_move[2]/3) + i] and board.big_boards_status[new_move[0]][3 * (new_move[1]/3)][3 * (new_move[2]/3) + i] == ply:
                board.small_boards_status[new_move[0]][(new_move[1]/3)][(new_move[2]/3)] = ply
                return True

        if board.big_boards_status[new_move[0]][3 * (new_move[1]/3)][3 * (new_move[2]/3)] == board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + 1][3 * (new_move[2]/3) + 1] == board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + 2][3 * (new_move[2]/3) + 2] and board.big_boards_status[new_move[0]][3 * (new_move[1]/3)][3 * (new_move[2]/3)] == ply:
            board.small_boards_status[new_move[0]][(new_move[1]/3)][(new_move[2]/3)] = ply
            return True
        if board.big_boards_status[new_move[0]][3 * (new_move[1]/3)][3 * (new_move[2]/3) + 2] == board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + 1][3 * (new_move[2]/3) + 1] == board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + 2][3 * (new_move[2]/3)] and board.big_boards_status[new_move[0]][3 * (new_move[1]/3)][3 * (new_move[2]/3) + 2] == ply:
            board.small_boards_status[new_move[0]][(new_move[1]/3)][(new_move[2]/3)] = ply
            return True
        for i in range(3):
            for j in range(3):
                if board.big_boards_status[new_move[0]][3 * (new_move[1]/3) + i][3 * (new_move[2]/3) + j] == '-':
                    return False

        board.small_boards_status[new_move[0]][(new_move[1]/3)][(new_move[2]/3)] = 'd'
        return False


    def block_score(self, board, board_num, block_num, ply):

        if board.small_boards_status[board_num][(block_num/3)][(block_num%3)] == ply:
            return self.score_block
        if board.small_boards_status[board_num][(block_num/3)][(block_num%3)] == self.opposite_flag(ply) or board.small_boards_status[board_num][(block_num/3)][(block_num%3)] == 'd':
            return 0

        def convert2num(flag):
            if flag == ply:
                return 1
            elif flag == '-':
                return 0
            else:
                return -2


        lines = []


        for pattern in self.patterns_X_Y:
            value = convert2num(board.big_boards_status[board_num][3 * (block_num/3) + pattern[0][0]][3 * (block_num%3) + pattern[0][1]]) + convert2num(board.big_boards_status[board_num][3 * (block_num/3)+pattern[1][0]][3 * (block_num%3) + pattern[1][1]]) + convert2num(board.big_boards_status[board_num][3 * (block_num/3)+pattern[2][0]][3 * (block_num%3) + pattern[2][1]])
            lines.append(value)
     

        two_attacks = 0
        one_attacks = 0
        for i in xrange(0,8):
            if lines[i] == 1:
                two_attacks += 1
            elif lines[i] == 2:
                one_attacks += 1

        my_block_score = self.oneattc * one_attacks + self.twoattc * two_attacks
        if ply == self.int_to_flag(self.my_flag_int):
            self.mvgavg = (self.size * self.mvgavg + my_block_score) / (self.size + 1)
            self.size += 1
        return my_block_score

    def game_score(self, board, board_num, ply):
        my_block = [0 for i in range(9)]
        line_score = 0

        for i in range(9):
            my_block[i] = self.block_score(board, board_num, i , ply)
        for pattern in self.patterns:
            line_score += my_block[pattern[0]] * my_block[pattern[1]]* my_block[pattern[2]]
        return line_score

    def heuristic(self, board):
        my_attack_score = 0
        opp_attack_score = 0
        wght_matrix = [4,6,4,6,3,6,4,6,4,0]
        for i in range(8):
            my_attack_score += wght_matrix[i] * ((self.block_score(board, 0, i, self.int_to_flag(self.my_flag_int)) + self.block_score(board, 1, i, self.int_to_flag(self.my_flag_int))))
            opp_attack_score += wght_matrix[i] * ((self.block_score(board, 0, i, self.int_to_flag(self.my_flag_int -1)) + self.block_score(board, 1, i, self.int_to_flag(self.my_flag_int -1))))

       
        my_game_score = self.game_score(board, 0, self.int_to_flag(self.my_flag_int)) + self.game_score(board, 1, self.int_to_flag(self.my_flag_int -1))
        opp_game_score = self.game_score(board, 0, self.int_to_flag(self.my_flag_int -1)) + self.game_score(board, 1, self.int_to_flag(self.my_flag_int -1))
        h = self.attack_weight * (my_attack_score - opp_attack_score) + self.game_weight * (my_game_score - opp_game_score)
        return h

    def eval(self, board, terminal_check):
        priorities = [terminal_check[1] == 'WON', terminal_check[0] == self.int_to_flag(self.my_flag_int), terminal_check[1] == 'DRAW']
        if priorities[0]:
            if priorities[1]:
                return self.win_utility
            return self.lose_utility
        else:
            if priorities[2]:
                return self.draw_utility
        ret = self.heuristic(board)
        return ret

    def max_value(self, board, alpha, beta, depth, old_move, bonus):
        terminal_check = board.find_terminal_state()
        priorities = [terminal_check[0] != 'CONTINUE' or depth == 0]
        if priorities[0]:
            opt = self.eval(board, terminal_check)
            return (opt, (-1, -1, -1))
        best_utility = -999999999
        best_action =  (-6,-6,-6)
        for action in board.find_valid_move_cells(old_move):
            cur_time = time()
            time_taken = cur_time - self.start_time
            bogus = (-999999999, (-1, -1, -1))
            if time_taken >= 22:
                return bogus
            if self.update(board, old_move, action, self.int_to_flag(self.my_flag_int)) and not bonus:
                utility, _ = self.max_value(board, alpha, beta, depth - 1, action, True)
            else:
                utility, _ = self.min_value(board, alpha, beta, depth - 1, action, False)
            if utility == -999999999:
                bogus = (utility, (-1, -1, -1))
                return bogus
            board.big_boards_status[action[0]][action[1]][action[2]] = '-'
            board.small_boards_status[action[0]][action[1] / 3][action[2] / 3] = '-'
            if utility > best_utility:
                best_utility = utility
                best_action = action
            if best_utility >= beta:
                opt = (best_utility, best_action)
                return opt 
            alpha = max(alpha, best_utility)
        opt = (best_utility, best_action)
        return opt

    def min_value(self, board, alpha, beta, depth, old_move, bonus):
        terminal_check = board.find_terminal_state()
        priorities = [terminal_check[0] != 'CONTINUE' or depth == 0]
        if priorities[0]:
            return (self.eval(board, terminal_check), (-1, -1, -1))
        best_utility = 999999999
        best_action = (-6,-6,-6)
        for action in board.find_valid_move_cells(old_move):
            cur_time = time()
            time_taken = cur_time - self.start_time
            bogus = (-999999999, (-1, -1, -1))
            if time_taken >= 22:
                return bogus
            if self.update(board, old_move, action, self.int_to_flag(self.my_flag_int -1)) and not bonus:
                utility, _ = self.min_value(board, alpha, beta, depth - 1, action, True)
            else:
                utility, _ = self.max_value(board, alpha, beta, depth - 1, action, False)
            if utility == -999999999:
                bogus = (utility, (-1, -1, -1))
                return bogus
            board.big_boards_status[action[0]][action[1]][action[2]] = '-'
            board.small_boards_status[action[0]][action[1] / 3][action[2] / 3] = '-'
            if best_utility > utility:
                best_utility = utility
                best_action = action
            if best_utility <= alpha:
                opt = (best_utility, best_action)
                return opt
            beta = min(beta, best_utility)
        opt = (best_utility, best_action)
        return opt

    def alpha_beta_search(self, board, depth, old_move):
        p = [board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == self.int_to_flag(self.my_flag_int)]
        if p[0]:
            utility, action = self.max_value(board, -999999999, 999999999, depth, old_move, True)
        else:
            utility, action = self.max_value(board, -999999999, 999999999, depth, old_move, False)
        opt = (utility, action)
        return opt

    def move(self, board, old_move, flag):
        self.start_time = time()
        self.my_flag_int = self.flag_to_int(flag)
        board_copy = deepcopy(board)
        best_action = (-6,-6,-6)
        best_utility = -999999999
        depth = 3
        while True:
            utility, action = self.alpha_beta_search(board_copy, depth, old_move)
            if utility == -999999999:
                break
            else:
                if utility > best_utility:
                    best_action = action
                    best_utility = utility
            depth += 1

        return best_action
