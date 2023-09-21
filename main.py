import os
import pygame
from Entity import *
import neat
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

    winner = p.run(main, 1000)
    print('\nBest genome:\n{!s}'.format(winner))


def draw_screen(entities):
    WIN.fill(BLACK)

    for entity in entities:
        entity.draw(WIN)

    pygame.display.update()


def direction_to_index(direction):
    if direction == 'W':
        return 0
    elif direction == 'A':
        return 1
    elif direction == 'S':
        return 2
    elif direction == 'D':
        return 3


def choose_direction(index):
    if index == 0:
        return 'W'
    elif index == 1:
        return 'A'
    elif index == 2:
        return 'S'
    elif index == 3:
        return 'D'


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

    if new_x != x or new_y != y:
        apply_penalty = True

    return new_x, new_y


def check_food_eaten(entities, predator, my_genomes, predator_index, neural_networks):
    for entity_index, entity in enumerate(entities):
        if isinstance(entity, Prey) and predator.rect.colliderect(entity.rect):
            my_genomes[entity_index].fitness -= 10
            entities.pop(entity_index)
            entity.die = True
            neural_networks.pop(entity_index)
            my_genomes.pop(entity_index)

            entities[predator_index].hunger -= 1
            my_genomes[predator_index].fitness += 30


def check_die(entities, my_genomes, neural_networks):
    for index, e in enumerate(entities):
        if e.die == True:
            my_genomes[index].fitness -= 10
            entities.pop(index)
            neural_networks.pop(index)
            my_genomes.pop(index)
    
    count = sum([isinstance(entity, Predator) for entity in entities])
    if count == 0:
        for index, e in enumerate(entities):
            my_genomes[index].fitness -= 10
            entities.pop(index)
            neural_networks.pop(index)
            my_genomes.pop(index)


def setup_neat_variables(genomes, config):
    neural_networks = []
    my_genomes = []
    entities = []

    i = 0
    for _, g in genomes:
        new_network = neat.nn.FeedForwardNetwork.create(g, config)
        neural_networks.append(new_network)
        if (i < 5):
            entities.append(Predator())
        else:
            entities.append(Prey())
        g.fitness = 0
        my_genomes.append(g)
        i += 1

    return neural_networks, my_genomes, entities


def reward_food_proximity(inputs, my_genomes, index):
    min_dist = np.min(inputs)
    max_dist = np.max(inputs)

    if min_dist <= 20:
        my_genomes[index].fitness += 0.01

    if max_dist >= 100:
        my_genomes[index].fitness -= 1


def evaluate_direction_change(old_direction, new_direction, my_genomes, index):
    if old_direction != new_direction:
        my_genomes[index].fitness += 10
        return True
    else:
        my_genomes[index].fitness -= 1

    return False

def rewardForSurvival(my_genomes, index):
    my_genomes[index].fitness += 1/125


x_axis = np.arange(NUM_PREYS)

generation = 0


def main(genomes, config):
    global generation

    neural_networks, my_genomes, entities = setup_neat_variables(genomes, config)

    entity_directions = [None for e in entities]
    
    run = True

    clock = pygame.time.Clock()

    loop = 0

    while run:
        #Clock tick
        clock.tick(250)

        #Check if user quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        #Get predator and prey instances, update hunger for predators
        predators = []
        preys = []

        for e in entities:
            if isinstance(e, Predator):
                e.updateHungerTimer()
                predators.append(e)
            else:
                preys.append(e)

        #End the generation if no entities are left
        if len(entities) == 0:
            run = False
            pass

        for index, entity in enumerate(entities):
            inputs = None

            #Fill the input list for the neural network, 15 sensor rays for each entity
            # + current direction + number representing if they are predator or prey
            #Reward the preys for survival
            if isinstance(entity, Predator):
                inputs = entity.update_sensor(preys)
                inputs.append(2)
            else:
                inputs = entity.update_sensor(predators)
                rewardForSurvival(my_genomes, index)
                inputs.append(0)

            if loop > 0:
                inputs.append(direction_to_index(entity_directions[index]))
            else:
                inputs.append(0)

            #Get the outputs from the neural network (currently 4, one for up, down, left, right)
            outputs = neural_networks[index].activate((inputs))
            max_index = np.argmax(outputs)

            #Map the direction received from NN and move the entity
            entity_directions[index] = choose_direction(max_index)
            entity.move(entity_directions[index])

            #Correct the position if they reach edge of screen -> teleport to other end
            entity.rect.x, entity.rect.y = correct_position(entity.rect.x, entity.rect.y)

            #Check if entity has eaten anything or died in this frame
            if isinstance(entity, Predator):
                check_food_eaten(entities, entity, my_genomes, index, neural_networks)
            check_die(entities, my_genomes, neural_networks)
           
        loop += 1

        draw_screen(entities)

    generation += 1


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)
