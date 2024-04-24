# Définition d'une class python Board
class Board():

    # Définition des constantes pour les pièces et les couleurs
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def __init__(self):
        # Initialisation du plateau de jeu avec les pièces et les couleurs par défaut
        self.board = [self.EMPTY, self.EMPTY, self.EMPTY,
                      self.EMPTY, self.EMPTY, self.EMPTY,
                      self.EMPTY, self.EMPTY, self.EMPTY ]

        # Initialisation du joueur dont c'est le tour
        self.turn = self.WHITE

        # Dictionnaire pour mapper les mouvements possibles aux index de sortie du réseau
        self.outputIndex = {}

        # Liste des mouvements légaux (initialisée à None car elle sera calculée dynamiquement)
        self.legal_moves = None

        # Définition des indices de sortie pour les différents types de mouvements possibles
        # (mouvements en avant, captures de pions adverses, etc.)
        # Chaque mouvement possible est associé à un index de sortie correspondant dans le réseau
        # Ces indices sont utilisés pour l'apprentissage et l'inférence du réseau de neurones
        # Les mouvements sont représentés par des coordonnées (ligne, colonne) de la forme "(ligne, colonne)"
        # Ces coordonnées sont stockées sous forme de chaînes de caractères dans le dictionnaire outputIndex

        # Indices de sortie pour les mouvements des pions blancs vers l'avant
        self.outputIndex["(6, 3)"] = 0
        self.outputIndex["(7, 4)"] = 1
        self.outputIndex["(8, 5)"] = 2
        self.outputIndex["(3, 0)"] = 3
        self.outputIndex["(4, 1)"] = 4
        self.outputIndex["(5, 2)"] = 5

        # Indices de sortie pour les mouvements des pions noirs vers l'avant
        self.outputIndex["(0, 3)"] = 6
        self.outputIndex["(1, 4)"] = 7
        self.outputIndex["(2, 5)"] = 8
        self.outputIndex["(3, 6)"] = 9
        self.outputIndex["(4, 7)"] = 10
        self.outputIndex["(5, 8)"] = 11

        # Indices de sortie pour les captures de pions blancs
        self.outputIndex["(6, 4)"] = 12
        self.outputIndex["(7, 3)"] = 13
        self.outputIndex["(7, 5)"] = 14
        self.outputIndex["(8, 4)"] = 15
        self.outputIndex["(3, 1)"] = 16
        self.outputIndex["(4, 0)"] = 17
        self.outputIndex["(4, 2)"] = 18
        self.outputIndex["(5, 1)"] = 19

        # Indices de sortie pour les captures de pions noirs
        self.outputIndex["(0, 4)"] = 20
        self.outputIndex["(1, 3)"] = 21
        self.outputIndex["(1, 5)"] = 22
        self.outputIndex["(2, 4)"] = 23
        self.outputIndex["(3, 7)"] = 24
        self.outputIndex["(4, 6)"] = 25
        self.outputIndex["(4, 8)"] = 26
        self.outputIndex["(5, 7)"] = 27

        # Liste indiquant les cases de capture possibles pour les pions blancs
        self.WHITE_PAWN_CAPTURES = [
            [],
            [],
            [],
            [1],
            [0,2],
            [1],
            [4],
            [3,5],
            [4]
        ]

        # Liste indiquant les cases de capture possibles pour les pions noirs
        self.BLACK_PAWN_CAPTURES = [
            [4],
            [3,5],
            [4],
            [7],
            [6,8],
            [7],
            [],
            [],
            []
        ]

    # Méthode pour déterminer si le jeu est terminé et qui a gagné
    def isTerminal(self):
        winner = None
        # Le joueur noir gagne s'il a placé un pion sur la première rangée
        if(self.board[6] == Board.BLACK or
                self.board[7] == self.BLACK or
                self.board[8] == self.BLACK):
            winner = self.BLACK
        # Le joueur blanc gagne s'il a placé un pion sur la quatrième rangée
        if (self.board[0] == self.WHITE or
                self.board[1] == self.WHITE or
                self.board[2] == self.WHITE):
            winner = self.WHITE
        if(winner != None):
            return (True, winner)
        else:
            # Match nul s'il n'y a pas de gagnant et que le joueur actuel ne peut pas jouer
            if(len(self.generateMoves()) == 0):
                if(self.turn == Board.WHITE):
                    return (True, Board.BLACK)
                else:
                    return (True, Board.WHITE)
            else:
                return (False, None)

    # Méthode pour obtenir une représentation textuelle du plateau de jeu
    def toString(self):
        if(self.turn == self.WHITE):
            return "w:"  + "".join([ str(x) for x in self.board])
        else:
            return "b:"  + "".join([ str(x) for x in self.board])

    # Méthode pour obtenir une représentation visuelle du plateau de jeu
    def toDisplayString(self):
        s = ""
        for i in range(0,3):
            if(self.board[i] == self.WHITE):
                s += "W"
            if(self.board[i] == self.BLACK):
                s += "B"
            if(self.board[i] == self.EMPTY):
                s += "_"
        s += "\n"
        for i in range(3,6):
            if(self.board[i] == self.WHITE):
                s += "W"
            if(self.board[i] == self.BLACK):
                s += "B"
            if(self.board[i] == self.EMPTY):
                s += "_"
        s += "\n"
        for i in range(6,9):
            if(self.board[i] == self.WHITE):
                s += "W"
            if(self.board[i] == self.BLACK):
                s += "B"
            if(self.board[i] == self.EMPTY):
                s += "_"
        s += "\n"
        return s

    # Méthode pour obtenir une représentation du plateau de jeu adaptée à l'entrée du réseau de neurones
    def toNetworkInput(self):
        posVec = []
        # Ajoute les pions blancs
        for i in range(0,9):
            if(self.board[i] == Board.WHITE):
                posVec.append(1)
            else:
                posVec.append(0)
        # Ajoute les pions noirs
        for i in range(0,9):
            if(self.board[i] == Board.BLACK):
                posVec.append(1)
            else:
                posVec.append(0)
        # Ajoute la couleur du joueur actuel
        for i in range(0,3):
            if(self.turn == Board.WHITE):
                posVec.append(1)
            else:
                posVec.append(0)
        return posVec

    # Méthode pour obtenir l'index de sortie du réseau de neurones correspondant à un mouvement donné
    def getNetworkOutputIndex(self, move):
        return self.outputIndex[str(move)]

    # Méthode pour définir la position de départ du plateau de jeu
    def setStartingPosition(self):
        # Position de départ
        # NOIR NOIR NOIR
        # ####### #######
        # BLANC BLANC BLANC
        self.board = [self.BLACK, self.BLACK, self.BLACK,
                      self.EMPTY, self.EMPTY, self.EMPTY,
                      self.WHITE, self.WHITE, self.WHITE ]

    # Méthode pour appliquer un mouvement sur le plateau de jeu
    def applyMove(self, move):
        fromSquare = move[0]
        toSquare = move[1]
        # Déplace la pièce
        self.board[toSquare] = self.board[fromSquare]
        self.board[fromSquare] = self.EMPTY
        # Change le tour du joueur
        if(self.turn == self.WHITE):
            self.turn = self.BLACK
        else:
            self.turn = self.WHITE
        self.legal_moves = None  # Réinitialise les mouvements légaux

    # Méthode pour générer tous les mouvements légaux possibles pour le joueur actuel
    def generateMoves(self):
        if(self.legal_moves == None):
            moves = []
            for i in range(0, 9):
                if(self.board[i] == self.turn):
                    if(self.turn == self.WHITE):
                        # Vérifie si le joueur blanc peut avancer d'une case
                        toSquare = i - 3
                        if(toSquare >= 0):
                            if(self.board[toSquare] == self.EMPTY):
                                moves.append((i, toSquare))
                        # Vérifie s'il peut capturer à gauche ou à droite
                        potCaptureSquares = self.WHITE_PAWN_CAPTURES[i]
                        for toSquare in potCaptureSquares:
                            if(self.board[toSquare] == self.BLACK):
                                moves.append((i, toSquare))
                    if (self.turn == self.BLACK):
                        # Vérifie si le joueur noir peut avancer d'une case
                        toSquare = i + 3
                        if(toSquare < 9):
                            if (self.board[toSquare] == self.EMPTY):
                                moves.append((i, toSquare))
                        # Vérifie s'il peut capturer à gauche ou à droite
                        potCaptureSquares = self.BLACK_PAWN_CAPTURES[i]
                        for toSquare in potCaptureSquares:
                            if (self.board[toSquare] == self.WHITE):
                                moves.append((i, toSquare))
            self.legal_moves = moves
        return self.legal_moves
