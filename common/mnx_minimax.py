# L'importation de la bibliothèque copy est nécessaire pour créer des copies profondes des objets.
import copy

def minimax(board, depth, maximize):
    # Vérifie si le jeu est terminé et retourne le score en conséquence
    isTerminal, winner = board.isTerminal()
    if(isTerminal):
        if(winner == board.WHITE):
            return 1000
        if(winner == board.BLACK):
            return -1000
        if(winner == board.DRAW):
            return 0
    
    # Génère les mouvements possibles pour le joueur actuel
    moves = board.generateMoves()
    
    if(maximize):
        bestVal = -999999999999
        # Parcourt tous les mouvements possibles
        for move in moves:
            # Crée une copie du plateau pour simuler le mouvement
            next = copy.deepcopy(board)
            next.applyMove(move)
            # Appelle récursivement minimax sur la nouvelle configuration
            bestVal = max(bestVal, minimax(next, depth - 1, (not maximize)))
        return bestVal
    else:
        bestVal = 9999999999999
        # Parcourt tous les mouvements possibles
        for move in moves:
            # Crée une copie du plateau pour simuler le mouvement
            next = copy.deepcopy(board)
            next.applyMove(move)
            # Appelle récursivement minimax sur la nouvelle configuration
            bestVal = min(bestVal, minimax(next, depth - 1, (not maximize)))
        return bestVal