import numpy as np

NUMBER_OF_MOVES = 4

from game_functions import random_move, move_down, move_left, move_right, move_up,add_new_tile

MOVE_INDICES = {
    0: "Left",
    1: "Up",
    2: "Down",
    3: "Right"
}

def ai_move(board, searches_per_move, search_length):
    first_options = [move_left, move_up, move_down, move_right]
    first_move_scores = np.zeros(NUMBER_OF_MOVES)

    #For each of the four options, get an initial score and continue
    for i in range(NUMBER_OF_MOVES):
        first_move_function =  first_options[i]
        board_after_first_move, first_move_valid, first_move_score = first_move_function(board)
        if first_move_valid:
            board_after_first_move = add_new_tile(board_after_first_move)
            first_move_scores[i] += first_move_score
        else:
            continue
        #For searches_per_move, repeat a random traversal of moves all while keeping track of score
        final_scores = np.array([])
        for _ in range(searches_per_move):
            cur_score = 0
            move_number = 1
            search_board = np.copy(board_after_first_move)
            game_valid = True
            while game_valid and move_number < search_length:
                search_board, game_valid, score = random_move(search_board)
                if game_valid:
                    search_board = add_new_tile(search_board)
                    cur_score += score
                    move_number += 1
            final_scores = np.append(final_scores, [cur_score])
        #Get the mean of the top 25% of scores out of all the random moves
        final_scores_index_array = np.argsort(final_scores)
        sorted_final_scores = final_scores[final_scores_index_array]
        mean = np.mean(sorted_final_scores[-len(sorted_final_scores)//4])
        first_move_scores[i] += mean
    #Choose the highest first move score after the traversal
    best_move_index = np.argmax(first_move_scores)
    best_move = first_options[best_move_index]
    search_board, game_valid, score = best_move(board)
    return search_board, game_valid, score



	