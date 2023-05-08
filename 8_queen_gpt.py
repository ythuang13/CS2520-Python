import random

# Number of queens
n = 8

# Population size
pop_size = 100

# Maximum number of generations
max_generations = 100

# Mutation probability
mutation_prob = 0.2

# Fitness function
def fitness(chromosome):
    conflicts = 0
    for i in range(n):
        for j in range(i+1, n):
            if chromosome[i] == chromosome[j] or abs(i-j) == abs(chromosome[i]-chromosome[j]):
                conflicts += 1
    return 1.0 / (conflicts + 1)

# Generate initial population
population = [[random.randint(1, n) for i in range(n)] for j in range(pop_size)]

# Evolution loop
for generation in range(max_generations):
    # Calculate fitness of each chromosome
    fitness_scores = [fitness(chromosome) for chromosome in population]
    
    # Select parents for crossover using tournament selection
    parents = []
    for i in range(pop_size):
        candidate_indices = random.sample(range(pop_size), 2)
        candidate_fitnesses = [fitness_scores[index] for index in candidate_indices]
        parent_index = candidate_indices[candidate_fitnesses.index(max(candidate_fitnesses))]
        parents.append(population[parent_index])
    
    # Create new population through crossover and mutation
    new_population = []
    for i in range(pop_size):
        parent1, parent2 = random.sample(parents, 2)
        child = [0] * n
        crossover_point = random.randint(1, n-1)
        child[:crossover_point] = parent1[:crossover_point]
        child[crossover_point:] = parent2[crossover_point:]
        if random.random() < mutation_prob:
            mutation_point = random.randint(0, n-1)
            child[mutation_point] = random.randint(1, n)
        new_population.append(child)
    
    # Replace old population with new population
    population = new_population

# Find best solution
best_chromosome = max(population, key=fitness)
best_fitness = fitness(best_chromosome)

# Print results
print("Best solution found:")
for i in range(n):
    row = ['-' for j in range(n)]
    row[best_chromosome[i]-1] = 'Q'
    print(' '.join(row))
print(f"Fitness score: {best_fitness}")
