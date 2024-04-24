import copy
import numpy as np
import math
from common.game import Board  # Importation de la classe Board depuis le fichier common.game
import random

# Classe représentant une arête dans l'arbre MCTS
class Edge():
    def __init__(self, move, parentNode):
        self.parentNode = parentNode  # Noeud parent
        self.move = move  # Mouvement associé à cette arête
        self.N = 0  # Nombre de visites de cette arête
        self.W = 0  # Somme des valeurs de récompense associées aux visites
        self.Q = 0  # Valeur moyenne des récompenses
        self.P = 0  # Probabilité calculée par le réseau de neurones

# Classe représentant un noeud dans l'arbre MCTS
class Node():
    def __init__(self, board, parentEdge):
        self.board = board  # Position du jeu associée à ce noeud
        self.parentEdge = parentEdge  # Arête parente
        self.childEdgeNode = []  # Liste des arêtes et noeuds enfants

    # Méthode pour étendre le noeud en ajoutant des arêtes et des noeuds enfants
    def expand(self, network):
        moves = self.board.generateMoves()  # Générer les mouvements possibles depuis cette position
        for m in moves:
            child_board = copy.deepcopy(self.board)  # Copier la position actuelle
            child_board.applyMove(m)  # Appliquer le mouvement
            child_edge = Edge(m, self)  # Créer une nouvelle arête avec ce mouvement
            childNode = Node(child_board, child_edge)  # Créer un nouveau noeud associé à la nouvelle position
            self.childEdgeNode.append((child_edge,childNode))  # Ajouter l'arête et le noeud associés à la liste
        q = network.predict(np.array([self.board.toNetworkInput()]))  # Obtenir les prédictions du réseau pour cette position
        prob_sum = 0.
        for (edge,_) in self.childEdgeNode:
            m_idx = self.board.getNetworkOutputIndex(edge.move)
            edge.P = q[0][0][m_idx]  # Attribuer la probabilité calculée par le réseau à chaque arête enfant
            prob_sum += edge.P
        for edge,_ in self.childEdgeNode:
            edge.P /= prob_sum  # Normaliser les probabilités des arêtes enfants pour qu'elles forment une distribution de probabilité
        v = q[1][0][0]  # Récupérer la valeur estimée de cette position par le réseau
        return v

    # Méthode pour vérifier si le noeud est une feuille (c'est-à-dire s'il n'a pas d'enfants)
    def isLeaf(self):
        return self.childEdgeNode == []

# Classe pour effectuer une recherche MCTS
class MCTS():

    def __init__(self, network):
        self.network = network  # Réseau de neurones utilisé pour l'évaluation
        self.rootNode = None  # Noeud racine de l'arbre MCTS
        self.tau = 1.0  # Paramètre tau pour le calcul des probabilités de déplacement
        self.c_puct = 1.0  # Paramètre c_puct pour l'exploration UCT

    # Méthode pour calculer la valeur UCT d'une arête
    def uctValue(self, edge, parentN):
        return self.c_puct * edge.P * (math.sqrt(parentN) / (1+edge.N))

    # Méthode de sélection d'un enfant à partir d'un noeud
    def select(self, node):
        if(node.isLeaf()):
            return node
        else:
            maxUctChild = None
            maxUctValue = -100000000.
            for edge, child_node in node.childEdgeNode:
                uctVal = self.uctValue(edge, edge.parentNode.parentEdge.N)
                val = edge.Q
                if(edge.parentNode.board.turn == Board.BLACK):
                    val = -edge.Q
                uctValChild = val + uctVal
                if(uctValChild > maxUctValue):
                    maxUctChild = child_node
                    maxUctValue = uctValChild
            allBestChilds = []
            for edge, child_node in node.childEdgeNode:
                uctVal = self.uctValue(edge, edge.parentNode.parentEdge.N)
                val = edge.Q
                if(edge.parentNode.board.turn == Board.BLACK):
                    val = -edge.Q
                uctValChild = val + uctVal
                if(uctValChild == maxUctValue):
                    allBestChilds.append(child_node)
            if(maxUctChild == None):
                raise ValueError("could not identify child with best uct value")
            else:
                if(len(allBestChilds) > 1):
                    idx = random.randint(0, len(allBestChilds)-1)
                    return self.select(allBestChilds[idx])
                else:
                    return self.select(maxUctChild)

    # Méthode pour étendre un noeud et évaluer les enfants
    def expandAndEvaluate(self, node):
        terminal, winner = node.board.isTerminal()  # Vérifier si la position actuelle est terminale
        if(terminal == True):
            v = 0.0
            if(winner == Board.WHITE):
                v = 1.0
            if(winner == Board.BLACK):
                v = -1.0
            self.backup(v, node.parentEdge)  # Effectuer une sauvegarde des valeurs de récompense rétrogradée
            return
        v = node.expand(self.network)  # Étendre le noeud et obtenir la valeur d'évaluation de la position
        self.backup(v, node.parentEdge)  # Effectuer une sauvegarde des valeurs de récompense rétrogradée

    # Méthode pour effectuer une sauvegarde des valeurs de récompense rétrogradée
    def backup(self, v, edge):
        edge.N += 1  # Incrémenter le nombre de visites de l'arête
        edge.W = edge.W + v  # Ajouter la valeur de récompense à la somme des récompenses
        edge.Q = edge.W / edge.N  # Calculer la valeur moyenne des récompenses
        if(edge.parentNode != None):
            if(edge.parentNode.parentEdge != None):
                self.backup(v, edge.parentNode.parentEdge)  # Effectuer une sauvegarde rétrogradée récursive

    # Méthode pour effectuer une recherche MCTS à partir d'un noeud racine donné
    def search(self, rootNode):
        self.rootNode = rootNode
        _ = self.rootNode.expand(self.network)  # Étendre le noeud racine
        for i in range(0,100):  # Effectuer un certain nombre d'itérations de recherche
            selected_node = self.select(rootNode)  # Sélectionner un noeud à explorer
            self.expandAndEvaluate(selected_node)  # Étendre ce noeud et évaluer ses enfants
        N_sum = 0  # Initialisation de la somme des visites pour le calcul des probabilités
        moveProbs = []  # Initialisation de la liste des probabilités de déplacement
        for edge, _ in rootNode.childEdgeNode:
            N_sum += edge.N  # Calcul de la somme des visites de toutes les arêtes enfants
        for (edge, node) in rootNode.childEdgeNode:
            prob = (edge.N ** (1 / self.tau)) / ((N_sum) ** (1/self.tau))  # Calcul des probabilités de déplacement normalisées
            moveProbs.append((edge.move, prob, edge.N, edge.Q))  # Ajout des probabilités à la liste des probabilités de déplacement
        return moveProbs  # Retourner la liste des probabilités de déplacement