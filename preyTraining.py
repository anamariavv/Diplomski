import os
import pygame
import neatUtils
from prey import *
from predator import *
from constants import *
from pygame.locals import *
from entity import *
from visualisation import *

def shouldRun(numberOfPreys, numberOfpredators):
    if numberOfPreys == 0 or numberOfpredators == 0:
        return False
    return True    

def trainPreys(genomes, config):
    pygame.init()
    pygame.event.set_allowed([QUIT, MOUSEBUTTONUP])
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(PREY_TRAINING_TITLE)

    preyNetworks, preyGenomes, preys = neatUtils.createEntities(genomes, config, True)
    predatorNetworks, predatorGenomes, predators = neatUtils.createTrainedPredators()
    visualisation = Visualisation(WIN)
   
    run = True
    clock = pygame.time.Clock()

    while shouldRun(len(preys), len(predators)) and run:
        timeDelta = clock.tick()/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                visualisation.checkClickForUi(predators + preys, mouseX, mouseY)

            visualisation.processUiEvents(event)

        visualisation.updateTimeDelta(timeDelta)

        neatUtils.updatePredators(predators, predatorGenomes, predatorNetworks, preys, False, preyGenomes, preyNetworks)
        neatUtils.updatePreys(preys, preyGenomes, preyNetworks, predators)

        visualisation.drawSimulation(predators, preys)