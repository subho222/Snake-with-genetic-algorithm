from play_each_snake import *
import random
from Snake import *
import threading
import  queue
import concurrent.futures


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     future = executor.submit(foo, 'world!')
#     return_value = future.result()
#     print(return_value)


# futures = [executor.submit(foo, param) for param in param_list] #The order will be maintained, and exiting the with will allow result collection. 
# [f.result() for f in futures]


def calculate_fitness(population):
	fitness = []
	#futures = []
	for i in range(population.shape[0]):
		# with concurrent.futures.ThreadPoolExecutor() as executor:
		# 	future = executor.submit(run,population[i],screen,clock)
		# 	futures.append(future)
		x = run(population[i],screen,clock)
		print('fitness value of chromosome '+ str(i) +' :  ', x)
		fitness.append(x)
	#fitness = [f.result() for f in futures]
	return np.array(fitness)


def selection(population,fitness,num_parents):
	parents = np.empty((num_parents,population.shape[1]))
	population_copy = population
	fitness_copy = fitness	
	for i in range(num_parents):
		max_fitness = sum(fitness_copy)
		pick = random.uniform(0, max_fitness)
		current = 0
		for chromosome in fitness_copy:
			current += chromosome
			if(current > pick):
				chromosome_idx = np.where(fitness_copy == chromosome)
				chromosome_idx = chromosome_idx[0][0]
				parents[i,:] = population_copy[chromosome_idx,:]
				population_copy = np.delete(population_copy, chromosome_idx, axis=0)
				fitness_copy = np.delete(fitness_copy,chromosome_idx)
				break

	return parents


def crossover(parents,num_offsprings):
	offsprings = np.empty(shape = (num_offsprings,parents.shape[1]))
	for i in range(num_offsprings):
		while True:
			parent1 = parents[random.randint(0,parents.shape[0]-1),:]
			parent2 = parents[random.randint(0,parents.shape[0]-1),:]
			if not (parent1 == parent2).all():
				crossover_point = int(parents.shape[1]/2) + random.randint(-10,10)
				offsprings[i] = np.append(parent1[:crossover_point],parent2[crossover_point:])
				break
	return offsprings





def mutation(offsprings,mutation_rate):
	mutated_offsprings = np.empty(shape = offsprings.shape)
	for i in range(offsprings.shape[0]):
		for gene in range(offsprings.shape[1]):
			if(100 * random.random() < mutation_rate):
				offsprings[i][gene] = random.random()
		mutated_offsprings[i] = offsprings[i]
	return mutated_offsprings


def create_new_population(population,parents,mutated_offsprings):
	new_population = np.empty(shape = population.shape)
	num_parents = parents.shape[0]
	num_offsprings = mutated_offsprings.shape[0]
	print(new_population.shape)
	new_population[:num_parents,:] = parents
	new_population[num_parents:,:] = mutated_offsprings
	print(new_population.shape)
	return new_population


