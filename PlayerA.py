import copy
import random
import sys
import time
import math
import matplotlib.pyplot as plt

# Nassim Maluli
# we implement the MiniMax algorithm + alpha-Beta pruning
if (len(sys.argv) < 3):
    print("PlayerA.py STATEFILE MOVEFILE")
    sys.exit()


########################################################################################################################
# dedicated for the check_methods
# test if there is n-coins in down-direction starting from x,y
def test_PositionDown(state, n, x, y):
    player = state[x][y]
    maxX = len(state)
    maxY = len(state[0])
    if (y > maxY - n):
        return ''
    for ny in range(y + 1, y + n):
        if (player != state[x][ny]):
            return ''
    # if we are checking the 5-coin streak it means we are checking that the player has won
    if n == 5:
        return player
    if y > 0:
        if state[x][y - 1] == 'e':
            return player
    return ''


# test if there is n-coins in right-direction starting from x,y
def test_PositionRight(state, n, x, y):
    # blocked 2 means we look at two sides

    player = state[x][y]
    maxX = len(state)
    maxY = len(state[0])
    if x > maxX - n:
        return ''
    for nx in range(x + 1, x + n):
        if player != state[nx][y]:
            return ''
    # if we are checking the 5-coin streak it means we are checking that the player has won
    if n == 5:
        return player
    # the next two conditions are there to check if the n-streak is blocked or not
    if x > 0:
        if state[x - 1][y] == 'e':
            return player
    if x + n <= maxX - 1:
        if state[x + n][y] == 'e':
            return player
    return ''


# test if there is n-coins down-right-diagonal starting from x,y
def test_PositionDownRight(state, n, x, y):
    player = state[x][y]
    maxX = len(state)
    maxY = len(state[0])
    if (x > maxX - n or y > maxY - n):
        return ''
    ny = y + 1;
    for nx in range(x + 1, x + n):
        if player != state[nx][ny]:
            return ''
        ny = ny + 1
    # if we are checking the 5-coin streak it means we are checking that the player has won
    if n == 5:
        return player
    # the next two conditions are there to check if the n-streak is blocked or not
    if x > 0 and y > 0:
        if state[x - 1][y - 1] == 'e':
            return player
    if x + n <= maxX - 1 and y + n <= maxY - 1:
        if state[x + n][y + n] == 'e':
            return player
    return ''


# test if there is n-coins up-right-diagonal starting from x,y
def test_PositionUpRight(state, n, x, y):
    player = state[x][y]
    maxX = len(state)
    maxY = len(state[0])
    if x > maxX - n or y < (n - 1):
        return ''
    ny = y - 1;
    for nx in range(x + 1, x + n):
        if player != state[nx][ny]:
            return ''
        ny = ny - 1
    # if we are checking the 5-coin streak it means we are checking that the player has won
    if n == 5:
        return player

    # the next two conditions are there to check if the n-streak is blocked or not
    if x > 0 and y < maxY - 1:
        if state[x - 1][y + 1] != 'e':
            return ''
    if x + n <= maxX - 1 and y >= n:
        if state[x + n][y - n] == 'e':
            return player
    return ''


# test if there is n-coins starting from a given x,y
def test_Position(state, n, x, y):
    player = state[x][y]
    # x=0,y=0 is upper left corner
    maxX = len(state)
    maxY = len(state[0])
    if (player == 'e'):
        return ''
    if (test_PositionDown(state, n, x, y) != ''):
        return player
    if (test_PositionRight(state, n, x, y) != ''):
        return player
    if (test_PositionDownRight(state, n, x, y) != ''):
        return player
    if (test_PositionUpRight(state, n, x, y) != ''):
        return player
    return ''


# Flips the board
def flip(state):
    oldState = [['e' for y in range(8)] for x in range(11)]
    for y in range(len(state[0])):
        for x in range(len(state)):
            oldState[x][y] = state[x][y]
            state[x][y] = 'e'
    for x in range(len(state)):
        flag = False
        yPos = len(state[0]) - 1;
        for y in range(len(state[0])):
            if (oldState[x][y] != 'e'):
                flag = True
            if (flag == True):
                state[x][yPos] = oldState[x][y]
                yPos = yPos - 1
    return True


########################################################################################################################

def check_fours(state):
    player = ''
    players = []
    for x in range(len(state)):
        for y in range(len(state[0])):
            player = test_Position(state, 4, x, y)
            if player != '':
                players.append(player)

    return players


def check_threes(state):
    player = ''
    players = []
    for x in range(len(state)):
        for y in range(len(state[0])):
            player = test_Position(state, 3, x, y)
            if player != '':
                players.append(player)

    return players


def check_twos(state):
    player = ''
    players = []
    for x in range(len(state)):
        for y in range(len(state[0])):
            player = test_Position(state, 2, x, y)
            if player != '':
                players.append(player)

    return players


########################################################################################################################

# Test is somebody has one, by testing each position
def hasWon(state):
    player = ''
    for x in range(len(state)):
        for y in range(len(state[0])):
            player = test_Position(state, 5, x, y)
            if player != '':
                return player
    return ''


# Test if there is a draw in the game
def isDraw(state):
    for x in range(len(state)):
        for y in range(len(state[0])):
            if (state[x][y] == 'e'):
                return False
    print("Draw Game")
    return True


########################################################################################################################
# This function represent the evaluation function
def eval(state):
    # returns a definitive value of +1000 / -1000 to assert win or loss
    if hasWon(state) == 'A':
        return 1000
    if hasWon(state) == 'B':
        return -1000

    # This section checks for "unblocked" 2s , 3s and 4s in a row (for A and B) and assigns proper values
    evaluation = 0

    if 'A' in check_fours(state):
        f4 = check_fours(state).count('A')
        evaluation = evaluation + (50 * f4)

    if 'B' in check_fours(state):
        f3 = check_fours(state).count('B')
        evaluation = evaluation - (50 * f3)

    if 'A' in check_threes(state):
        f2 = check_threes(state).count('A')
        evaluation = evaluation + (25 * f2)

    if 'B' in check_threes(state):
        f1 = check_threes(state).count('B')
        evaluation = evaluation - (25 * f1)

    # The 2s streak was added to incentivize the AI in shallow depth depth <= 4-5
    if 'A' in check_twos(state):
        fn = check_twos(state).count('A')
        evaluation = evaluation + (10 * fn)

    return evaluation


########################################################################################################################
# tests to see if a state is terminal
def test_terminal(s):
    return hasWon(s) != '' or isDraw(s)


# checks if droping a coin in a specific position is possible
def is_legal_action(state, a):
    if a < 0 or a > 11:
        return False
    if a == 11:
        return True
    if state[a][0] == 'e':
        return True
    return False


# a modified add_coin function to apply the transition model for a state and an action - for a particular player
def result(state, pos, player):
    rs = copy.deepcopy(state)

    if (pos < 0):
        print("E1: Not allowed move by " + str(player) + " at position " + str(pos))
        return None
    if (pos >= len(rs)):
        print("E2: Not allowed move by " + str(player) + " at position " + str(pos))
        return None
    if (rs[pos][0] != 'e'):
        print("E3: Not allowed move by " + str(player) + " at position " + str(pos) + " since board was full")
        return None

    if pos == 11:
        return flip(rs)

    for y in range(len(rs[pos]) - 1, -1, -1):
        if (rs[pos][y] == 'e'):
            rs[pos][y] = player
            return rs

    print("Not allowed move by " + str(player))
    return None


########################################################################################################################
# to read the state space for player A
# Read State-File to disk
def readStateSpace(filename):
    state = [['e' for y in range(8)] for x in range(11)]
    f = open(filename, "r")
    bflag = False
    nY = 0;
    for line in f:
        if bflag == True:
            nX = 0
            for c in line:
                if (nX < len(state)):
                    state[nX][nY] = c
                nX = nX + 1
            nY = nY + 1
        if (line.find("Current-State") != -1):
            bflag = True
    f.close()
    return state


########################################################################################################################
# The minimax algorithm with alpha-Beta pruning (Alpha-beta Search)
def alpha_beta_search(state):
    v = max_value(state, 5, -math.inf, math.inf)
    print('Evaluation of the best State == ' + str(v[1]))
    return v[0]


# This returns a pair of [action,maximum value]
def max_value(state, depth, alpha, beta):
    if test_terminal(state) or depth == 0:
        return [None, eval(state)]

    v = [15, -math.inf]

    for a in range(0, 11):
        if is_legal_action(state, a):

            rs = result(state, a, 'A')
            mv = min_value(rs, depth - 1, alpha, beta)

            if mv[1] > v[1]:
                v[1] = mv[1]
                v[0] = a
            if v[1] >= beta:
                return v
            alpha = max(alpha, v[1])

    return v


# This returns a pair of [action,minimum value]
def min_value(state, depth, alpha, beta):
    if test_terminal(state) or depth == 0:
        return [None, eval(state)]

    v = [15, math.inf]

    for a in range(0, 11):
        if is_legal_action(state, a):

            rs = result(state, a, 'B')
            mv = max_value(rs, depth - 1, alpha, beta)

            if mv[1] < v[1]:
                v[1] = mv[1]
                v[0] = a
            if v[1] <= alpha:
                return v
            beta = min(beta, v[1])

    return v


########################################################################################################################
# Graphics
def drawState(state):
    global fig
    global ax

    fig, ax = plt.subplots()
    ax.cla()
    circle = plt.Circle((6, 5), 40, color='b')
    ax.add_artist(circle)
    plt.draw()
    for y in range(len(state[0])):
        for x in range(len(state)):
            scol = 'w'
            if (state[x][y] == 'A'):
                scol = 'r'
            if (state[x][y] == 'B'):
                scol = 'y'
            circle1 = plt.Circle((x + 1, len(state[0]) - y), 0.4, color=scol)
            ax.add_artist(circle1)
    plt.axis([0, 12, 0, 10])
    fig.savefig('5GewinntState.png')
    plt.show()
    plt.pause(0.001)


########################################################################################################################
# Print State on Screen
def printState(state):
    print("State that playerA evaluates")
    for y in range(len(state[0])):
        for x in range(len(state)):
            c = '.'
            if (state[x][y] != 'e'):
                c = state[x][y]
            print(c, end="")
        print('')


########################################################################################################################
# program playerA
main_state = readStateSpace(sys.argv[1])
move = str(alpha_beta_search(main_state) + 1)
plt.ion()
drawState(main_state)

print('The advised move is == ' + move)
if move == '12':
    move = 'flip'

f = open(sys.argv[2], "w")
f.write(move)
f.close()

time.sleep(1)
########################################################################################################################
