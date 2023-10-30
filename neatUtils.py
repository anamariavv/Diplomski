from constants import *
from prey import *
from predator import *
import neat
import pickle
import random
import visualize
from neat import math_util

def run(configPath, function, iterations, outFileName):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    population.run(function, iterations)

def createEntities(genomes, config, isPrey):
    neuralNetworks = []
    entities = []

    for _, g in genomes:
        new_network = neat.nn.FeedForwardNetwork.create(g, config)
        neuralNetworks.append(new_network)
        if isPrey:
            entities.append(Prey())
        else:
            entities.append(Predator())
        g.fitness = 0

    return neuralNetworks, entities

def createTrainedPredators(n, filename):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    predators = []
    genomes = []
    predatorNetworks = []

    with open(filename, "rb") as f:
        id, genome = pickle.load(f)
        for _ in range(n):
            genomes.append(genome)
            predators.append(Predator())
            predatorNetwork = neat.nn.FeedForwardNetwork.create(genome, config)
            predatorNetworks.append(predatorNetwork)

    return predatorNetworks, genomes, predators


def createTrainedPreys(n, filename):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config-prey.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    preys = []
    genomes = []
    preyNetworks = []

    with open(filename, "rb") as f:
        id, genome = pickle.load(f)
        for _ in range(n):
            genomes.append(genome)
            preys.append(Prey())
            preyNetwork = neat.nn.FeedForwardNetwork.create(genome, config)
            preyNetworks.append(preyNetwork)

    return preyNetworks, genomes, preys


def correctPosition(currentX, currentY):
    newX, newY = currentX, currentY

    if currentX >= WIDTH:
        newX = 0
    if currentX <= 0:
        newX = WIDTH
    if currentY >= HEIGHT:
        newY = 0
    if currentY <= 0:
        newY = HEIGHT

    return newX, newY


def checkPredatorDeaths(predators, predatorGenomes, predatorNetworks):
    deadPredators = []

    for index, p in enumerate(predators):
        if p.die == True:
            predatorGenomes[index][1].fitness -=30
            deadPredators.append(index)

    for i in reversed(deadPredators):
        predators.pop(i)
        predatorNetworks.pop(i)
        predatorGenomes.pop(i)

    return predators    
            
def checkTrainedPredatorDeaths(predators, predatorGenomes, predatorNetworks):
    deadPredators = []

    for index, p in enumerate(predators):
        if p.die == True:
            predatorGenomes[index].fitness -= 30
            deadPredators.append(index)

    for i in reversed(deadPredators):
        predators.pop(i)
        predatorNetworks.pop(i)
        predatorGenomes.pop(i)

    return predators    

def checkFoodEaten(predator, preys, predatorGenomes, predatorIndex):
    for preyIndex, prey in enumerate(preys):
        if (predator.img.get_rect(topleft=(predator.x, predator.y)).colliderect(prey.img.get_rect(topleft=(prey.x, prey.y)))):
            if predator.hunger >= 1:
                predator.hunger -= 1
            predator.food_eaten += 1  
            predatorGenomes[predatorIndex].fitness += 5
            prey.die = True
       

def checkTrainedPreyDeath(preys, preyGenomes, preyNetworks):
    deadPreys = []

    for index, p in enumerate(preys):
        if p.die == True:  
            preyGenomes[index].fitness -= 30
            deadPreys.append(index)

    for i in reversed(deadPreys):
        preys.pop(i)   
        preyNetworks.pop(i) 
        preyGenomes.pop(i)

    return preys         

def checkPreyDeath(preys, preyGenomes, preyNetworks):
    deadPreys = []

    for index, p in enumerate(preys):
        if p.die == True:  
            preyGenomes[index][1].fitness -= 50
            deadPreys.append(index)

    for i in reversed(deadPreys):
        preys.pop(i)   
        preyNetworks.pop(i) 
        preyGenomes.pop(i)

    return preys         


def checkIdlePreyEaten(predator, preys, predatorGenomes, predatorIndex):
    deadPreys = []

    for preyIndex, prey in enumerate(preys):
        if (predator.img.get_rect(topleft=(predator.x, predator.y)).colliderect(prey.img.get_rect(topleft=(prey.x, prey.y)))):
            if predator.hunger >= 1:
                predator.hunger -= 1
            predator.food_eaten += 1
            predatorGenomes[predatorIndex][1].fitness += 5    
            prey.die = True
            deadPreys.append(preyIndex)
    
    for i in reversed(deadPreys):
        preys.pop(i)

    return preys    


def reward(genomes, index, amount):
    genomes[index][1].fitness += amount

def processOutputs(outputs, entity):

    if outputs[0] > 0.5:
        entity.turn_right()
    else:
        entity.turn_left()  

def updatePredators(predators, genomes, predatorNetworks, preys):
    for index, predator in enumerate(predators):
        inputs = []

        predator.updateHungerTimer()

        closest, distanceToPrey, angleToPrey = predator.getClosest(preys)
        if closest is not None:
            inputs.append(distanceToPrey)
            inputs.append(angleToPrey)
            # fitness = -0.1 * distanceToPrey + 25
            # genomes[index][1].fitness += fitness
        else:
            inputs.append(185)
            inputs.append(0)

        outputs = predatorNetworks[index].activate((inputs))
        processOutputs(outputs, predator)

        predator.x, predator.y = correctPosition(predator.x, predator.y)   

def updateTrainedPredators(predators, genomes, predatorNetworks, preys):
    for index, predator in enumerate(predators):
        inputs = []

        predator.updateHungerTimer()

        closest, distanceToPrey, angleToPrey = predator.getClosest(preys)
        if closest is not None:
            inputs.append(distanceToPrey)
            inputs.append(angleToPrey)
            fitness = -0.1 * distanceToPrey + 25
            genomes[index].fitness += fitness
        else:
            inputs.append(185)
            inputs.append(0)

        outputs = predatorNetworks[index].activate((inputs))
        processOutputs(outputs, predator)

        predator.x, predator.y = correctPosition(predator.x, predator.y)        


def updateTrainedPreys(preys, preyGenomes, preyNetworks, predators):
    for index, prey in enumerate(preys):
        inputs = []

        prey.updateSurvivalTime()
        preyGenomes[index].fitness += 0.1

        closest, distanceToThreat, angleToThreat = prey.getClosest(predators)
        if closest is not None:
            inputs.append(distanceToThreat)
            inputs.append(angleToThreat)
        else:
            inputs.append(75)
            inputs.append(180)
        
        outputs = preyNetworks[index].activate((inputs))       
        processOutputs(outputs, prey)

        prey.x, prey.y = correctPosition(prey.x, prey.y)

def updatePreys(preys, preyGenomes, preyNetworks, predators):
    for index, prey in enumerate(preys):
        inputs = []

        prey.updateSurvivalTime()
        reward(preyGenomes, index, 0.01)

        closest, distanceToThreat, angleToThreat = prey.getClosest(predators)
        if closest is not None:
            inputs.append(distanceToThreat)
            inputs.append(angleToThreat)
            if prey.isClosestInDangerZone():
                fitness = -0.25 * distanceToThreat + 25
                preyGenomes[index][1].fitness -= fitness
            else:
                preyGenomes[index][1].fitness += 1
        else:
            inputs.append(185)
            inputs.append(180)
        
        outputs = preyNetworks[index].activate((inputs))       
        processOutputs(outputs, prey)

        prey.x, prey.y = correctPosition(prey.x, prey.y)

def updateReproductionTimer(entities):
    for e in entities:
        e.updateReproductionTimer()        

def checkReproductionChance(entity, entities, genomes, networks, isPrey):
    if entity.canReproduce == True:
        n = random.random()

        if(isPrey and len(entities) > 0 and len(entities) < 50):
            if (n < 0.3):
                local_dir = os.path.dirname(__file__)
                config_path = os.path.join(local_dir, 'neat-config-prey.txt')
                config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
                with open("winnerPrey.pkl", "rb") as f:
                    id, genome = pickle.load(f)
                    genomes.append(genome)
                    networks.append(neat.nn.FeedForwardNetwork.create(genome, config))
                    entities.append(Prey())     
        elif(len(entities) > 0 and len(entities) < 25 and entity.hunger < 2):
            if(n < 0.5):
                local_dir = os.path.dirname(__file__)
                config_path = os.path.join(local_dir, 'neat-config.txt')
                config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
                with open("winnerPredator.pkl", "rb") as f:
                    id, genome = pickle.load(f)
                    genomes.append(genome)
                    networks.append(neat.nn.FeedForwardNetwork.create(genome, config))
                    entities.append(Predator())

    entity.canReproduce = False