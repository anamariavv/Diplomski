from constants import *
from prey import *
from predator import *
import neat
import pickle

def run(configPath, function, iterations, outFileName):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(function, iterations)
    
    print('\nBest genome:\n{!s}'.format(winner))
    with open(outFileName, "wb") as f:
        pickle.dump(winner,f)
        f.close()

def createEntities(genomes, config, isPrey):
    neuralNetworks = []
    myGenomes = []
    entities = []

    for _, g in genomes:
        new_network = neat.nn.FeedForwardNetwork.create(g, config)
        neuralNetworks.append(new_network)
        if isPrey:
            entities.append(Prey())
        else:
            entities.append(Predator())   
        g.fitness = 0
        myGenomes.append(g)

    return neuralNetworks, myGenomes, entities


def createTrainedPredators():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    predators = []
    genomes = []
    predatorNetworks = []

    with open("winner.pkl", "rb") as f:
        genome = pickle.load(f)
        for _ in range(10):
            genomes.append(genome)
            predators.append(Predator())
            predatorNetwork = neat.nn.FeedForwardNetwork.create(genome, config)
            predatorNetworks.append(predatorNetwork)

    return predatorNetworks, genomes, predators

def createTrainedPreys():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config-prey.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)      

    preys = []
    genomes = []
    preyNetworks = []

    with open("winnerPrey.pkl", "rb") as f:
        genome = pickle.load(f)
        for _ in range(30):
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


def checkPredatorDeath(predator, predators, predatorGenomes, predatorNetworks, index):
    if predator.die == True:
        predatorGenomes[index].fitness -= 20
        predators.pop(index)
        predatorNetworks.pop(index)
        predatorGenomes.pop(index)


def checkFoodEaten(predator, preys, predatorGenomes, predatorIndex, preyGenomes, preyNetworks):
    for preyIndex, prey in enumerate(preys):
        if (predator.img.get_rect(topleft=(predator.x, predator.y)).colliderect(prey.img.get_rect(topleft=(prey.x, prey.y)))):
            predator.hunger -= 1
            predator.food_eaten += 1
            predatorGenomes[predatorIndex].fitness += 5
            prey.die = True
            prey.stopSurvivalTime()
            preys.pop(preyIndex),
            preyGenomes[preyIndex].fitness -= 20
            preyNetworks.pop(preyIndex)

def checkIdlePreyEaten(predator, preys, predatorGenomes, predatorIndex):
    for preyIndex, prey in enumerate(preys):
        if (predator.img.get_rect(topleft=(predator.x, predator.y)).colliderect(prey.img.get_rect(topleft=(prey.x, prey.y)))):
            predator.hunger -= 1
            predator.food_eaten += 1
            predatorGenomes[predatorIndex].fitness += 5
            prey.die = True
            preys.pop(preyIndex)

def reward(genomes, index, amount):
    genomes[index].fitness += amount

def punish(genomes, index, amount):
    genomes[index].fitness -= amount    

def processOutputs(outputs, entity):       
    if outputs[0] > 0.5:
        entity.moveForward()
    elif outputs[1] > 0.5:
        entity.turn_left()
    elif outputs[2] > 0.5:
        entity.turn_right()

def updatePredators(predators, predatorGenomes, predatorNetworks, preys, isPreyIdle, preyGenomes, preyNetworks):
    for index, predator in enumerate(predators):
        inputs = []

        predator.updateHungerTimer()

        closest, distanceToPrey, angleToPrey = predator.getClosest(preys)
        if closest is not None:
            inputs.append(distanceToPrey)
            inputs.append(angleToPrey)
        else:
            inputs.append(1000)
            inputs.append(0)

        outputs = predatorNetworks[index].activate((inputs))
        processOutputs(outputs, predator)

        predator.x, predator.y = correctPosition(predator.x, predator.y)

        if isPreyIdle:
            checkIdlePreyEaten(predator, preys, predatorGenomes, index)
        else:    
            checkFoodEaten(predator, preys, predatorGenomes, index, preyGenomes, preyNetworks)

        checkPredatorDeath(predator, predators,predatorGenomes, predatorNetworks, index)


def updatePreys(preys, preyGenomes, preyNetworks, predators):
    for index, prey in enumerate(preys):
        inputs = []

        prey.updateSurvivalTime()
        reward(preyGenomes, index, 0.01)

        closest, distanceToThreat, angleToThreat = prey.getClosest(
            predators)
        if closest is not None:
            inputs.append(distanceToThreat)
            inputs.append(angleToThreat)
        else:
            inputs.append(0)
            inputs.append(180)

        outputs = preyNetworks[index].activate((inputs))
        processOutputs(outputs, prey)

        prey.x, prey.y = correctPosition(prey.x, prey.y)
