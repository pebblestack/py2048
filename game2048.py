import random
import os
import numpy as np
import time
import argparse

def take_input():
    import msvcrt
    ch = msvcrt.getch()
    return chr(ch[0])

def game_board(game_size):
    game = np.zeros((game_size,game_size), dtype = np.int)
    return game

def show_game(current_game):
    for row in current_game:
        print('\t', end = '  ')
        for item in row:
            if item != 0:
                print(item, end='    ')
            else:
                print('-', end='    ')
        print("\n")
    print('\t', '*****'*len(current_game), end='    ')
    print(f"Winning tile: {win_tile}", end='\n')

def swipe_up(current_game, store_game):
    store_game = current_game
    clean_board = game_board(len(current_game))
    for col in range(len(current_game)):
        new_row = 0
        for row in range(len(current_game)):
            if current_game[row][col] != 0:
                clean_board[new_row][col] = current_game[row][col]
                new_row += 1
    current_game = clean_board
    clean_board = game_board(len(current_game))
    for col in range(len(current_game)):
        for row in range(len(current_game)-1):
            if current_game[row][col] == current_game[row+1][col]:
                current_game[row][col] = current_game[row][col] * 2
                current_game[row+1][col] = 0
        new_row = 0
        for row in range(len(current_game)):
            if current_game[row][col] != 0:
                clean_board[new_row][col] = current_game[row][col]
                new_row += 1
    current_game = clean_board    
    
    return current_game, store_game

def swipe_down(current_game, store_game):
    store_game = current_game
    clean_board = game_board(len(current_game))
    for col in range(len(current_game)):
        new_row = len(current_game)-1
        for row in reversed(range(len(current_game))):
            if current_game[row][col] != 0:
                clean_board[new_row][col] = current_game[row][col]
                new_row -= 1
    current_game = clean_board
    clean_board = game_board(len(current_game))
    for col in range(len(current_game)):
        for row in reversed(range(1,len(current_game))):
            if current_game[row][col] == current_game[row-1][col]:
                current_game[row][col] = current_game[row][col] * 2
                current_game[row-1][col] = 0
        new_row = len(current_game)-1
        for row in reversed(range(len(current_game))):
            if current_game[row][col] != 0:
                clean_board[new_row][col] = current_game[row][col]
                new_row -= 1
    current_game = clean_board    
    
    return current_game, store_game

def swipe_right(current_game, store_game):
    store_game = current_game
    clean_board = game_board(len(current_game))
    for row in range(len(current_game)):
        new_col = len(current_game) - 1
        for col in reversed(range(len(current_game))):
            if current_game[row][col] != 0:
                clean_board[row][new_col] = current_game[row][col]
                new_col -= 1
    current_game = clean_board
    clean_board = game_board(len(current_game))
    for row in range(len(current_game)):
        for col in reversed(range(1, len(current_game))):
            if current_game[row][col] == current_game[row][col-1]:
                current_game[row][col] = current_game[row][col] * 2
                current_game[row][col-1] = 0
        new_col = len(current_game) - 1
        for col in reversed(range(len(current_game))):
            if current_game[row][col] != 0:
                clean_board[row][new_col] = current_game[row][col]
                new_col -= 1
    current_game = clean_board    
    
    return current_game, store_game

def swipe_left(current_game, store_game):
    store_game = current_game
    clean_board = game_board(len(current_game))
    for row in range(len(current_game)):
        new_col = 0
        for col in range(len(current_game)):
            if current_game[row][col] != 0:
                clean_board[row][new_col] = current_game[row][col]
                new_col += 1
    current_game = clean_board
    clean_board = game_board(len(current_game))
    for row in range(len(current_game)):
        for col in range(len(current_game)-1):
            if current_game[row][col] == current_game[row][col+1]:
                current_game[row][col] = current_game[row][col] * 2
                current_game[row][col+1] = 0
        new_col = 0
        for col in range(len(current_game)):
            if current_game[row][col] != 0:
                clean_board[row][new_col] = current_game[row][col]
                new_col += 1
    current_game = clean_board    
    
    return current_game, store_game

def check_win(current_game):
    count1 = 0
    for col in range(len(current_game)):
        for row in range(len(current_game)):
            if current_game[row][col] == 0:
                count1 +=1
    if count1 == 0:
        count2 = 0
        for col in range(len(current_game)):
            for row in range(len(current_game)):
                if current_game[row][col] == win_tile:
                    count2 +=1
        if count2 > 0:
            return False, True, True
        elif count2 == 0:
            count3 = 0
            for col in range(len(current_game)):
                for row in range(len(current_game)-1):
                    if current_game[row][col] == current_game[row+1][col]:
                        count3 +=1
            for row in range(len(current_game)):
                for col in range(len(current_game)-1):
                    if current_game[row][col] == current_game[row][col+1]:
                        count3 +=1
            if count3 >0:
                return True, False, False
            elif count3 == 0:
                return False, True, False
    elif count1 >0:
        count2 = 0
        for col in range(len(current_game)):
            for row in range(len(current_game)):
                if current_game[row][col] == win_tile:
                    count2 +=1
        if count2 >0:
            return False, True, True
        elif count2 == 0:
            return True, False, False

os.system("cls")

try:
    num_of_moves = 0
    print("The Game Is Starting...")
    print("Swipe in different directions using w,a,s or d keys or use u key to undo a move.")
    parser = argparse.ArgumentParser(description='Input for game size and winning tile size')
    parser.add_argument('-n', '--board_size', metavar='', help='Choose your game size')
    parser.add_argument('-w', '--max_tile', help='Choose your winning tile size', metavar='')
    parser.add_argument('-q', '--quiet', help='print quiet', action='store_true')
    args = parser.parse_args()

    try:
        if args.board_size.isnumeric():
            game_size = int(args.board_size)
            if game_size < 1:
                game_size = 5
        else:
            game_size = 5
    except:
        game_size = 5
    try:
        if args.max_tile.isnumeric():
            win_tile = int(args.max_tile)
            if win_tile < 1:
                win_tile = 2048
        else:
            win_tile = 2048
    except:
        win_tile = 2048
    
    os.system('cls')
    start = time.time()

    game = game_board(game_size)
    play = True
    game_over = False
    you_win = False
    game[random.randint(0, len(game)-1)][random.randint(0, len(game)-1)] = 2
    store_game = game
    move = 'o'
    while play:

        play, game_over, you_win = check_win(game)
        if game_over and not you_win:
            play = False
            show_game(game)
            print('')
            if not args.quiet:
                print("Total number of moves made: ", num_of_moves)
                print(f"Total time taken is {int(time.time() - start)} seconds")
            print("Sorry, You Loose")
        elif game_over and you_win:
            play = False
            show_game(game)
            print('')
            if not args.quiet:
                print("Total number of moves made: ", num_of_moves)
                print(f"Total time taken is {int(time.time() - start)} seconds")
            print("Congratulations, You Win")
            
        if play:
            os.system('cls')
            show_game(game)
            
            invalid_move = True
            while invalid_move:
                move = take_input()
                
                if move.lower() == 'w':
                    num_of_moves += 1
                    invalid_move = False
                    game, store_game = swipe_up(game, store_game)
                    
                elif move.lower() == 's':
                    num_of_moves += 1
                    invalid_move = False
                    game, store_game = swipe_down(game, store_game)
                    
                elif move.lower() == 'a':
                    num_of_moves += 1
                    invalid_move = False
                    game, store_game = swipe_left(game, store_game)
                    
                elif move.lower() == 'd':
                    num_of_moves += 1
                    invalid_move = False
                    game, store_game = swipe_right(game, store_game)
                
                elif move.lower() == 'u':
                    game = store_game
                    invalid_move = False

                elif move.lower() == 'z':
                    play = False
                    break
                    
                else:
                    print("Invalid move, try again!", end='    ')
                    invalid_move = True

                comparison = game == store_game
                equal_arrays = comparison.all() 
                if move.lower() != 'u' and equal_arrays:
                    print("Warning!! Move in that direction not possible, try again!")
                    invalid_move = True

            if move.lower() != 'u':
                get = True
                while get:
                    rand_row = random.randint(0,len(game)-1)
                    rand_col = random.randint(0,len(game)-1)
                    num = game[rand_row][rand_col]
                    if num == 0:
                        game[rand_row][rand_col] = 2
                        get = False
    
    print("Game Over, Byeeeee")

            
except Exception as e:
    print("Something went wrong!", e)
    play = True



