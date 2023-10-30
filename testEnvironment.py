import os
import pygame
import neatUtils
from prey import *
from predator import *
from constants import *
from pygame.locals import *
from entity import *
from visualisation import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def shouldRun(numberOfPreys, numberOfpredators):
    if numberOfPreys == 0 or numberOfpredators == 0:
        return False
    return True


def runTestEnvironment():
    pygame.init()
    pygame.event.set_allowed([QUIT, MOUSEBUTTONUP])
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TEST_ENVIRONMENT_TITLE)

    preyNetworks, preyGenomes, preys = neatUtils.createTrainedPreys(30, "winnerPrey.pkl")
    predatorNetworks, predatorGenomes, predators = neatUtils.createTrainedPredators(10, "winnerPredator.pkl")
    visualisation = Visualisation(WIN)

    run = True
    clock = pygame.time.Clock()

    numPreys = []
    numPreys.append(len(preys))
    numPredators = []
    numPredators.append(len(predators))

    for p in preys:
        p.startReproductionTimer()

    for p in predators:
        p.startReproductionTimer()

    while shouldRun(len(preys), len(predators)) and run:
        timeDelta = clock.tick()/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                visualisation.checkClickForUi(
                    predators + preys, mouseX, mouseY)

            visualisation.processUiEvents(event)

        visualisation.updateTimeDelta(timeDelta)

        neatUtils.updateTrainedPredators(predators, predatorGenomes, predatorNetworks, preys)

        for index, p in enumerate(predators):
            neatUtils.checkFoodEaten(p, preys, predatorGenomes, index)
            
        neatUtils.checkTrainedPredatorDeaths(predators, predatorGenomes, predatorNetworks)

        neatUtils.updateTrainedPreys(preys, preyGenomes, preyNetworks, predators)

        for index, p in enumerate(preys):
            preys = neatUtils.checkTrainedPreyDeath(preys, preyGenomes, preyNetworks)  

        neatUtils.updateReproductionTimer(predators)
        neatUtils.updateReproductionTimer(preys)

        for p in predators:
            neatUtils.checkReproductionChance(
                p, predators, predatorGenomes, predatorNetworks, False)

        for p in preys:
            neatUtils.checkReproductionChance(
                p, preys, preyGenomes, preyNetworks, True)

        numPredators.append(len(predators))
        numPreys.append(len(preys))
        visualisation.drawSimulation(predators, preys)

    print('End!')

    x1 = np.linspace(0, len(numPredators), len(numPredators))

    y1_data = np.array(numPredators)
    y2_data= np.array(numPreys)
    cubic_interpolation_model_1 = interp1d(x1, y1_data, kind = "cubic")
    cubic_interpolation_model_2 = interp1d(x1, y2_data, kind = "cubic")
    
    X = np.linspace(x1.min(), x1.max(), 500)
    y1 = cubic_interpolation_model_1(X) 
    y2 = cubic_interpolation_model_2(X)

    plt.figure()
    
    plt.plot(X, y1, label='number of predators')
    plt.plot(X, y2, label='number of preys')
    plt.xlabel('Iteration')
    plt.ylabel('Number of entities')
    plt.legend()
    plt.savefig('numberOfPredatorsAndPreys.png')
    plt.show()
