# Ran Ju   1621899 Autumn 2017
# CSE 415 A5   Option B
# K-In-A-Row

'''
juran94KInARow.py
A K-In-A-Row game agent
Win the game by having k consecutive same element in a line
(in a row, a column, or a diagonal)
'''
import random
import copy
import time

def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    '''record the initial state in this game, return OK'''
    global cur_state
    global k1
    global m
    global n
    global my_side
    global opp_side
    global opp_nickname
    k1 = k
    cur_state = initial_state
    my_side = what_side_I_play
    opp_nickname = opponent_nickname
    m = len(cur_state[0])
    n = len(cur_state[0][0])
    if my_side == 'X':
        opp_side = 'O'
    elif my_side == 'O':
        opp_side = 'X'
    else:
        raise 'what_side_I_play must be X or O.'
    return "OK"


def introduce():
    '''Introduce my agent'''
    introduction = "Hi all, my name is Jay, created by Ran Ju, hew UWID is juran94.I am the smartest geek in the world!"
    return introduction

def nickname():
    '''define the nickname of my agent'''
    return "Jay"

def makeMove(currentState, currentRemark, timeLimit=10000):
    '''function that can make move in this board based on miniMax search'''
    board = currentState[0]
    m = len(board)
    n = len(board[0])
    #create different dialogs based on different situation.
    good_list = ["Fantasy Game!", "I nearly beat you, right?","Awesome."]
    nice_list = ["Good battle! ","Good step, ","Yumm, nice job! ","You know I am the smartest person in the world! "]
    normal_list = ["Nice move...", "Hmmm, something trouble...","I cannot beatable!"]
    start_time = time.time()
    res = miniMax(currentState, timeLimit, start_time, 3)
    newScore = res[0]
    newState = copy.deepcopy(res[1])
    #based on different situation, give different response. My agent is a swagger and rude.
    if newScore > 100 and newScore < -100:
        newMark = random.choice(good_list) + opp_nickname
    elif newScore > 50 or newScore < -50:
        newMark = random.choice(nice_list)+ opp_nickname
    else:
        newMark = random.choice(normal_list)
    curBoard = currentState[0]
    newBoard = newState[0]
    for i in range(m):
        for j in range(n):
            if curBoard[i][j] != newBoard[i][j]:
                break
        else:
            continue
        break
    move = (i, j)
    return [[move,newState],newMark]

def score(state, side):
    '''give a score based on the situation,
    add 10 ^(number of count ) to evaluation score.'''

    board = state[0]
    m = len(board)
    n = len(board[0])
    val = 0
    rowList = []
    colList = []
    diaList = []
    diaList2 = []
    # colum
    for i in range(m):
        colCount = 0
        for j in range(n):
            if board[j][i] == side:
                colCount += 1
                if j == n - 1:
                    colList.append(colCount)
            else:
                if colCount == 0:
                    continue
                else:
                    colList.append(colCount)
                    colCount = 0

    for i in colList:
        val += 10 ** i
    #find how many continuous X or O in every rows
    for i in range(m):
        rowCount = 0
        for j in range(n):
            if board[i][j] == side:
                rowCount += 1
                if j == n-1:
                    rowList.append(rowCount)
            else:
                if rowCount == 0:
                    continue
                else:
                    rowList.append(rowCount)
                    rowCount = 0
    for i in rowList:
        val += 10** (i+1)

    #diagonals
    for i in range(m + n - 1):
        diaCount = 0
        for j in range(max(i - m + 1, 0), min(i+1, n)):
            if board[m - i + j - 1][j] == side:
                diaCount += 1
                if j == n-1:
                    diaList.append(diaCount)
            else:
                if diaCount == 0:
                    continue
                else:
                    diaList.append(diaCount)
                    diaCount = 0

    for i in diaList:
        val += 10 ** i
    #another diagnoal
    for i in range(m + n - 1):
        diaCount = 0
        for j in range(max(i - m + 1, 0), min(i+1, n)):
            if board[i-j][j] == side:
                diaCount += 1
                if j == n-1:
                    diaList2.append(diaCount)
            else:
                if diaCount == 0:
                    continue
                else:
                    diaList2.append(diaCount)
                    diaCount = 0
    for i in diaList2:
        val += 10 ** i
    return val

def staticEval(state):
    '''evaluation each state in their side'''
    my_side = state[1]
    opp_side = changeSide(my_side)
    return score(state, my_side)-score(state,opp_side)

def getMove(state):
    '''find the all states in the next steps can move'''
    board = state[0]
    my_side = state[1]
    moveList = []
    for i in range(m):
        for j in range(n):
            if board[i][j] == ' ':
                new_board = copy.deepcopy(board)
                new_board[i][j] = my_side
                moveList.append([new_board, changeSide(my_side)])
    return moveList

def changeSide(my_side):
    if my_side == 'X':
        return 'O'
    if my_side == 'O':
        return  'X'
    else:
        raise "Error"

def miniMax(state, time_limit, startTime, depth):
    if time.time() - startTime >= time_limit *0.8 :
        return [staticEval(state),state]
    side = state[1]
    newState = []
    if depth == 0 :
        return [staticEval(state), state]
    if side == "X":
        val = -100000
    else:
        val = 100000
    for each in getMove(state):
        res = miniMax(each, time_limit, startTime, depth - 1)
        if my_side == 'X':
            score = -res[0]
        else:
            score = res[0]
        if (side == 'X' and score > val) or(side == 'O' and score < val):
            val = score
            newState = each


    return [val, newState]


# state = \
#               [[['-','O','X',' ','O',' ','-'],
#                 [' ',' ','X',' ','O',' ',' '],
#                 [' ',' ','X',' ','X',' ',' '],
#                 ['O','O','O',' ',' ',' ',' '],
#                 [' ','O','X',' ',' ',' ',' '],
#                 [' ',' ','X',' ',' ',' ',' '],
#                 ['-',' ',' ',' ',' ',' ','-']], "O"]
# print(staticEval(state))
# print(getMove(state))
# print(miniMax(state,1,10,3))
#
# print(makeMove(state, 'win you'))