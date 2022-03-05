#ticTacToe.py
def prboard(board):
    print('A B C')
    print(board['A1'] + '|' + board['B1'] + '|' + board['C1'] + '1')
    print('-+-+-')
    print(board['A2'] + '|' + board['B2'] + '|' + board['C2'] + '2')
    print('-+-+-')
    print(board['A3'] + '|' + board['B3'] + '|' + board['C3'] + '3')
tb = {'A1':' ','B1':' ','C1':' ',
'A2':' ','B2':' ','C2':' ',
'A3':' ','B3':' ','C3':' '}
prboard(tb)
P1 = input('What\'s the 1P name:')
print(P1,'is the \'X\'.')
P2 = input('What\'s the 2P name:')
if P1 == P2:
	P2 += '(1)'
print(P2,'is the \'O\'.')
print()
#name format
winner = ''
turn = 'X'
while not winner:
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
	if ((tb['A1'] == turn and tb['A2'] == turn and tb['A3'] == turn) or (tb['B1'] == turn and tb['B2'] == turn and tb['B3'] == turn) or (tb['C1'] == turn and tb['C2'] == turn and tb['C3'] == turn)) or ((tb['A1'] == turn and tb['B1'] == turn and tb['C1'] == turn) or (tb['A2'] == turn and tb['B2'] == turn and tb['C2'] == turn) or (tb['A3'] == turn and tb['B3'] == turn and tb['C3'] == turn)) or ((tb['A1'] == turn and tb['B2'] == turn and tb['C3'] == turn) or (tb['C1'] == turn and tb['B2'] == turn and tb['A3'] == turn)):
		if turn == 'X':
			winner = P1
		else:
			winner = P2
		break
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
print('Winner is',winner,'!')
#finish
