from testEnvironment import *
from constants import *
import numpy as np
import pickle
import visualize
import neat
import myCheckpointer

maxPredatorFitnessList = []
maxPreyFitnessList = []
minPredatorFitnessList = []
minPreyFitnessList = []
predatorGenerationNum = 0
preyGenerationNum = 0
lastCheckPointPredator = None
lastCheckPointPrey = None

def runWithoutCheckpoint(configPath, function, iterations, isPrey):
    global predatorGenerationNum
    global preyGenerationNum
    global lastCheckPointPredator
    global lastCheckPointPrey

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    population.run(function, iterations)

    prefix = None
    generation = None

    if isPrey:
        prefix = "prey-checkpoint-"
        generation = preyGenerationNum
        lastCheckPointPrey = prefix+str(predatorGenerationNum)
        myCheckpointer.MyCheckpointer.save_checkpoint(config, population, population.species, generation, prefix)
    else:
        prefix = "predator-checkpoint-"   
        generation = predatorGenerationNum
        lastCheckPointPredator = prefix+str(predatorGenerationNum) 
        myCheckpointer.MyCheckpointer.save_checkpoint(config, population, population.species, generation, prefix)

def runFromCheckpoint(configPath, function, iterations, isPrey):
    global predatorGenerationNum
    global preyGenerationNum
    global lastCheckPointPredator
    global lastCheckPointPrey

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

    population = None
    if isPrey:
        population = myCheckpointer.MyCheckpointer.restore_checkpoint(lastCheckPointPrey)
    else:
        population = myCheckpointer.MyCheckpointer.restore_checkpoint(lastCheckPointPredator)    

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    population.run(function, iterations)
    
    if isPrey:
        prefix = "prey-checkpoint-"
        generation = preyGenerationNum
        lastCheckPointPrey = prefix+str(predatorGenerationNum)
        myCheckpointer.MyCheckpointer.save_checkpoint(config, population, population.species, generation, prefix)
    else:
        prefix = "predator-checkpoint-"   
        generation = predatorGenerationNum
        lastCheckPointPredator = prefix+str(predatorGenerationNum) 
        myCheckpointer.MyCheckpointer.save_checkpoint(config, population, population.species, generation, prefix)

def trainPredatorsStagnant(genomes, config):
    predatorNetworks, predators = neatUtils.createEntities(genomes, config, False)
    preys = [Prey() for _ in range(30)]

    global minPredatorFitnessList 
    global maxPredatorFitnessList
    global predatorGenerationNum

    maxPredatorFitness = 0
    minPredatorFitness = 1000
    
    run = True
    clock = pygame.time.Clock()
    while run and (len(predators) > 0):
        timeDelta = clock.tick()/1000.0
        
        neatUtils.updatePredators(predators, genomes, predatorNetworks, preys)

        for index, p in enumerate(predators):
            preys = neatUtils.checkIdlePreyEaten(p, preys, genomes, index)
            if p.die == True:
                if genomes[index][1].fitness < minPredatorFitness:
                    minPredatorFitness = genomes[index][1].fitness
                if genomes[index][1].fitness > maxPredatorFitness:
                    maxPredatorFitness = genomes[index][1].fitness  
                    maxPredatorFitnessList.append(maxPredatorFitness) 
                    with open("winnerPredatorAlternate.pkl", "wb") as f:
                        pickle.dump(genomes[index], f)
                        f.close()
                    
        neatUtils.checkPredatorDeaths(predators, genomes, predatorNetworks)
            
    minPredatorFitnessList.append(minPredatorFitness)
    predatorGenerationNum += 1


def trainPredators(predatorGenomes, config):
    global minPredatorFitnessList 
    global maxPredatorFitnessList
    global predatorGenerationNum

    preyNetworks, preyGenomes, preys  = neatUtils.createTrainedPreys(20, "winnerPreyAlternate.pkl")
    predatorNetworks, predators = neatUtils.createEntities(predatorGenomes, config, False)
 
    run = True
    clock = pygame.time.Clock()

    while shouldRun(len(preys), len(predators)) and run:
        timeDelta = clock.tick()/1000.0

        neatUtils.updatePredators(predators, predatorGenomes, predatorNetworks, preys)
        for index, p in enumerate(predators):
            neatUtils.checkFoodEaten(p, preys, predatorGenomes, index)

        neatUtils.checkPredatorDeaths(predators, predatorGenomes, predatorNetworks)
        neatUtils.updateTrainedPreys(preys, preyGenomes, preyNetworks, predators)

        for index, p in enumerate(preys):
            if p.die == True:
                if predatorGenomes[index][1].fitness < minPredatorFitness:
                    minPredatorFitness = predatorGenomes[index][1].fitness
                if predatorGenomes[index][1].fitness > maxPredatorFitness:
                    maxPredatorFitness = predatorGenomes[index][1].fitness  
                    maxPredatorFitnessList.append(maxPredatorFitness) 
                    with open("winnerPredatorAlternate.pkl", "wb") as f:
                        pickle.dump(predatorGenomes[index], f)
                        f.close()
        neatUtils.checkPreyDeath(preys, preyGenomes, preyNetworks)  
        
    minPredatorFitnessList.append(minPredatorFitness) 
    predatorGenerationNum += 1     


def trainPreys(preyGenomes, config): 
    global minPreyFitnessList
    global maxPreyFitnessList
    global preyGenerationNum

    preyNetworks, preys = neatUtils.createEntities(preyGenomes, config, True)
    predatorNetworks, predatorGenomes, predators = neatUtils.createTrainedPredators(20, "winnerPredatorAlternate.pkl")
  
    maxPreyFitness = 0
    minPreyFitness = 1000
 
    run = True
    clock = pygame.time.Clock()

    while shouldRun(len(preys), len(predators)) and run:
        timeDelta = clock.tick()/1000.0

        neatUtils.updateTrainedPredators(predators, predatorGenomes, predatorNetworks, preys)
        for index, p in enumerate(predators):
            neatUtils.checkFoodEaten(p, preys, predatorGenomes, index)

        neatUtils.checkTrainedPredatorDeaths(predators, predatorGenomes, predatorNetworks)
        neatUtils.updatePreys(preys, preyGenomes, preyNetworks, predators)

        for index, p in enumerate(preys):
            if p.die == True:
                if preyGenomes[index][1].fitness < minPreyFitness:
                    minPreyFitness = preyGenomes[index][1].fitness
                if preyGenomes[index][1].fitness > maxPreyFitness:
                    maxPreyFitness = preyGenomes[index][1].fitness  
                    maxPreyFitnessList.append(maxPreyFitness)  
                    with open("winnerPreyAlternate.pkl", "wb") as f:
                        pickle.dump(preyGenomes[index], f)
                        f.close()
        neatUtils.checkPreyDeath(preys, preyGenomes, preyNetworks)  
        
    minPreyFitnessList.append(minPreyFitness) 
    preyGenerationNum += 1     

def main():
    local_dir = os.path.dirname(__file__)
    predatorConfigPath = os.path.join(local_dir, PREDATOR_CONFIG_FILE)
    preyConfigPath = os.path.join(local_dir, PREY_CONFIG_FILE)

    for i in range(3):
        if i == 0:
            runWithoutCheckpoint(predatorConfigPath, trainPredatorsStagnant, 3, False)
            runWithoutCheckpoint(preyConfigPath, trainPreys, 3, True)
        else:
            runFromCheckpoint(predatorConfigPath, trainPredators, 3, False)    
            runFromCheckpoint(preyConfigPath, trainPreys, 3, True)

    # runTestEnvironment()

if __name__ == "__main__":
    main()   