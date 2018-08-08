import random
import numpy as np

"""This program solves 0/1 Knapsack problem using genetic algorithm"""

# GLOBAL PARAMETERS

MAX_WEIGHT = 100              #Maximum weight the knapsack bag can hold
POPULATION_SIZE = 5	      #Population size of a generation
NUMBER_OF_ITEMS = 4          #Total number of items available
MUTATION_PROBALITY = 0.2      #The probabilty that the child will be mutatted
NUMBER_OF_ITERATIONS = 20     #Total no of generations
random.seed = 1

items = {}
def initialize_knapsack_table():
  """ Initializes the knapsack input table by getting the weight and value from the user"""
  for i in range(NUMBER_OF_ITEMS):
      print "For Item", i + 1
      weight = int(raw_input("Enter the weight for item"))
      value = int(raw_input("Enter the value for item"))
      items[i] = weight,value
      print items[i]

def print_knapsack_table():
  """ Prints the knapsack Table """
  print "Knapsack Table"
  for i in range(NUMBER_OF_ITEMS):
     print chr(i + 65),
     print items[i][0],
     print items[i][1]

class individual:
   """ The individual holds a list of 0's or 1's 
       0 - Corresponding Item is not in list
       1 - Coressponding Item is there in Knapsack
       It also holds the the total value which is denotes as fitness"""
   def __init__(self):
      """ Initializes the genome as an empty list and fitness as zero"""
      self.genome = []
      self.fitness = 0

   def generate(self):
      """ Generates random genomes for the first generation """
      for i in range(NUMBER_OF_ITEMS):
          self.genome.append(random.randint(0,1))
      self.fitness = self.fitness_function()

   def fitness_function(self):
      """ The fitness function gives the total value of the items in the knapsack
          If the weight exceeds the maximum weight fitness becomes 0"""
      fitness = 0
      weight = 0
      for i in range(NUMBER_OF_ITEMS):
          if self.genome[i] == 1:
             weight = weight + items[i][0]
             fitness = fitness + items[i][1]
      if weight > MAX_WEIGHT:
         fitness = 0
      return fitness

   def mutate(self):
      """ Chooses a random item and topples its presence """

      mutate_index =  random.randint(0,NUMBER_OF_ITEMS-1)
      self.genome[mutate_index] = bool(self.genome[mutate_index]) ^ 1
      self.fitness = self.fitness_function()
   


class population:
   """ This stores a list of the population members of a generation"""

   def __init__(self):
       self.populationlist = []
       

   def generate_random_population(self):
      """ Generates a random list of population """
      for i in range(POPULATION_SIZE):
          Chromosome = individual()
          Chromosome.generate()
          self.populationlist.append(Chromosome)

   def crossover(self):
       """ Randomly selects two individuls from population list and cross over happens
          It returns the two children """

       crossover1 = random.randint(0,POPULATION_SIZE-1)
       crossover2 = random.randint(0,POPULATION_SIZE-1)
       
       spiltpoint =  random.randint(0,NUMBER_OF_ITEMS-1)

       child1 = individual()
       child2 = individual()
       
       list1 = []
       list2 = []

       child1.genome = self.populationlist[crossover1].genome
       child2.genome = self.populationlist[crossover2].genome       
         
       list1 = child1.genome[:spiltpoint] + child2.genome[spiltpoint:]
       list2 = child2.genome[:spiltpoint] + child1.genome[spiltpoint:]

       child1.genome = list1
       child2.genome = list2
                   
       child1.fitness =  child1.fitness_function()
       child2.fitness =  child2.fitness_function()

       return child1,child2
   
   def sort_and_cut_growth(self):
       """ The population list is sorted according to the fitness function and the least fit ones are 
           removed to maintain the population size """

       self.populationlist = sorted( self.populationlist, key=lambda x: x.fitness, reverse = True)
       self.populationlist = self.populationlist[:POPULATION_SIZE]



if __name__ == "__main__":
  
  initialize_knapsack_table()		#Knapsack Table is got from the user
  knapsack = population()               
  knapsack.generate_random_population() #For first generation it is randomly populated

  for x in range(NUMBER_OF_ITERATIONS): 
   print "Knapsack Generation ",        #Prints genome for each generation
   print x + 1
   for i in range(POPULATION_SIZE):
      print knapsack.populationlist[i].genome
      print knapsack.populationlist[i].fitness

   for y in range(POPULATION_SIZE/2 + 1):      # Performs crossover
    offspring1,offspring2 = knapsack.crossover()
    if random.random() > MUTATION_PROBALITY:   # Randomly generates the mutation probability;if greater than given propability mutation occurs 
     offspring1.mutate()
    if random.random() > MUTATION_PROBALITY:
     offspring2.mutate()
  
    knapsack.populationlist.append(offspring1) # After mutation it is appended to the list
    knapsack.populationlist.append(offspring2)

   knapsack.sort_and_cut_growth()              # At the end of generation death cycle occurs

  print_knapsack_table()
  
  print "Solution set:"
  print knapsack.populationlist[0].genome
  
  print "Items taken are"
  for i in range(NUMBER_OF_ITEMS):            # Prints the solution set
     if knapsack.populationlist[0].genome[i] == 1:
        print chr(i+ 65),
  print "\n"
  print "Total value is",
  print knapsack.populationlist[0].fitness
