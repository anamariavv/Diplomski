import os
import pygame
from Entity import *
from UserInterface import *
import neat
import pickle
import pygame_gui
import matplotlib.pyplot as plt

pygame.init()

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
    with open("winnerPrey.pkl", "wb") as f:
        pickle.dump(winner,f)
        f.close()

def draw_screen(predators, preys, interface):
    WIN.fill(BLACK)

    for predator in predators:
        predator.draw(WIN)

    for prey in preys:
        prey.draw(WIN)

    interface.draw()
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

def drawAssistanceLines(entity, closest, interface):
    if interface.drawLines == True:
        entity.drawLineToClosestEntity(WIN, closest)
        entity.drawVisionLines(WIN)
        pygame.display.update() 

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

def checkDeath(predator, predators, predatorGenomes, predatorNetworks, index):
    if predator.die == True:
        predatorGenomes[index].fitness -= 20
        predators.pop(index)
        predatorNetworks.pop(index)
        predatorGenomes.pop(index)   

def checkFoodEaten(predator, preys, predatorGenomes, predatorIndex, preyGenomes, preyNetworks):
    for preyIndex, prey in enumerate(preys):
        if(predator.img.get_rect(topleft = (predator.x, predator.y)).colliderect(prey.img.get_rect(topleft = (prey.x, prey.y)))):
            predator.hunger -= 1
            predator.food_eaten += 1
            predatorGenomes[predatorIndex].fitness += 5
            prey.die = True
            preys.pop(preyIndex),
            preyGenomes[preyIndex].fitness -= 20
            preyNetworks.pop(preyIndex)               

def main(predatorGenomes, config):
    preyNetworks, preyGenomes, preys = setup_neat_variables(predatorGenomes, config)
    predatorNetworks, predatorGenomes, predators = createPredatorsFromGenome()
    allEntities = predators + preys
    drawLines = False
    interface = UserInterface(WIN, WIDTH, HEIGHT)
   
    run = True
    clock = pygame.time.Clock()

    while run:
        time_delta = clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    interface.checkClick(allEntities, mouseX, mouseY)

            interface.processEvents(event) 

        interface.updateTimeDelta(time_delta) 

        for predator in predators: 
            predator.updateHungerTimer()        

        if len(preys)== 0 or len(predators) == 0:
            run = False
            pass

        for index, predator in enumerate(predators):
            inputs = []

            closest, distanceToPrey, angleToPrey = predator.getClosest(preys)    
            if closest is not None:
                drawAssistanceLines(predator, closest, interface)
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

            checkFoodEaten(predator, preys, predatorGenomes, index, preyGenomes, preyNetworks)
            checkDeath(predator, predators, predatorGenomes, predatorNetworks, index)   

        for index, prey in enumerate(preys):
            inputs = []
            
            rewardForSurvival(prey, preyGenomes, index)

            closest, distanceToThreat, angleToThreat = prey.getClosest(predators)    
            if closest is not None:
                drawAssistanceLines(prey, closest, interface)
                inputs.append(distanceToThreat)
                inputs.append(angleToThreat)
            else:
                inputs.append(0)
                inputs.append(180)
        
            outputs = preyNetworks[index].activate((inputs))

            if outputs[0] > 0.5:
                prey.moveForward()
            elif outputs[1] > 0.5:
                prey.turn_left()
            elif outputs[2] > 0.5:
                prey.turn_right()    

            prey.x, prey.y = correct_position(prey.x, prey.y)

        draw_screen(predators, preys, interface)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config-prey.txt')
    run(config_path)
