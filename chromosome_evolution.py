
# Surya Tej Kodali
# 1/8/20
# Making a evolutionary genetic algorithm
# Scenario: Chromosome Structure
# Ch = (g0, g1, g2, g3. g4. g5. g6, g7, g8, g9)
# 0 <= g <= 9
# Fitness
# f(ch) = (g[0]*g[1])-(g[2]-g[3])+(g[4]+g[5])-(g[6]+g[7])+(g[8]-g[9])
# Maximization problem
# Select two highest
# Cross over (single point, two point, uniform)
# Mutation, allows for species to escape a local mininmum/maximum
# Then loop to fitness and repeat until termination criteria reached
# How to improve selection, increasing offspring speeds up fitness
import numpy as np
from numpy import random
from random import randrange # randrange()
import matplotlib.pyplot as plt

NUM_CHROMOSOMES = 10
MUTATION_RATE = 0.02
NUM_CHILDREN = 16 # doubling children decreases increased generation speed by 4 to achieve max fitness
NUM_GENERATIONS = 30

def generateChromosomes(num_chromosomes):
    chromosomes_list = []
    for _ in range(num_chromosomes):
        ch = random.randint(10, size=10)
        chromosomes_list.append(ch)
    print("chromosomes: ", chromosomes_list)
    return chromosomes_list

def twoHighest(chromosomes_list):
    selected_two = []
    fitness_scores = []
    for item in chromosomes_list:
        fitness_scores.append(fitness(item))
    # print("fitness scores before: ", fitness_scores)
    fitness_scores.sort(reverse=True)
    for item in chromosomes_list:
        if(len(selected_two) < 2 and (fitness(item) == fitness_scores[0] or fitness(item) == fitness_scores[1])):
            selected_two.append(item)
    print("selected two: ", selected_two)
    print("fitness scores: ", fitness_scores)
    print("generation high fitness:", fitness_scores[0])
    return selected_two

def fitness(chromosome):
    g = chromosome
    # ideal (9,9,0,9,9,9,0,0,9,0) = 117
    f = (g[0]*g[1])-(g[2]-g[3])+(g[4]+g[5])-(g[6]+g[7])+(g[8]-g[9])
    return f

def crossover(selected_two, NUM_CHILDREN):
    new_generation = []
    crossed_chromsomes = []
    for i in range(NUM_CHILDREN):
        temp = randrange(3)
        if(temp==0):
            ch1, ch2 = singlePoint(selected_two)
        elif(temp==1):
            ch1, ch2 = twoPoint(selected_two)
        else:
            ch1, ch2 = uniform(selected_two)

        #ch1, ch2 = uniform(selected_two) # children get stuck with same genes, mutation rate limits evolution
        # different generation crashes occur where fitness drops drastically
        # temp = randrange(2)
        # if(temp==1):
        #     ch1, ch2 = singlePoint(selected_two)
        # else:
        #     ch1, ch2 = uniform(selected_two)
        crossed_chromsomes.extend([ch1,ch2])
    new_generation = mutate(MUTATION_RATE, crossed_chromsomes)
    print("new generation: ", new_generation[:5], "...")
    return new_generation

def singlePoint(selected_two):
    point = randrange(10)
    #print("point:", point)
    temp_ch1 = selected_two[0]
    temp_ch2 = selected_two[1]
    onetop = temp_ch1[:point]
    onebot = temp_ch1[point:]
    twotop = temp_ch2[:point]
    twobot = temp_ch2[point:]
    child_one = np.concatenate((onetop, twobot), axis=None)
    child_two = np.concatenate((twotop, onebot), axis=None)
    return child_one, child_two

def twoPoint(selected_two):
    point1 = randrange(5)
    point2 = randrange(5,10)
    #print("point1:", point1, "point2:", point2)
    temp_ch1 = selected_two[0]
    temp_ch2 = selected_two[1]
    child_one = np.concatenate((temp_ch1[:point1], temp_ch2[point1:point2], temp_ch1[point2:]), axis=None)
    child_two = np.concatenate((temp_ch2[:point1], temp_ch1[point1:point2], temp_ch2[point2:]), axis=None)
    return child_one, child_two

def uniform(selected_two):
    child_one = selected_two[0]
    child_two = selected_two[1]
    for index, value in enumerate(child_one):
        if(randrange(2) == 1):
            child_one[index] = child_two[index]
            child_two[index] = value
    return child_one, child_two

def mutate(MUTATION_RATE, chromosomes):
    mutated_chromosomes = []
    temp_ch = []
    for ch in chromosomes:
        temp_ch = ch
        for index in range(len(ch)):
            if(random.uniform(0,1.0) <= MUTATION_RATE):
                temp_ch[index] = randrange(10)
        mutated_chromosomes.append(temp_ch)
    return mutated_chromosomes

if __name__ == "__main__":
    print("generation 0")
    ch_list = generateChromosomes(NUM_CHROMOSOMES)
    selected_two = twoHighest(ch_list)
    # Create generation two
    ideal_generation = 0
    reached_ideal = False
    history = []
    # for i in range(NUM_GENERATIONS):
    #     if (fitness(selected_two[0]) == 117 and not(reached_ideal)): 
    #         ideal_generation = i+1
    #         reached_ideal = True
    #     print("\ngeneration ", i+1)
    #     ch_list.clear()
    #     ch_list = crossover(selected_two, NUM_CHILDREN)
    #     print("number of children:", len(ch_list))
    #     selected_two.clear()
    #     selected_two = twoHighest(ch_list)
    gen = 0
    while(not(reached_ideal)):
        highfit = fitness(selected_two[0])
        history.append(highfit)
        if (highfit == 117 and not(reached_ideal)): 
            ideal_generation = gen
            reached_ideal = True
            break
        elif(gen > 999):
            print("max generations reached!")
            break
        else:
            gen+=1
            # NUM_CHILDREN+=1 # population growth rate
            print("\ngeneration ", gen)
            ch_list.clear()
            ch_list = crossover(selected_two, NUM_CHILDREN)
            print("number of children:", len(ch_list))
            selected_two.clear()
            selected_two = twoHighest(ch_list)
    print()
    if(reached_ideal):
        print("population reached ideal fitness at generation", ideal_generation)
    else:
        print("population did not reach ideal fitness after", NUM_GENERATIONS, "generations")
    print("best: ", selected_two[0].tolist(), "f =", fitness(selected_two[0]))
    print("ideal : [9, 9, 0, 9, 9, 9, 0, 0, 9, 0], f =", fitness(np.array([9,9,0,9,9,9,0,0,9,0])))
    count = -1
    for item in history:
        if item == 117:
            count+=1
    print("fail to stop:", count)
    print("history:", history)
  
    plt.plot(history)
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title("Evolution of Chromosome")
    plt.show()