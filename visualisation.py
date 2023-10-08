from constants import *
from userInterface import *

class Visualisation:
    def __init__(self, surface):
        self.surface = surface
        self.userInterface = UserInterface(surface, WIDTH, HEIGHT)

    def drawSimulation(self, preys, predators):
        self.surface.fill(BLACK)

        for predator in predators:
            predator.draw(self.surface)

        for prey in preys:
            prey.draw(self.surface)

        self.userInterface.draw()
        self.userInterface.drawAssistanceLines(preys + predators)
        pygame.display.update()    
       
    def checkClickForUi(self, entities, mouseX, mouseY):
        self.userInterface.checkClick(entities, mouseX, mouseY)

    def processUiEvents(self, event):
        self.userInterface.processEvents(event) 

    def updateTimeDelta(self, delta):
        self.userInterface.updateTimeDelta(delta)
