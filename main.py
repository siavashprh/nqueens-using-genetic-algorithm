import random
import matplotlib.pyplot as plt

# Problem-specific parameters
N = 16
POPULATION_SIZE = 100
MAX_GENERATIONS = 1000
MUTATION_RATE = 0.1

# generate a random chromosome.
def generate_chromosome():
    return [random.randint(0, N - 1) for _ in range(N)]


# calculate the number of conflicts of a chromosome.
def calculate_fitness(chromosome):
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            if (
                chromosome[i] == chromosome[j]
                or abs(chromosome[i] - chromosome[j]) == j - i
            ):
                conflicts += 1
    return conflicts


# perform tournament selection to choose parents for reproduction.
def selection(population):
    selected = []
    for _ in range(len(population)):
        contestants = random.sample(population, 2)
        selected.append(
            min(contestants, key=lambda chromosome: calculate_fitness(chromosome))
        )
    return selected


# perform N-point crossover between two parents.
def crossover(parent1, parent2):
    n = random.randint(1, N - 1)
    child1 = parent1[:n] + parent2[n:]
    child2 = parent2[:n] + parent1[n:]
    return child1, child2


# Mutate a chromosome by randomly changing a position.
def mutation(chromosome):
    if random.random() < MUTATION_RATE:
        mutated_index = random.randint(0, N - 1)
        chromosome[mutated_index] = random.randint(0, N - 1)

# Generate an initial population.
def generate_population():
    return [generate_chromosome() for _ in range(POPULATION_SIZE)]


# Plot the chess board with queens.
def plot_board(chromosome):
    board = [['.'] * N for _ in range(N)]
    for col, row in enumerate(chromosome):
        board[row][col] = 'Q'

    plt.figure(figsize=(N, N))
    plt.imshow([[0.5 if (i + j) % 2 else 0.9 for i in range(N)] for j in range(N)],
               cmap='RdBu', vmin=0, vmax=1)

    for i in range(N):
        for j in range(N):
            plt.text(j, i, board[i][j], ha='center', va='center', fontsize=20)

    plt.xticks([])
    plt.yticks([])
    plt.show()


# Solve the N-Queens problem using a genetic algorithm.
def genetic_algorithm():
    population = generate_population()

    for generation in range(MAX_GENERATIONS):
        population = sorted(
            population, key=lambda chromosome: calculate_fitness(chromosome)
        )
        best_chromosome = population[0]
        if calculate_fitness(best_chromosome) == 0:
            return best_chromosome

        selected_parents = selection(population)
        offspring = []
        while len(offspring) < POPULATION_SIZE:
            parent1, parent2 = random.sample(selected_parents, 2)
            child1, child2 = crossover(parent1, parent2)
            mutation(child1)
            mutation(child2)
            offspring.extend([child1, child2])

        population = offspring

    return None


# Run the genetic algorithm.
solution = genetic_algorithm()

# Print the solution.
if solution:
    print("Found a solution:")
    print("calculate fitness:", calculate_fitness(solution))
    for i in range(N):
        row = ['.'] * N
        row[solution[i]] = 'Q'
        print(' '.join(row))
    plot_board(solution)
else:
    print("No solution found.")