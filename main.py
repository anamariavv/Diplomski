from predatorTraining import *
from preyTraining import *
from testEnvironment import *
from constants import *
import numpy as np

def main():
    open("predatorMaxFitness.txt", "w").close()

    local_dir = os.path.dirname(__file__)
    configPath = os.path.join(local_dir, PREDATOR_CONFIG_FILE)
    neatUtils.run(configPath, trainPredators, 1, "winnerPredator.pkl")

    with open("winnerPredator.pkl", "rb") as f:
        genome = pickle.load(f)
        print(f'best predator genome {genome}')

    open("preyMaxFitness.txt", "w").close()    

    configPath = os.path.join(local_dir, PREY_CONFIG_FILE)
    neatUtils.run(configPath, trainPreys, 1, "winnerPrey.pkl")

    with open("winnerPrey.pkl", "rb") as f:
        genome = pickle.load(f)
        print(f'best prey genome {genome}')

    # with open('predatorMaxFitness.txt', 'r') as file:
    #     # Read the entire file as a string
    #     file_contents = file.read()

    #     # Split the string into a list of numbers using commas as the delimiter
    #     numbers_as_strings = file_contents.split(';')
    #     # Convert the strings to integers (or floats if they're not all integers)
    #     fitnessList = [int(number) for number in numbers_as_strings]

    #     # todo plot max fitness over gnerations for predators and preys
    #     x = np.linspace(0, 20, 20)
    #     plt.plot(x, np.array(fitnessList), label='Best predator fitness')

    #     plt.xlabel('Generation')
    #     plt.ylabel('Max fitness')
    #     plt.legend()
    #     plt.show()

    
    # with open('preyMaxFitness.txt', 'r') as file:
    #     # Read the entire file as a string
    #     file_contents = file.read()

    #     # Split the string into a list of numbers using commas as the delimiter
    #     numbers_as_strings = file_contents.split(';')
    #     # Convert the strings to integers (or floats if they're not all integers)
    #     fitnessList = [float(number) for number in numbers_as_strings]

    #     # todo plot max fitness over gnerations for predators and preys
    #     x = np.linspace(0, 20, 20)
    #     plt.plot(x, np.array(fitnessList), label='Best prey fitness')

    #     plt.xlabel('Generation')
    #     plt.ylabel('Max fitness')
    #     plt.legend()
    #     plt.show()    

    runTestEnvironment()

if __name__ == "__main__":
    main()   