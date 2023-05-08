# Yitian Huang
# chromosome encoding scheme of n queen is each 
# column from left to right, one queen per column,
# the gene is the row number for that queen
# this took 2 hours, chatgpt got it in 10 seconds first try
# with faster, shorter code, more readable code, and less jank


import random

class GeneticNQueen:
    generation_counter = 0
    chromosomes = []
    fitnesses = {}
    max_generations = 1000
    parents = []
    children = []
    n = 0


    def __init__(self, n, num_of_chromosomes, mutation_chance=0.05, max_generations=100, seed=None):
        self.num_of_chromosomes = num_of_chromosomes
        self.chromosomes = ["" for _ in range(num_of_chromosomes)]
        self.mutation_chance = mutation_chance
        self.n = n
        self.max_generations = max_generations

        if seed is not None:
            random.seed(seed)

    def random_generate_chromosome(self) -> str:
        """return a random chromosome with above encoding"""
        return "".join([str(random.randint(1, self.n)) for i in range(self.n)])

    def random_generate_generation(self) -> None:
        """return a randomly generated generation"""
        population = []
        for _ in range(self.num_of_chromosomes):
            population.append(self.random_generate_chromosome())
        
        return population
            
    def fitnesses_evaluation(self) -> None:
        """evaluate all chromosomes' fitness in genes, store in fitnesses"""
        self.fitnesses = {}
        for chromosome in self.chromosomes:
            self.fitnesses[chromosome] = self.fitness_evaluation(chromosome)


    def fitness_evaluation(self, chromosome) -> int:
        """evaluate and return a chromosome's fitness
        fitness is calculated based on each queen,
        how many other queen it sees, 0 is optimal, 7 * 8 = 56 is worst
        It's the inverse of what we have in class.
        It's more intuitive and we want to minimize it"""
        clashes = 0

        # since we assumed one queen per column, we only need to check row and diagonal
        for i, gene in enumerate(chromosome):
            for j in range(self.n):
                if i == j:
                    continue
                # row
                if gene == chromosome[j]:
                    clashes += 1
                # diagonal
                dx = abs(j - i)
                dy = abs(int(chromosome[j]) - int(gene))
                if dx == dy:
                    clashes += 1 
                
        return clashes

    def selection(self):
        """select half of the best for crossover"""
        sorted_dict = sorted(self.fitnesses.items(), key=lambda x: x[1])
        half_length = self.num_of_chromosomes // 2
        self.parents = [x[0] for x in sorted_dict[:half_length]]

    def crossover(self):
        """create childrens for next generation"""
        self.children = []

        for parent1, parent2 in zip(self.parents[0::2], self.parents[1::2]):
            split_position = random.randint(2, 6)
            children1 = parent1[:split_position] + parent2[split_position:]
            children2 = parent2[:split_position] + parent1[split_position:]

            self.children.append(children1)
            self.children.append(children2)


    def mutation(self) -> None:
        """each chromosome has a mutation chance of mutate random gene to something else"""
        for i, chromosome in enumerate(self.chromosomes):
            if random.random() < self.mutation_chance:
                gene_list = [*chromosome]
                gene_list[random.randint(0, self.n-1)] = str(random.randint(1, self.n))
                self.chromosomes[i] = "".join(gene_list)

    def is_terminate(self) -> bool:
        """check terminate condition
        return true if terminate, false if not
        """
        if self.generation_counter > self.max_generations:
            return True
        for fitness in self.fitnesses.values():
            if fitness == 0:
                return True
        return False

    def output(self) -> None:
        """print output"""
        # if there's a optimal, print optimal else print best
        sorted_fitnesses = sorted(self.fitnesses.items(), key=lambda x: x[1])
        best = sorted_fitnesses[0]
        print(best)

        # print output is from chatgpt
        grid = [["_" for _ in range(self.n)] for _ in range(self.n)]
        for i, gene in enumerate(best[0]):
            grid[self.n - int(gene)][i] = "Q"

        alphabets = [chr(ord("A")+i) for i in range(self.n)]
        print(" ", " ".join(alphabets))
        for i, row in enumerate(grid):
            print(self.n - i, end=" ")
            print(' '.join(row))
        

    def run(self):
        print("Generate intial population", self.generation_counter)
        # generate initial population
        self.chromosomes = self.random_generate_generation()

        # fitness evaluation
        self.fitnesses_evaluation()
        print(f"initial chromosomes' fitnesses {self.fitnesses=}")

        # loop, condition terminate condition
        while not self.is_terminate():
            self.generation_counter += 1
            print(f"gen {self.generation_counter}")

            # selection
            self.selection()
            # crossover
            self.crossover()
            # create new generation by coming parents and child
            self.chromosomes = self.parents + self.children
            # mutation
            self.mutation()

            # fitness evaluation
            self.fitnesses_evaluation()
        
        # print result
        self.output()

def main():
    ga = GeneticNQueen(n=8, num_of_chromosomes=16, max_generations=500, mutation_chance=0.1)
    ga.run()

if __name__ == "__main__":
    main()