import tensorflow as tf
from tensorflow import keras
import numpy as np
def create_nn_model(w1,w2):
	
	model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(6, activation='relu',input_dim = 4, name = "hidden_layer", kernel_initializer=w1), 
    tf.keras.layers.Dense(3, activation='softmax',name = "output_layer",kernel_initializer=w2)  
	])

	return model


def process_weight_vector(indivisual):
	a = np.array(indivisual[:24])
	b = np.array(indivisual[24:])
	
	w1 = tf.constant_initializer(a.reshape(6,4))
	w2 = tf.constant_initializer(b.reshape(3,6))
	return w1, w2



def think_with_NN(featutres,indivisual):
	W1, W2 = process_weight_vector(indivisual)
	model = create_nn_model(W1,W2)
	return np.array(model(featutres))






