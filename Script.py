import random
import sys

def drawBoard(board):
    
    HLINE = ' +---+---+---+---+---+---+---+---+ '
    VLINE = ' |   |   |   |   |   |   |   |   | '
    
    print(' 1  2  3  4  5  6  7  8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end='')
        for x in range(8):
            print('| %s' % (board[x][y]), end='')
        print('|')
        print(VLINE)
        print(HLINE)

def resetBoard(board):
    
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '
            board[3][3] = 'X'
            board[3][4] = '0'
            board[4][3] = '0'
            board[4][4] = 'X'

def getNewBoard():
    
    board = []
    for i in range(8):
        board.append([''] * 8)
        
    return board

def isValidMove(board, tile, xstart, ystart):
    
        if board[xstart][ystart] != '' or not isOnBoard(xstart, ystart):
            return False
        board[xstart][ystart] = tile
        if tile == 'X':
            otherTile = '0'
        else:
            otherTile = 'X'
        tileToFlip = []
        
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection()
            y += ydirection()
            
            if isOnBoard(x, y) and board[x][y] == otherTile:
                x += xdirection()
                y += ydirection()
                if not isOnBoard(x, y):
                    continue
                
                while board[x][y] == otherTile:
                    x += xdirection()
                    y += ydirection()
                    if not isOnBoard(x, y):
                        break
                    if not isOnBoard(x, y):
                        continue
                    
                    if board[x][y] == tile:
                        while True:
                            x -= xdirection()
                            y -= ydirection()
                            if x == xstart and y == ystart:
                                break
                            tileToFlip.append([x,y])
        board[xstart][ystart] = ' '
        if len(tileToFlip) == 0:
            return False
        return tileToFlip

def isOnBoard(x, y):
    
    return x >= 0 and x <= 7 and y >= 0 and y <=  7

def getBoardWithValidMoves(board, tile):
    
    dupeBoard = getBoardCopy(board)
    
    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard

def getValidMoves(board, tile):
    
    validMoves = []
    
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    
    xscore = 0
    oscore = 0
    
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == '0':
                oscore += 1
    return {'X':xscore, '0':oscore}

def enterPlayerTile():
    
    tile = ''
    
    while not (tile == 'X' or tile == '0'):
        print("Queres ser X ou 0?")
        tile = input().upper()
        
    if tile == 'X':
        return ['X', '0']
    else:
        return ['0', 'X']

def whoGoesFirst():
    
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'   

def playAgain():
    
    print('Queres jogar de novo? (sim ou não)')
    return input().lower().startwith('s')
        
def makeMove(board, tile, xstart, ystart):
    
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    
    if tilesToFlip == False:
        return False
    
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    
    dupeBoard = getNewBoard()
    
    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard

def isOnCorner(x, y):
    
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile):
    
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    
    while True:
            print('Insira seu movimento, ou escreve quit para terminar o jogo, ou hints para desligar/ligar dicas.')
            move = input().lower()
            if move == 'quit':
                return 'quit'
            if move == 'hints':
                return 'hints'
            if len(move) == 2 and move[2] in DIGITS1TO8:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if isValidMove(board, playerTile, x, y) == False:
                    continue
                else:
                    break
            else:
                print('O movimento não é valido. Digite o digito x de (1-8), depois o digito y de (1-8)')
                print('Por exemplo, 81 sera o canto superior.')
    return [x, y]

def getComputerMove(board, computerTile):
    
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)
    
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    
    bestScore = - 1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x , y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def showPoints(playerTile, computerTile):
    
    scores = getScoreOfBoard(mainBoard)
    print('Voce tem %s pontos. O computador tem %s pontos'%(scores[playerTile], scores[computerTile]))

print('Bem-vindo ao Reversi!')

while True:
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('O' + turn + 'vai primeiro.')
    
    while True:
        if turn == 'player':
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                drawBoard(validMovesBoard)
            else:
                drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)
            
            if move == 'quit':
                print('Obrigado por jogar!')
                sys.exit()
            elif move == 'hints':
                showHints = not showHints
                continue
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])
            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = 'computer'
        else:
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Pressiona enter para ver o movimento do computador.')
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)
            
            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'
        
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('X marcou %s pontos. 0 marcou %s pontos.'%(scores['X'],scores['0']))
    if scores[playerTile] > scores[computerTile]:
        print('Voce ganhou o computador por %s pontos! Parabens!'%(scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('Voce perdeu. O computador ganhou por %s pontos.'%(scores[computerTile] - scores[playerTile]))
    else:
        print('O jogo foi empate!')
    if not playAgain():
        break
    
                
    
    
    
                            
                        
        
        
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        