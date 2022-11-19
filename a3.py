#

import random
from enum import Enum


# enum of position status with EMPTY, X(Player1), or O(Player2)
class element(Enum):
    EMPTY = 1
    X = 2
    O = 3


class win_lost_tie(Enum):
    WIN = 1
    LOSE = 2
    TIE = 3


# initial map
def creat_map():
    map = [[element.EMPTY, element.EMPTY, element.EMPTY], [element.EMPTY, element.EMPTY, element.EMPTY],
           [element.EMPTY, element.EMPTY, element.EMPTY]]
    return map


# make a map copy for search tree
def copy_map(map):
    new_map = [[map[0][0], map[0][1], map[0][2]], [map[1][0], map[1][1], map[1][2]], [map[2][0], map[2][1], map[2][2]]]
    return new_map


# print game on terminal
def print_map(map):
    for i in range(8):
        for j in range(8):
            if i == 0:
                if j == 2:
                    print("0", end='')
                elif j == 4:
                    print("1", end='')
                elif j == 6:
                    print("2", end='')
                else:
                    print(" ", end='')
            elif j == 0:
                if i == 2:
                    print("0", end='')
                elif i == 4:
                    print("1", end='')
                elif i == 6:
                    print("2", end='')
                else:
                    print(" ", end='')
            else:
                if i % 2 == 1:
                    print('-', end='')
                elif j % 2 == 1:
                    print('|', end='')
                else:
                    if map[int(i / 3)][int(j / 3)] == element.EMPTY:
                        print(" ", end='')
                    elif map[int(i / 3)][int(j / 3)] == element.X:
                        print("X", end='')
                    else:
                        print("O", end='')
        print()


# if position is empty, put player symbol on that position
def make_a_move(map, row, col, player: element):
    if map[row][col] == element.EMPTY:
        map[row][col] = player


# true is row win
def check_row(map):
    for i in range(3):
        if map[i][1] != element.EMPTY and map[i][1] == map[i][2] == map[i][0]:
            return True
    return False


# true is col win
def check_col(map):
    for i in range(3):
        if map[1][i] != element.EMPTY and map[1][i] == map[2][i] == map[0][i]:
            return True
    return False


# true is diagonal win
def check_diagonal(map):
    if map[1][1] != element.EMPTY:
        if map[1][1] == map[2][2] == map[0][0]:
            return True
        elif map[1][1] == map[0][2] == map[2][0]:
            return True
    else:
        return False


# true is game win
def check_win(map):
    if check_row(map) or check_col(map) or check_diagonal(map):
        return True
    else:
        return False


# true if game tie
def check_tie(map):
    for i in range(3):
        for j in range(3):
            if map[i][j] == element.EMPTY:
                return False
    return True


# return a list which save all possible position is empty
def get_possible_move(map):
    possible_move = []
    for i in range(3):
        for j in range(3):
            if map[i][j] == element.EMPTY:
                possible_move.append([i, j])
    return possible_move


# once time simulation
def random_playouts(map, row, col, AI: element):
    if (AI == element.X):
        Player = element.O
    else:
        Player = element.X

    new_map = copy_map(map)
    # make move on select position
    make_a_move(new_map, row, col, AI)
    if check_win(new_map) == True:
        one_step = True
        game_status = win_lost_tie.WIN
    elif check_tie(map):
        one_step = False
        game_status = win_lost_tie.TIE
    else:
        one_step = False
        game_status = win_lost_tie.LOSE
    # random play
    while check_tie(new_map) == False and check_win(new_map) == False:
        possible_move = get_possible_move(new_map)
        next_move = random.choice(possible_move)
        make_a_move(new_map, next_move[0], next_move[1], Player)
        # only change to False when Player win
        if check_win(new_map) == True:
            game_status = win_lost_tie.LOSE
            break
        if check_tie(new_map) == True:
            game_status = win_lost_tie.TIE
            break
        possible_move = get_possible_move(new_map)
        next_move = random.choice(possible_move)
        make_a_move(new_map, next_move[0], next_move[1], AI)
        if check_win(new_map) == True:
            game_status = win_lost_tie.WIN
            break
        if check_tie(new_map) == True:
            game_status = win_lost_tie.TIE
            break

    return game_status, one_step


# pure Monte Carlo Tree Search (pMCTS)
def pMCTS(map, AI: element):
    possible_move = get_possible_move(map)
    lose_time = 2000
    row = -1
    col = -1
    one_move = False
    for each in possible_move:
        # count current lose time
        current_lose = 0
        # number of times random playouts
        if len(possible_move) >= 8:
            r = 1000
        elif len(possible_move) >= 6:
            r = 3000
        elif len(possible_move) >= 4:
            r = 1000
        else:
            r = 100  # not much choices left
        for i in range(r):
            game_status, one_step = random_playouts(map, each[0], each[1], AI)
            # record lose time
            if game_status == win_lost_tie.LOSE:
                current_lose = current_lose + 1
            # only need one step can win
            if game_status == win_lost_tie.WIN and one_step == True:
                one_move = True
                break
        # print(current_lose, each)
        # only need one step can win
        if one_move:
            row = each[0]
            col = each[1]
            break
        # select least number of lose
        if current_lose < lose_time:
            lose_time = current_lose
            # save row and col position
            row = each[0]
            col = each[1]
    return row, col


def play_a_new_game():
    map = creat_map()
    print("Fisrt: X\nSecond: O\nVaild input are integer between 0 to 2 (0, 1, 2)")
    user = input("If you type X or x you will go first, other AI will go first")
    if user.lower() == 'x':
        # Player is X, AI is O
        Player = element.X
        AI = element.O
        print_map(map)
        while check_tie(map) == False and check_win(map) == False:
            print("\nPlayer round")
            print("vaild moves are")
            print(get_possible_move(map))
            # make sure player input is vaild
            while True:
                row = input("please select row")
                col = input("please select col")
                try:
                    row = int(row)
                    col = int(col)
                except:
                    print("must be integer")
                if 0 <= row <= 2 and 0 <= col <= 2:
                    if map[row][col] != element.EMPTY:
                        print("already choose")
                        continue
                    break
                else:
                    print("row and col need to between 0 and 2")
                    continue
            # put player symbol on select position
            make_a_move(map, row, col, Player)
            print_map(map)
            if check_tie(map) == True:
                print("Tie game")
                break
            elif check_win(map) == True:
                print("Player win")
                break

            print("\nAI round")
            # get position based on pMCTS
            row, col = pMCTS(map, AI)
            # put AI symbol on select position
            make_a_move(map, row, col, AI)
            print("AI select ", [row, col])
            print_map(map)
            if check_tie(map) == True:
                print("Tie game")
            elif check_win(map) == True:
                print("AI win")
    else:
        # AI is X, Player is O
        Player = element.O
        AI = element.X
        print_map(map)
        while check_tie(map) == False and check_win(map) == False:
            print("\nAI round")
            # get position based on pMCTS
            row, col = pMCTS(map, AI)
            # put AI symbol on select position
            make_a_move(map, row, col, AI)
            print("AI select ", [row, col])
            print_map(map)
            if check_tie(map) == True:
                print("Tie game")
                break
            elif check_win(map) == True:
                print("AI win")
                break

            print("\nPlayer round")
            print("vaild moves are")
            print(get_possible_move(map))
            # make sure player input is vaild
            while True:
                row = input("please select row")
                col = input("please select col")
                try:
                    row = int(row)
                    col = int(col)
                except:
                    print("must be integer")
                if 0 <= row <= 2 and 0 <= col <= 2:
                    if map[row][col] != element.EMPTY:
                        print("already choose")
                        continue
                    break
                else:
                    continue
            # put player symbol on select position
            make_a_move(map, row, col, Player)
            print_map(map)
            if check_tie(map) == True:
                print("Tie game")
                break
            elif check_win(map) == True:
                print("Player win")
                break

    '''
    # Let AI play with AI

    map = creat_map()
    print("Player: X\nAI: O")
    AI1 = element.X
    AI2 = element.O
    print_map(map)
    while check_tie(map) == False and check_win(map) == False:
        print("\nAI1 round")
        row, col = pMCTS(map, AI1)
        make_a_move(map, row, col, AI1)
        print_map(map)
        if check_tie(map) == True:
            print("Tie game")
            break
        elif check_win(map) == True:
            print("AI1 win")
            break
        print("\nAI2 round")
        row, col = pMCTS(map, AI2)
        make_a_move(map, row, col, AI2)
        print_map(map)
        if check_tie(map) == True:
            print("Tie game")
        elif check_win(map) == True:
            print("AI2 win")
    '''


if __name__ == '__main__':
    play_a_new_game()
