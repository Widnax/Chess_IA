import chess
import chess.svg

# Définition de la table de valorisation des pièces
pieceSquareTable = [
  [ -50,-40,-30,-30,-30,-30,-40,-50 ],
  [ -40,-20,  0,  0,  0,  0,-20,-40 ],
  [ -30,  0, 10, 15, 15, 10,  0,-30 ],
  [ -30,  5, 15, 20, 20, 15,  5,-30 ],
  [ -30,  0, 15, 20, 20, 15,  0,-30 ],
  [ -30,  5, 10, 15, 15, 10,  5,-30 ],
  [ -40,-20,  0,  5,  5,  0,-20,-40 ],
  [ -50,-40,-30,-30,-30,-30,-40,-50 ] ]

# Définition de la fonction d'évaluation de l'échiquier
def eval(board):
    scoreWhite = 0
    scoreBlack = 0
    for i in range(0,8):
        for j in range(0,8):
            squareIJ = chess.square(i,j)
            pieceIJ = board.piece_at(squareIJ)
            if str(pieceIJ) == "P":
                scoreWhite += (100 + pieceSquareTable[i][j])
            if str(pieceIJ) == "N":
                scoreWhite += (310 + pieceSquareTable[i][j])
            if str(pieceIJ) == "B":
                scoreWhite += (320 + pieceSquareTable[i][j])
            if str(pieceIJ) == "R":
                scoreWhite += (500 + pieceSquareTable[i][j])
            if str(pieceIJ) == "Q":
                scoreWhite += (900 + pieceSquareTable[i][j])
            if str(pieceIJ) == "p":
                scoreBlack += (100 + pieceSquareTable[i][j])
            if str(pieceIJ) == "n":
                scoreBlack += (310 + pieceSquareTable[i][j])
            if str(pieceIJ) == "b":
                scoreBlack += (320 + pieceSquareTable[i][j])
            if str(pieceIJ) == "r":
                scoreBlack += (500 + pieceSquareTable[i][j])
            if str(pieceIJ) == "q":
                scoreBlack += (900 + pieceSquareTable[i][j])
    return scoreWhite - scoreBlack

NODECOUNT = 0
# Définition de l'algorithme alpha-beta
def alphaBeta(board, depth, alpha, beta, maximize):
    # Initialisation du compteur de nœuds explorés
    global NODECOUNT
    
    # Vérification de la fin de la partie
    if(board.is_checkmate()):
        if(board.turn == chess.WHITE):
            return -100000
        else:
            return 1000000
    
    # Évaluation de l'échiquier si la profondeur maximale est atteinte
    if depth == 0:
        return eval(board)
    
    # Génération des coups légaux
    legals = board.legal_moves
    
    # Cas de maximisation
    if(maximize):
        bestVal = -9999
        for move in legals:
            board.push(move)
            NODECOUNT += 1
            bestVal = max(bestVal, alphaBeta(board, depth-1, alpha, beta, (not maximize)))
            board.pop()
            alpha = max(alpha, bestVal)
            if alpha >= beta:
                return bestVal
        return bestVal
    
    # Cas de minimisation
    else:
        bestVal = 9999
        for move in legals:
            board.push(move)
            NODECOUNT += 1
            bestVal = min(bestVal, alphaBeta(board, depth - 1, alpha, beta, (not maximize)))
            board.pop()
            beta = min(beta, bestVal)
            if beta <= alpha:
                return bestVal
        return bestVal

# Définition de la fonction pour obtenir le prochain coup à jouer
def getNextMove(depth, board, maximize):
    legals = board.legal_moves
    bestMove = None
    bestValue = -9999
    if(not maximize):
        bestValue = 9999
    for move in legals:
        board.push(move)
        value = alphaBeta(board, depth-1, -10000, 10000, (not maximize))
        board.pop()
        if maximize:
            if value > bestValue:
                bestValue = value
                bestMove = move
        else:
            if value < bestValue:
                bestValue = value
                bestMove = move
    return (bestMove, bestValue)

def play_chess(depth=3):
    board = chess.Board()  # Initialisation du tableau d'échecs
    player_color = input("Choisissez la couleur des pièces que vous voulez jouer (B/N) : ").upper()

    while not board.is_game_over():
        # Affichage du tableau d'échecs
        print(board)
        # Affiche du plateau sous format FEN
        print(board.fen())

        if player_color == "B" and board.turn == chess.WHITE:
            # Au tour du joueur de jouer
            try:
                move = input("Votre coup (notation algebrique): ")
                if chess.Move.from_uci(move) in board.legal_moves:
                    board.push_uci(move)
                else:
                    print("Coup invalide, veuillez rejouer.")
            except:
                print("Coup invalide, veuillez rejouer.")

        elif player_color == "N" and board.turn == chess.BLACK:
            # Au tour du joueur de jouer
            move = input("Votre coup (notation algebrique): ")
            try:
                if chess.Move.from_uci(move) in board.legal_moves:
                    board.push_uci(move)
                else:
                    print("Coup invalide, veuillez rejouer.")
            except:
                print("Coup invalide, veuillez rejouer.")

        else:
            # Au tour de l'algorithme alpha-beta de jouer
            best_move, _ = getNextMove(depth, board, board.turn == chess.WHITE)
            board.push(best_move)
            print("Coup de l'ordinateur : ", best_move)

        print("\n")  # Affichage d'une ligne vide pour la clarté
    print("Fin de la partie")
    print("Le gagnant est : ", board.result())

play_chess()
