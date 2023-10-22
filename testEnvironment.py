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


def shouldRun(numberOfPreys, numberOfpredators):
    if numberOfPreys == 0 or numberOfpredators == 0:
        return False
    return True


def runTestEnvironment():
    pygame.init()
    pygame.event.set_allowed([QUIT, MOUSEBUTTONUP])
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TEST_ENVIRONMENT_TITLE)

    preyNetworks, preyGenomes, preys = neatUtils.createTrainedPreys(30)
    predatorNetworks, predatorGenomes, predators = neatUtils.createTrainedPredators(
        10)
    visualisation = Visualisation(WIN)

    run = True
    clock = pygame.time.Clock()
    iterations = []
    numPreys = []
    numPreys.append(len(preys))
    numPredators = []
    numPredators.append(len(predators))
    loop = 1
    iterations.append(loop)

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

        neatUtils.updatePredators(
            predators, predatorGenomes, predatorNetworks, preys, False, preyGenomes, preyNetworks)
        neatUtils.updatePreys(preys, preyGenomes, preyNetworks, predators)

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
        loop += 1
        iterations.append(loop)

        visualisation.drawSimulation(predators, preys)

    print('End!')
    plt.plot(np.array(iterations), np.array(numPredators), label='number of predators')
    plt.plot(np.array(iterations), np.array(numPreys), label='number of preys')

    plt.xlabel('Iterations')
    plt.ylabel('Number of entities')
    plt.legend()
    plt.show()
