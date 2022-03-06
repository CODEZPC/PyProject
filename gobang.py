#!python3

tb = {'A1':' ','B1':' ','C1':' ','D1':' ','E1':' ','F1':' ','G1':' ','H1':' ','I1':' ','J1':' ',
    'A2':' ','B2':' ','C2':' ','D2':' ','E2':' ','F2':' ','G2':' ','H2':' ','I2':' ','J2':' ',
    'A3':' ','B3':' ','C3':' ','D3':' ','E3':' ','F3':' ','G3':' ','H3':' ','I3':' ','J3':' ',
    'A4':' ','B4':' ','C4':' ','D4':' ','E4':' ','F4':' ','G4':' ','H4':' ','I4':' ','J4':' ',
    'A5':' ','B5':' ','C5':' ','D5':' ','E5':' ','F5':' ','G5':' ','H5':' ','I5':' ','J5':' ',
    'A6':' ','B6':' ','C6':' ','D6':' ','E6':' ','F6':' ','G6':' ','H6':' ','I6':' ','J6':' ',
    'A7':' ','B7':' ','C7':' ','D7':' ','E7':' ','F7':' ','G7':' ','H7':' ','I7':' ','J7':' ',
    'A8':' ','B8':' ','C8':' ','D8':' ','E8':' ','F8':' ','G8':' ','H8':' ','I8':' ','J8':' ',
    'A9':' ','B9':' ','C9':' ','D9':' ','E9':' ','F9':' ','G9':' ','H9':' ','I9':' ','J9':' ',
    'A10':' ','B10':' ','C10':' ','D10':' ','E10':' ','F10':' ','G10':' ','H10':' ','I10':' ','J10':' '}
alphalist = ['A','B','C','D','E','F','G','H','I','J']

def prboard(board):
    print('   A B C D E F G H I J')
    for i in range(1,11):
        if i != 10:
            print(str(i),end = '  ')
        else:
            print(str(i),end = ' ')
        for j in alphalist:
            if j != 'J':
                print(tb[j + str(i)],end = '|')
            else:
                print(tb[j + str(i)])
        print('   -+-+-+-+-+-+-+-+-+-')

def row():
    global alphalist,i,j,tb,turn
    for i in range(1,7):
        n = 0
        for j in alphalist:
            if tb[j + str(i)] == turn:
                n += 1
                if n == 5:
                    if turn == 'X':
                        print('Winner is',P1,'!')
                    else:
                        print('Winner is',P2,'!')
                    exit()

def col():
    global alphalist,i,j,tb,turn
    for j in alphalist:
        n = 0
        for i in range(1,7):
            if tb[j + str(i)] == turn:
                n += 1
                if n == 5:
                    if turn == 'X':
                        print('Winner is',P1,'!')
                    else:
                        print('Winner is',P2,'!')
                    exit()

def ld():
    global alphalist,i,j,tb,turn
    for j in alphalist[:6]:
        for i in range(1,7):
            if tb[j + str(i)] == turn:
                n = 1
                index = alphalist.index(j)
                ii = str(i + 1)
                for k in range(4):
                    if tb[alphalist[index + 1] + ii] != turn:
                        break
                    else:
                        n += 1
                        index += 1
                        ii = str(int(ii) + 1)
                if n == 5:
                    if turn == 'X':
                        print('Winner is',P1,'!')
                    else:
                        print('Winner is',P2,'!')
                    exit()
                n = 0

def ru():
    global alphalist,i,j,tb,turn
    for j in alphalist[:6]:
        for i in range(10,4,-1):
            if tb[j + str(i)] == turn:
                n = 1
                index = alphalist.index(j)
                ii = str(i + 1)
                for k in range(4):
                    if tb[alphalist[index + 1] + ii] != turn:
                        break
                    else:
                        n += 1
                        index += 1
                        ii = str(int(ii) + 1)
                if n == 5:
                    if turn == 'X':
                        print('Winner is',P1,'!')
                    else:
                        print('Winner is',P2,'!')
                    exit()
                n = 0

def somebodywin():
    row()
    col()
    ld()
    ru()

if __name__ == '__main__':
    prboard(tb)
    P1 = input('What\'s the 1P name:')
    print(P1,'is the \'X\'.')
    P2 = input('What\'s the 2P name:')
    if P1 == P2:
        P2 += '(1)'
    print(P2,'is the \'O\'.')
    print()
    #name format
    turn = 'X'
    while True:
        prboard(tb)
        move = input('Turn for ' + turn + '. Move on which space:')
        try:
            if tb[move] != ' ':
                print('Error.')
                continue
            else:
                tb[move] = turn
        except:
            print('Enter Error.')
            continue
        #enter
        somebodywin()
        if ' ' not in tb.values():
            print('No any winner.')
            exit()
        #winner
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'
        #turn next
        print()
    prboard(tb)
    #finish
