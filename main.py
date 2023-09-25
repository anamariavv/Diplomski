import os
import pygame
from Entity import *
import neat
import math
import itertools
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 1500, 1000
BLACK = (0, 0, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator-Prey simulation")


def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(main, 200)
    print('\nBest genome:\n{!s}'.format(winner))


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
    
def check_die(predators, my_genomes, neural_networks):
    for index, predator in enumerate(predators):
        if predator.die == True:
            my_genomes[index].fitness -= 20
            predators.pop(index)
            neural_networks.pop(index)
            my_genomes.pop(index)      


def setup_neat_variables(genomes, config):
    neural_networks = []
    my_genomes = []
    predators = []

    for _, g in genomes:
        new_network = neat.nn.FeedForwardNetwork.create(g, config)
        neural_networks.append(new_network)
        predators.append(Predator())
        g.fitness = 0
        my_genomes.append(g)

    return neural_networks, my_genomes, predators

def drawAssistanceLines(predator, closest):
    predator.drawLineToClosestEntity(WIN, closest)
    predator.drawVisionLines(WIN)
    pygame.display.update() 

def drawVisionLines(predators):
    for p in predators:
        p.drawVisionLines(WIN)    

def main(genomes, config):
    neural_networks, my_genomes, predators = setup_neat_variables(genomes, config)
    preys = [Prey() for _ in range(50)]
   
    run = True
    clock = pygame.time.Clock()

    while run:
        #Clock tick
        clock.tick(250)

        #Check if user quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        for predator in predators: 
            predator.updateHungerTimer()

        #End the generation if no entities are left
        if len(predators) == 0:
            run = False
            pass

        for index, predator in enumerate(predators):
            inputs = []

            #Fill the input list for the neural network -> 2 inputs: distance and angle dif to closest food
            closest, distanceToPrey, angleToPrey = predator.getClosest(preys)    
            if closest is not None:
                if math.fabs(angleToPrey) <= 10 and distanceToPrey <= 10 :
                    my_genomes[index].fitness += 0.2
                drawAssistanceLines(predator, closest)
                inputs.append(distanceToPrey)
                inputs.append(angleToPrey)
            else:
                inputs.append(1000)
                inputs.append(0)
        
            #Get the outputs from the neural network (3 - left, right or forward)
            outputs = neural_networks[index].activate((inputs))

            #Move entity based on output
            if outputs[0] > 0.5:
                predator.moveForward()
            elif outputs[1] > 0.5:
                predator.turn_left()
            elif outputs[2] > 0.5:
                predator.turn_right()    

            #Correct the position if they reach edge of screen -> teleport to other end
            predator.x, predator.y = correct_position(predator.x, predator.y)

            #Check if entity has eaten anything or died in this frame
            check_food_eaten(predator, preys, my_genomes, index)
            check_die(predators, my_genomes, neural_networks)
             
        draw_screen(predators, preys)
        drawVisionLines(predators)

    for index, p in enumerate(predators):
        print(f'-------Predator number {index} ate {p.food_eaten} preys and has a fitness of {my_genomes[index].fitness}---------')


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)
