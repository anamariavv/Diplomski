import os
import pygame
import neatUtils
from entity import *
from prey import *
from predator import *
from entity import *
from constants import *
from pygame.locals import *
from visualisation import *

def trainPredators(genomes, config):
    pygame.init()
    pygame.event.set_allowed([QUIT, MOUSEBUTTONUP])
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(PREDATOR_TRAINING_TITLE)
    
    predatorNetworks, predatorGenomes, predators = neatUtils.createEntities(genomes, config, False)
    preys = [Prey() for _ in range(30)]
    visualisation = Visualisation(WIN)

    run = True
    clock = pygame.time.Clock()

    while run and (len(predators) > 0):
        timeDelta = clock.tick()/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                visualisation.checkClickForUi(preys, mouseX, mouseY)

            visualisation.processUiEvents(event)

        visualisation.updateTimeDelta(timeDelta)

        neatUtils.updatePredators(predators, predatorGenomes, predatorNetworks, preys, True, None, None)
        visualisation.drawSimulation(predators, preys)
