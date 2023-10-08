import pygame
import pygame_gui
from entity import *
from prey import *
from predator import *

class UserInterface:
    def __init__(self, surface, width, height):
        self.entity = None
        self.surface = surface
        self.drawLines = False
        self.uiManager = pygame_gui.UIManager((width, height))
        self.toggleLinesButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1350, 0), (150, 50)), text='Toggle lines', manager=self.uiManager)
        self.statisticsTextBox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((1300, 50), (200, 100)), html_text="", wrap_to_height=True, manager=self.uiManager)

    def setEntity(self, entity):
        self.entity = entity 

    def drawAssistanceLines(self, entities):
        if self.drawLines == True:
            for entity in entities:
                entity.drawLineToClosestEntity(self.surface)
                entity.drawVisionLines(self.surface)

    def highlightActiveEntity(self):
        if self.entity is not None and self.entity.die == False:
            self.entity.drawRectLines(self.surface)
            self.showStatistics()
        else:
            self.entity = None 
            self.statisticsTextBox.hide()

    def showStatistics(self):
        text = "<b>Statistics</b> \n"
        if isinstance(self.entity, Predator):
            text += f'Prey eaten: {self.entity.food_eaten} \n'
            text += f'Hunger: {self.entity.hunger}'
        else:
            text += "Time survived: {:.2f}s".format(self.entity.timeSurvived)

        self.statisticsTextBox.clear_all_active_effects()
        self.statisticsTextBox.set_text(text)
        self.statisticsTextBox.show()
        
    def checkClick(self, entities, mouseX, mouseY):
        entityFound = False

        for entity in entities:
            if entity.collidesWithPoint(mouseX, mouseY):
                self.entity = entity
                entityFound = True

        if entityFound == False:
            self.entity = None    

    def processEvents(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.toggleLinesButton:
                self.drawLines = not self.drawLines

        self.uiManager.process_events(event)  

    def updateTimeDelta(self, delta):
        self.uiManager.update(delta)    

    def draw(self):
        self.uiManager.draw_ui(self.surface)   
        self.highlightActiveEntity()              

