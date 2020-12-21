from Genetic_algorithm import *
import numpy as np

input_layer_nodes = 4
hidden_layer_nodes = 6
output_layer_nodes = 3
num_indivisual_per_pop = 20
num_weights = input_layer_nodes*hidden_layer_nodes + hidden_layer_nodes*output_layer_nodes
population_size = (num_indivisual_per_pop,num_weights)
#file = open("weights.txt","w+")
new_population = np.random.choice(np.arange(-1,1,step=0.01),size=population_size,replace=True)
#new_population = np.loadtxt("weights.txt")
#print(new_population.shape)
num_generations = 100
num_parents = 10
mutation_rate = 0.5

for generation in range(num_generations):
	

	print("#Generation: ",generation+1)
	fitness = calculate_fitness(new_population)
	print("Maximum fitness value in generation ", generation+1,": ",np.max(fitness))
	parents = selection(new_population,fitness,num_parents)
	offsprings = crossover(parents,population_size[0] - num_parents)
	mutated_offsprings = mutation(offsprings, mutation_rate)
	new_population = create_new_population(new_population,parents,mutated_offsprings)
	#np.savetxt("weights.txt",new_population)

