import sys
import copy
import random
import time
import Dylans_chess_view
import numpy as np
import multiprocessing
import cProfile, pstats


def main():
    start_time_1 = time.time()
    
    if len(sys.argv)==1:
        print("There has to be atleast one argument")
        sys.exit(2)
    try:
        board_size = int(sys.argv[1])
    except:
        print("argument has to be a number")
    if len(sys.argv)>2:
        print(sys.argv)
        print("Too many arguments")
        sys.exit(2)
    full_board = []
    quit = multiprocessing.Event()
    foundit = multiprocessing.Event()
    
    for i in range(board_size):
        temp_row = []
        for x in range(board_size):
            temp_row.append('.')
    
            
        full_board.append(temp_row)

    board, queens_list = random_board(full_board)
    solution_1 = print_current_try(queens_list)
    print(solution_1)
    beg_time = time.time() - start_time_1
    # Dylans_chess_view.game(len(board),solution_1, complete_move_list(board))
    start_time = time.time()
    
    
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    # multiprocessing.cpu_count()
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=loop, args=(board, return_dict,i,quit,foundit,full_board))
        jobs.append(p)
        p.start()

    foundit.wait()
    quit.set()
    board = return_dict.values()[0]
    queens_list = return_dict.values()[1]
    print("THIS IS THE SOLUTION")
    solution = print_current_try(queens_list)
    

    total_time = (time.time() - start_time) + beg_time

    # Dylans_chess_view.game(len(board),solution, complete_move_list(board), total_time)

def loop(board,return_dict,num,quit,foundit,full_board):
    
    all_tries = []
    count = 0
    num = 1
    queens_list = []
    board,queens_list = random_board(full_board)
    print_current_try(queens_list)

    while not quit.is_set():

        
        start_time = time.time()
        curr_try = print_current_try(queens_list)
        all_tries.append(curr_try)
        if all_tries.count(curr_try)>2:
            board, queens_list = random_board(full_board)
            
            all_tries = []
        
        
        # profiler = cProfile.Profile()
        # profiler.enable()
        # new_queens = [value for i,value in enumerate(queens_list) if check_queen(queens_list,value)!=0]


        # start_time = time.time()

        # new_board = np.array(board)
        # new_queens_list = np.array(queens_list)Python Advanced Topics


        # best = all_available_moves(new_board,new_queens_list)
        best = all_available_moves(board,queens_list)




        # curr_best = evaluation(copy.deepcopy(queens_list))
        # print(queens_list)
        # print(new_queens)
        # best = random_best_avail_queen(board,new_queens,curr_best)
        # print((time.time() - start_time))
        # profiler.disable()
        # stats = pstats.Stats(profiler).sort_stats('tottime')
        # stats.print_stats()
        
        # quit()

     
        count = count + 1
        queens_list = update_queens(best, queens_list)
        board = make_move(board,best)
        # print("--- %s seconds ---" % (time.time() - start_time))

        

        num = num + 1
        if board_solution(board,queens_list) == True:
            return_dict[num] = board
            return_dict["queen"] = queens_list
            foundit.set()
            break

    

def update_queens(move,queens_list):

    queens_list = copy.copy(queens_list)
    for num,queen in enumerate(queens_list):
            moves_1 = move[0].split(",")
            # print(move)
            if queens_list[num][0] == int(moves_1[0]) and queens_list[num][1] == int(moves_1[1]):
                moves_2 = move[1].split(",")
                
                queens_list[num] = (int(moves_2[0]), int(moves_2[1]))
    return queens_list

def board_solution(board,queen):
    for x,value in enumerate(queen):
            if check_queen(queen,(value[0],value[1]))>0:
                return False
    return True
def check_queen(queen, curr_queen):
    
    num = 0
    for value in queen:
        if value[0] == curr_queen[0] and value[1] == curr_queen[1]:
            continue
        elif value[0] == curr_queen[0] or value[1] == curr_queen[1] or curr_queen[0] + curr_queen[1] == value[0] + value[1] or curr_queen[0] -value[0] == curr_queen[1]- value[1]:
            num = num + 1

        
    return num

def make_move(board, move):

    beg = move[0].split(",")
    end = move[1].split(",")
    # print("best")
    # print(move)
    temp_board = board
    temp_board[int(beg[0])][int(beg[1])]= "."
    temp_board[int(end[0])][int(end[1])]= "Q"
    return temp_board
def evaluation(queen):
    eval = 0
    for value in queen:

            eval = eval +  check_queen(queen, (value[0],value[1]))
            

    return eval

def all_available_moves(board,queens_list):

    min_eval = 1000
    min_move = 0
    # print("queens")
    # print(queens_list)
    
    for value in queens_list:
        # print(value)
        # print("board")
        # print(board)
        num = 0
        for place in board:
            # print(board)
            # print(num)
            if num != value[0]:
                move = f'{value[0]},{value[1]}', f'{num},{value[1]}'

                new_queens_list = update_queens(move, queens_list)
                temp_eval = evaluation(new_queens_list)
        
                if temp_eval< min_eval:
                    min_eval = temp_eval
                    min_move = move
            num = num + 1
    return min_move

def random_best_avail_queen(board, queens_list,curr_move):
    min_eval = 1000
    count = 0
    while min_eval>curr_move:
        # print("top")
        # print(min_eval)
        count = count + 1
        min_eval = 1000
        min_move = 0

        value = queens_list[random.randint(0,len(queens_list)-1)]
        for l,place in enumerate(board):
            if l != value[0]:
                move = f'{value[0]},{value[1]}', f'{l},{value[1]}'

                new_queens_list = update_queens(move, queens_list)
                temp_eval = evaluation(new_queens_list)
                # if count >1000:
                #     print("bttom")
                #     print(curr_move)
                #     print(min_eval)
                #     print(temp_eval)
                if temp_eval< min_eval:
                    min_eval = temp_eval
                    min_move = move
    return min_move

def print_board(board):
    num = 0
    for row in board:
        print(f'{num}: {row}')
        num = num + 1
    print("     ", end = "")
    for i, value in enumerate(board):
        if i ==len(board) - 1:
            print("^")
        else:
            print("^", end ="    ")
    print("     ", end = "")
    for i, value in enumerate(board):
        print(i, end ="    ")



def print_current_try(queens_list):
    temp_dict = {}
    print("[", end = " ")
    for n, value in enumerate(queens_list):
            print(value[0], end= " ")
            temp_dict[value[1]] = value[0]
          
    print("]")

    return temp_dict

def random_board(board):
    ran_list = []
    new_board = []
    queens_list =[]
    new_board = copy.deepcopy(board)
    for i, value in enumerate(board):
        ran_list.append(random.randint(0,len(board)-1))

    for i, value in enumerate(ran_list):
        queens_list.append((value,i))

        new_board[value][i] = "Q"
    return new_board, queens_list

def complete_move_list(board):
    final_list = []
    for i, value in enumerate(board):
        for x, value in enumerate(board[i]):
            if board[i][x] == "Q":
                final_list = final_list +  queen_moves(board, (i,x))
    return final_list

def queen_moves(board, curr_queen):
    temp_list = []
    for i, value in enumerate(board):
        for x, value in enumerate(board[i]):
            
            if i == curr_queen[0] and x == curr_queen[1]:
                continue
            elif board[i][x] == "Q" and (i == curr_queen[0] or x == curr_queen[1] or curr_queen[0] + curr_queen[1] == x + i or curr_queen[0] -i == curr_queen[1]- x):
                temp_list.append((True,f'{curr_queen[0]},{curr_queen[1]}', f'{i},{x}') )
            elif i == curr_queen[0] or x == curr_queen[1] or curr_queen[0] + curr_queen[1] == x + i or curr_queen[0] -i == curr_queen[1]- x:
                temp_list.append((False,f'{curr_queen[0]},{curr_queen[1]}', f'{i},{x}') )


    return temp_list


if __name__ == "__main__":
    main()
    



