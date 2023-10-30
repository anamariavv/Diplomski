from testEnvironment import *
from constants import *
import numpy as np
import pickle
import visualize
import neat

maxPredatorFitnessList = []
maxPreyFitnessList = []
minPredatorFitnessList = []
minPreyFitnessList = []
numIterations = 200

def trainPreys(preyGenomes, config):
    # pygame.init()
    # pygame.event.set_allowed([QUIT, MOUSEBUTTONUP])
    # WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption(PREY_TRAINING_TITLE)

    preyNetworks, preys = neatUtils.createEntities(preyGenomes, config, True)
    predatorNetworks, predatorGenomes, predators = neatUtils.createTrainedPredators(20, "winnerPredator.pkl")

    # visualisation = Visualisation(WIN)

    global minPreyFitnessList
    global maxPreyFitnessList
    maxPreyFitness = 0
    minPreyFitness = 1000
 
    run = True
    clock = pygame.time.Clock()

    while shouldRun(len(preys), len(predators)) and run:
        timeDelta = clock.tick()/1000.0

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #         pygame.quit()

        #     if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        #         mouseX, mouseY = pygame.mouse.get_pos()
        #         visualisation.checkClickForUi(preys, mouseX, mouseY)

        #     visualisation.processUiEvents(event)

        # visualisation.updateTimeDelta(timeDelta)

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
                    with open("winnerPrey.pkl", "wb") as f:
                        pickle.dump(preyGenomes[index], f)
                        f.close()
        neatUtils.checkPreyDeath(preys, preyGenomes, preyNetworks)  
        
        # visualisation.drawSimulation(predators, preys)   
             
    minPreyFitnessList.append(minPreyFitness)  

def trainPredators(genomes, config):
    # pygame.init()
    # pygame.event.set_allowed([QUIT, MOUSEBUTTONUP])
    # WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption(PREDATOR_TRAINING_TITLE)

    predatorNetworks, predators = neatUtils.createEntities(genomes, config, False)
    preys = [Prey() for _ in range(30)]

    # visualisation = Visualisation(WIN)

    global minPredatorFitnessList 
    global maxPredatorFitnessList
    maxPredatorFitness = 0
    minPredatorFitness = 1000
    
    run = True
    clock = pygame.time.Clock()
    while run and (len(predators) > 0):
        timeDelta = clock.tick()/1000.0

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #         pygame.quit()

        #     if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        #         mouseX, mouseY = pygame.mouse.get_pos()
        #         visualisation.checkClickForUi(preys, mouseX, mouseY)

        #     visualisation.processUiEvents(event)

        # visualisation.updateTimeDelta(timeDelta)
        
        neatUtils.updatePredators(predators, genomes, predatorNetworks, preys)

        for index, p in enumerate(predators):
            preys = neatUtils.checkIdlePreyEaten(p, preys, genomes, index)
            if p.die == True:
                if genomes[index][1].fitness < minPredatorFitness:
                    minPredatorFitness = genomes[index][1].fitness
                if genomes[index][1].fitness > maxPredatorFitness:
                    maxPredatorFitness = genomes[index][1].fitness  
                    maxPredatorFitnessList.append(maxPredatorFitness) 
                    with open("winnerPredator.pkl", "wb") as f:
                        pickle.dump(genomes[index], f)
                        f.close()
                    
        neatUtils.checkPredatorDeaths(predators, genomes, predatorNetworks)

        # visualisation.drawSimulation(predators, preys) 
            
    minPredatorFitnessList.append(minPredatorFitness)
       

def main():
    local_dir = os.path.dirname(__file__)
    configPath = os.path.join(local_dir, PREDATOR_CONFIG_FILE)
    global maxPreyFitnessList

    neatUtils.run(configPath, trainPredators, numIterations, "winnerPredator.pkl")

    with open("winnerPredator.pkl", "rb") as f:
        genome = pickle.load(f)
        print(f'best predator genome {genome}')

    configPath = os.path.join(local_dir, PREY_CONFIG_FILE)
    neatUtils.run(configPath, trainPreys, numIterations, "winnerPrey.pkl")

    with open("winnerPrey.pkl", "rb") as f:
        genome = pickle.load(f)
        print(f'best prey genome {genome}')

    plt.figure()
    x = np.linspace(0, len(maxPredatorFitnessList), len(maxPredatorFitnessList))
    plt.plot(x, np.array(maxPredatorFitnessList), label='Max predator fitness')  
    x = np.linspace(0, len(minPredatorFitnessList), len(minPredatorFitnessList))  
    plt.plot(x, np.array(minPredatorFitnessList), label='Min predator fitness')   
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig('predatorFitness.png')

    plt.figure()
    x = np.linspace(0, len(maxPreyFitnessList), len(maxPreyFitnessList))
    plt.plot(x, np.array(maxPreyFitnessList), label='Max prey fitness')    
    x = np.linspace(0, len(minPreyFitnessList), len(minPreyFitnessList))  
    plt.plot(x, np.array(minPreyFitnessList), label='Min prey fitness')   
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig('preyFitness.png')

    node_names = {-1: 'distance', -2: 'angle', 0: 'left', 1: 'right'}
    with open("winnerPredator.pkl", "rb") as f:
        id, winnerPredator = pickle.load(f)
        predatorConfig = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.path.join(local_dir, PREDATOR_CONFIG_FILE))
        visualize.draw_net(predatorConfig, winnerPredator, True, node_names=node_names)
    with open("winnerPrey.pkl", "rb") as f:
        id, winnerPrey = pickle.load(f)
        preyConfig = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.path.join(local_dir, PREY_CONFIG_FILE))
        visualize.draw_net(preyConfig, winnerPrey, True, node_names=node_names)

    runTestEnvironment()

if __name__ == "__main__":
    main()   