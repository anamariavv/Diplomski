from testEnvironment import *
from constants import *
import numpy as np
import pickle

maxPredatorFitnessList = []
maxPreyFitnessList = []
minPredatorFitnessList = []
minPreyFitnessList = []
numIterations = 20

def trainPreys(genomes, config):
    preyNetworks, preyGenomes, preys = neatUtils.createEntities(genomes, config, True)
    predatorNetworks, predatorGenomes, predators = neatUtils.createTrainedPredators(20)

    global minPreyFitnessList
    global maxPreyFitnessList

    maxPreyFitness = 0
    minPreyFitness = 1000

    run = True
    clock = pygame.time.Clock()

    while shouldRun(len(preys), len(predators)) and run:
        timeDelta = clock.tick()/1000.0

        neatUtils.updatePredators(predators, predatorNetworks, preys)
        for index, p in enumerate(predators):
            neatUtils.checkFoodEaten(p, preys, predatorGenomes, index)

        predators = neatUtils.checkPredatorDeaths(predators, predatorGenomes, predatorNetworks)
            
        neatUtils.updatePreys(preys, preyGenomes, preyNetworks, predators)
        for index, p in enumerate(preys):
            if p.die == True:
                if preyGenomes[index].fitness < minPreyFitness:
                    minPreyFitness = preyGenomes[index].fitness
                if preyGenomes[index].fitness > maxPreyFitness:
                    maxPreyFitness = preyGenomes[index].fitness   
        preys = neatUtils.checkPreyDeath(preys, preyGenomes, preyNetworks)    
             
    maxPreyFitnessList.append(maxPreyFitness)  
    minPreyFitnessList.append(minPreyFitness)  

def trainPredators(genomes, config):
    predatorNetworks, predatorGenomes, predators = neatUtils.createEntities(genomes, config, False)
    preys = [Prey() for _ in range(40)]

    global minPredatorFitnessList 
    global maxPredatorFitnessList

    maxPredatorFitness = 0
    minPredatorFitness = 1000

    run = True
    clock = pygame.time.Clock()
    while run and (len(predators) > 0):
        timeDelta = clock.tick()/1000.0

        neatUtils.updatePredators(predators, predatorNetworks, preys)

        for index, p in enumerate(predators):
            preys = neatUtils.checkIdlePreyEaten(p, preys, predatorGenomes, index)
            if p.die == True:
                if predatorGenomes[index].fitness < minPredatorFitness:
                    minPredatorFitness = predatorGenomes[index].fitness
                if predatorGenomes[index].fitness > maxPredatorFitness:
                    maxPredatorFitness = predatorGenomes[index].fitness  
        
        predators = neatUtils.checkPredatorDeaths(predators, predatorGenomes, predatorNetworks)
            
           
    minPredatorFitnessList.append(minPredatorFitness)
    maxPredatorFitnessList.append(maxPredatorFitness)    


def main():
    local_dir = os.path.dirname(__file__)
    # configPath = os.path.join(local_dir, PREDATOR_CONFIG_FILE)
    # neatUtils.run(configPath, trainPredators, numIterations, "winnerPredator.pkl")

    # with open("winnerPredator.pkl", "rb") as f:
    #     genome = pickle.load(f)
    #     print(f'best predator genome {genome}')

    # configPath = os.path.join(local_dir, PREY_CONFIG_FILE)
    # neatUtils.run(configPath, trainPreys, numIterations, "winnerPrey.pkl")

    # with open("winnerPrey.pkl", "rb") as f:
    #     genome = pickle.load(f)
    #     print(f'best prey genome {genome}')

    # plt.figure()

    # x = np.linspace(0, numIterations, numIterations)
    # plt.plot(x, np.array(maxPredatorFitnessList), label='Max predator fitness')    
    # plt.plot(x, np.array(minPredatorFitnessList), label='Min predator fitness')   
    # plt.xlabel('Generation')
    # plt.ylabel('Fitness')
    # plt.legend()
    # plt.savefig('predatorFitness.png')
    # plt.show() 

    # plt.plot(x, np.array(maxPreyFitnessList), label='Max prey fitness')    
    # plt.plot(x, np.array(minPreyFitnessList), label='Min prey fitness')   
    # plt.xlabel('Generation')
    # plt.ylabel('Fitness (survival time)')
    # plt.legend()
    # plt.savefig('preyFitness.png')
    # plt.show() 

    runTestEnvironment()

if __name__ == "__main__":
    main()   