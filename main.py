from testEnvironment import *
from constants import *
import numpy as np
import pickle

maxPredatorFitness = 0
maxPreyFitness = 0
minPredatorFitness = 1000
minPreyFitness = 1000
maxPredatorFitnessList = []
maxPreyFitnessList = []
minPredatorFitnessList = []
minPreyFitnessList = []

def trainPreys(genomes, config):
    preyNetworks, preyGenomes, preys = neatUtils.createEntities(genomes, config, True)
    predatorNetworks, predatorGenomes, predators = neatUtils.createTrainedPredators(30)
    global minPreyFitness
    global maxPreyFitness
    global minPreyFitnessList
    global maxPreyFitnessList

    run = True
    clock = pygame.time.Clock()

    while shouldRun(len(preys), len(predators)) and run:
        timeDelta = clock.tick()/1000.0

        neatUtils.updatePredators(predators, predatorGenomes, predatorNetworks, preys, False, preyGenomes, preyNetworks)
        neatUtils.updatePreys(preys, preyGenomes, preyNetworks, predators)
        for index, p in enumerate(preys):
            if p.die == True:
                if preyGenomes[index].fitness < minPreyFitness:
                    minPreyFitness = preyGenomes[index].fitness
            neatUtils.checkPreyDeath(p, preys, index, preyGenomes, preyNetworks)

        for index, prey in enumerate(preys):    
            if preyGenomes[index].fitness > maxPreyFitness:
                maxPreyFitness = preyGenomes[index].fitness   
 
    maxPreyFitnessList.append(maxPreyFitness)  
    minPreyFitnessList.append(minPreyFitness)  


def trainPredators(genomes, config):
    predatorNetworks, predatorGenomes, predators = neatUtils.createEntities(genomes, config, False)
    preys = [Prey() for _ in range(20)]
    global minPredatorFitness
    global maxPredatorFitness
    global minPredatorFitnessList 
    global maxPredatorFitnessList

    run = True
    clock = pygame.time.Clock()
    while run and (len(predators) > 0):
        timeDelta = clock.tick()/1000.0

        neatUtils.updatePredators(predators, predatorGenomes, predatorNetworks, preys, True, None, None)
        for index, p in enumerate(predators):
            if p.die == True:
                if predatorGenomes[index].fitness < minPredatorFitness:
                    minPredatorFitness = predatorGenomes[index].fitness
            neatUtils.checkPredatorDeath(p, predators, predatorGenomes, predatorNetworks, index)

        for index, predator in enumerate(predators):    
            if predatorGenomes[index].fitness > maxPredatorFitness:
                maxPredatorFitness = predatorGenomes[index].fitness  

    minPredatorFitnessList.append(minPredatorFitness)
    maxPredatorFitnessList.append(maxPredatorFitness)    


def main():
    open("predatorMaxFitness.txt", "w").close()

    local_dir = os.path.dirname(__file__)
    configPath = os.path.join(local_dir, PREDATOR_CONFIG_FILE)
    neatUtils.run(configPath, trainPredators, 2, "winnerPredator.pkl")

    with open("winnerPredator.pkl", "rb") as f:
        genome = pickle.load(f)
        print(f'best predator genome {genome}')

    open("preyMaxFitness.txt", "w").close()    

    configPath = os.path.join(local_dir, PREY_CONFIG_FILE)
    neatUtils.run(configPath, trainPreys, 2, "winnerPrey.pkl")

    with open("winnerPrey.pkl", "rb") as f:
        genome = pickle.load(f)
        print(f'best prey genome {genome}')

    # with open('predatorMaxFitness.txt', 'r') as file:
    #     # Read the entire file as a string
    #     file_contents = file.read()

    #     # Split the string into a list of numbers using commas as the delimiter
    #     numbers_as_strings = file_contents.split(';')
    #     # Convert the strings to integers (or floats if they're not all integers)
    #     fitnessList = [int(number) for number in numbers_as_strings]

    #     # todo plot max fitness over gnerations for predators and preys
    #     x = np.linspace(0, 20, 20)
    #     plt.plot(x, np.array(fitnessList), label='Best predator fitness')

    #     plt.xlabel('Generation')
    #     plt.ylabel('Max fitness')
    #     plt.legend()
    #     plt.show()

    
    # with open('preyMaxFitness.txt', 'r') as file:
    #     # Read the entire file as a string
    #     file_contents = file.read()

    #     # Split the string into a list of numbers using commas as the delimiter
    #     numbers_as_strings = file_contents.split(';')
    #     # Convert the strings to integers (or floats if they're not all integers)
    #     fitnessList = [float(number) for number in numbers_as_strings]

    #     # todo plot max fitness over gnerations for predators and preys
    #     x = np.linspace(0, 20, 20)
    #     plt.plot(x, np.array(fitnessList), label='Best prey fitness')

    #     plt.xlabel('Generation')
    #     plt.ylabel('Max fitness')
    #     plt.legend()
    #     plt.show()    

    print(f'min prey:{minPreyFitnessList}')
    print(f'min predator:{minPredatorFitnessList}')
    print(f'max predator:{maxPredatorFitnessList}')
    print(f'max prey:{maxPreyFitnessList}')

    runTestEnvironment()

if __name__ == "__main__":
    main()   