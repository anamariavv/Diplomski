from predatorTraining import *
from preyTraining import *
from testEnvironment import *
from constants import *

def main():
    local_dir = os.path.dirname(__file__)
    configPath = os.path.join(local_dir, PREDATOR_CONFIG_FILE)
    neatUtils.run(configPath, trainPredators, 1, "winnerPredator.pkl")

    configPath = os.path.join(local_dir, PREY_CONFIG_FILE)
    neatUtils.run(configPath, trainPreys, 1, "winnerPrey.pkl")

    runTestEnvironment()

if __name__ == "__main__":
    main()   