import os
import pygame
from entity import *
from prey import *
from predator import *
import neat
import pickle
import neatUtils

WIDTH, HEIGHT = 1500, 1000
BLACK = (0, 0, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator training")

def draw_screen(predators, preys):
    WIN.fill(BLACK)

    for predator in predators:
        predator.draw(WIN)

    for prey in preys:
        prey.draw(WIN)

    pygame.display.update()

def correct_position(x, y):
    new_x, new_y = x, y

    if x >= WIDTH:
        new_x = 0
    if x <= 0:
        new_x = WIDTH
    if y >= HEIGHT:
        new_y = 0
    if y <= 0:
        new_y = HEIGHT

    return new_x, new_y


def check_food_eaten(predator, preys, my_genomes, predator_index):
    for index, prey in enumerate(preys):
        if(predator.img.get_rect(topleft = (predator.x, predator.y)).colliderect(prey.img.get_rect(topleft = (prey.x, prey.y)))):
            predator.hunger -= 1
            predator.food_eaten += 1
            my_genomes[predator_index].fitness += 5
            prey.die = True
            preys.pop(index)

def drawAssistanceLines(predator, closest):
    predator.drawLineToClosestEntity(WIN, closest)
    predator.drawVisionLines(WIN)
    pygame.display.update() 

def drawVisionLines(predators):
    for p in predators:
        p.drawVisionLines(WIN)    


def main(genomes, config):
    predatorNetworks, predatorGenomes, predators = neatUtils.createEntities(genomes, config, False)
    preys = [Prey() for _ in range(50)]
   
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if len(predators) == 0:
            run = False
            pass

        neatUtils.updatePredators(predators, predatorGenomes, predatorNetworks, preys, None, None, True)

        draw_screen(predators, preys)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    configPath = os.path.join(local_dir, 'neat-config.txt')
    neatUtils.run(configPath, main, 200, "winnerPredator.pkl")
