import os
import pygame
from Entity import *
import neat
import pickle
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 1500, 1000
BLACK = (0, 0, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prey training")

def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

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

    
def check_die(preys, my_genomes, neural_networks):
    for index, prey in enumerate(preys):
        if prey.die == True:
            my_genomes[index].fitness -= 20
            preys.pop(index)
            neural_networks.pop(index)
            my_genomes.pop(index)    

def check_food_eatenPredator(predator, preys, my_genomes, predator_index):
    for index, prey in enumerate(preys):
        if(predator.img.get_rect(topleft = (predator.x, predator.y)).colliderect(prey.img.get_rect(topleft = (prey.x, prey.y)))):
            predator.hunger -= 1
            predator.food_eaten += 1
            my_genomes[predator_index].fitness += 5
            prey.die = True
            preys.pop(index)
    
def check_diePredator(predators, my_genomes, neural_networks):
    for index, predator in enumerate(predators):
        if predator.die == True:
            my_genomes[index].fitness -= 20
            predators.pop(index)
            neural_networks.pop(index)
            my_genomes.pop(index)      

def rewardForSurvival(prey, my_genomes, index):
    my_genomes[index].fitness += 0.01

def setup_neat_variables(genomes, config):
    neural_networks = []
    my_genomes = []
    preys = []

    for _, g in genomes:
        new_network = neat.nn.FeedForwardNetwork.create(g, config)
        neural_networks.append(new_network)
        preys.append(Prey())
        g.fitness = 0
        my_genomes.append(g)

    return neural_networks, my_genomes, preys

def drawAssistanceLines(predator, closest):
    predator.drawLineToClosestEntity(WIN, closest)
    predator.drawVisionLines(WIN)
    pygame.display.update() 

def drawVisionLines(predators):
    for p in predators:
        p.drawVisionLines(WIN)   

def createPredatorsFromGenome():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)         
    
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


def main(predatorGenomes, config):
    neural_networks, my_genomes, preys = setup_neat_variables(predatorGenomes, config)
    predatorNetworks, predatorGenomes, predators = createPredatorsFromGenome()
   
    run = True
    clock = pygame.time.Clock()

    # for prey in preys:
    #     prey.startSurvivalTimer()

    while run:
        clock.tick(250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        for predator in predators: 
            predator.updateHungerTimer()        

        if len(preys)== 0 or len(predators) == 0:
            run = False
            pass

        for index, prey in enumerate(preys):
            inputs = []

            #prey.updateSurvivalTimer()
            
            rewardForSurvival(prey, my_genomes, index)

            closest, distanceToThreat, angleToThreat = prey.getClosest(predators)    
            if closest is not None:
                drawAssistanceLines(prey, closest)
                inputs.append(distanceToThreat)
                inputs.append(angleToThreat)
            else:
                inputs.append(0)
                inputs.append(180)
        
            outputs = neural_networks[index].activate((inputs))

            if outputs[0] > 0.5:
                prey.moveForward()
            elif outputs[1] > 0.5:
                prey.turn_left()
            elif outputs[2] > 0.5:
                prey.turn_right()    

            prey.x, prey.y = correct_position(prey.x, prey.y)

            check_die(preys, my_genomes, neural_networks)

        for index, predator in enumerate(predators):
            inputs = []

            closest, distanceToPrey, angleToPrey = predator.getClosest(preys)    
            if closest is not None:
                #drawAssistanceLines(predator, closest)
                inputs.append(distanceToPrey)
                inputs.append(angleToPrey)
            else:
                inputs.append(1000)
                inputs.append(0)
        
            outputs = predatorNetworks[index].activate((inputs))

            if outputs[0] > 0.5:
                predator.moveForward()
            elif outputs[1] > 0.5:
                predator.turn_left()
            elif outputs[2] > 0.5:
                predator.turn_right()    

            predator.x, predator.y = correct_position(predator.x, predator.y)

            check_food_eatenPredator(predator, preys, predatorGenomes, index)
            check_diePredator(predators, predatorGenomes, neural_networks)    
             
        draw_screen(predators, preys)

    for index, p in enumerate(preys):
        print(f'-------Prey number {index} has a fitness of {my_genomes[index].fitness}---------')

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config-prey.txt')
    run(config_path)
