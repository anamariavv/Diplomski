import os
import pygame
from Entity import *
import neat
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
    if direction  == 'W':
        return 0
    elif direction == 'A':
        return 1
    elif direction == 'S':
        return 2
    elif direction == 'D':
        return 3  

def choose_direction(index):
    if index  == 0:
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

def check_food_eaten(predators, my_genomes, index):
    predators = predators[:5]
    preys = predators[5:-1]
    for p in predators:   
        for pr in preys:            
            if(p.rect.colliderect(pr.rect)):
                preys.remove(pr)
                p.hunger -= 5
                my_genomes[index].fitness += 30
                p.update_food_eaten()

def check_die(entities, my_genomes, neural_networks):
    for index, e in enumerate(entities):
        if e.die == True:
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
        if(i < 5):
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

x_axis = np.arange(NUM_PREYS)

generation = 0

def main(genomes, config):  
    global generation
 
    neural_networks, my_genomes, entities = setup_neat_variables(genomes, config)
    predators = entities[:5]
    preys = entities[5:15]

    entity_directions = [None for e in entities]

    run = True

    clock = pygame.time.Clock()

    loop = 0
            
    while run:
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        
        for p in predators:
            p.updateHungerTimer()
            
        if len(entities) == 0:
            run = False
            pass
    
        for index, entity in enumerate(entities):  
            inputs = None
        
            if isinstance(entity, Predator):
                inputs = entity.update_sensor(preys)
            else:
                inputs = entity.update_sensor(predators)
            
            if loop > 0:
                inputs.append(direction_to_index(entity_directions[index]))
            else:
                inputs.append(0)

            outputs = neural_networks[index].activate((inputs)) 
            max_index = np.argmax(outputs)

            check_food_eaten(predators, my_genomes, index)
            check_die(entities, my_genomes, neural_networks)
                  
            previous_direction = entity_directions[index]
            
            # print(f'inputs are {inputs},\n outputs are: {outputs}, argmax = {max_index}, value is: {np.max(outputs)}')

            entity_directions[index] = choose_direction(max_index)
        
            entity.move(entity_directions[index])  

            evaluate_direction_change(previous_direction, entity_directions[index], my_genomes, index)
            entity.rect.x, entity.rect.y = correct_position(entity.rect.x, entity.rect.y)
        
        loop += 1

        draw_screen(entities)  

    generation += 1
  

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)
