from keras.models import Model  # Importation de la classe Model depuis keras.models
from keras.layers import *  # Importation de toutes les couches disponibles depuis keras.layers
import tensorflow as tf  # Importation du module tensorflow sous le nom tf

inp = Input((21,))  # Définition de la couche d'entrée avec 21 dimensions

# Création des couches de neurones densément connectées avec la fonction d'activation ReLU
l1 = Dense(128, activation='relu')(inp)
l2 = Dense(128, activation='relu')(l1)
l3 = Dense(128, activation='relu')(l2)
l4 = Dense(128, activation='relu')(l3)
l5 = Dense(128, activation='relu')(l4)

# Couche de sortie pour les probabilités des mouvements, avec une fonction d'activation softmax
policyOut = Dense(28, name='policyHead', activation='softmax')(l5)

# Couche de sortie pour la valeur estimée de la position, avec une fonction d'activation tanh
valueOut = Dense(1, activation='tanh', name='valueHead')(l5)

# Définition de la fonction de perte pour l'apprentissage du modèle
bce = tf.keras.losses.CategoricalCrossentropy(from_logits=False)

# Création du modèle en spécifiant les couches d'entrée et de sortie
model = Model(inp, [policyOut,valueOut])

# Compilation du modèle avec l'optimiseur SGD et les fonctions de perte pour chaque sortie
model.compile(optimizer = 'SGD', loss={'valueHead' : 'mean_squared_error', 'policyHead' : bce})

# Sauvegarde du modèle
model.save('random_model.keras')
