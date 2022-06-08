import time

import reversi


def run():
    board = None
    count_A_wins = 0
    # try:
    black, white = reversi.minimax_searcher(3, reversi.f_weighted_score_randomised), \
                   reversi.minimax_searcher(3, reversi.weighted_score)

    # for i in range(0, 50):
    start_time = time.time()
    board, score = reversi.play(black, white)
    # if score > 0 :
    #      count_A_wins +=1
    #      print(" blakc wins" , count_A_wins)
    # print( "no of  Black wins: " ,  count_A_wins)
    # print("Quality of the startegy : " , count_A_wins/50)

    print("time execution of the game", time.time() - start_time)
    print("Black wins " if score > 0 else "White wins")
    print(score)
    print(reversi.print_board(board))
    # except reversi.IllegalMoveError as e:
    #     print(e)
    #     return
    # except EOFError as e:
    #     print('Goodbye.')
    #     return
    # print('%s wins!' % ('Black' if score > 0 else 'White'))


def run_quality():
    count_A_wins = 0

    for i in range(0, 50):
        black, white = reversi.alphabeta_searcher(3, reversi.weighted_score), \
                       reversi.minimax_searcher(3, reversi.weighted_score)
        board, score = reversi.play(black, white)
        if score > 0:
            count_A_wins += 1
            print(" blakc wins", count_A_wins)
        elif score < 0:
            print("white wins")
        else:
            print("draw")

    print("Quality of the startegy : ", count_A_wins / 50)
    print(reversi.print_board(board))


if __name__ == '__main__':
    #run()
    run_quality()
