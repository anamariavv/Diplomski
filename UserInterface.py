import pygame
import pygame_gui
from Entity import *

class UserInterface:
    def __init__(self, surface, width, height):
        self.entity = None
        self.surface = surface
        self.drawLines = False
        self.uiManager = pygame_gui.UIManager((width, height))
        self.toggleLinesButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1350, 0), (150, 50)), text='Toggle lines', manager=self.uiManager)
        self.statisticsTextBox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((1350, 50), (150, 100)), html_text="<b>Statistics</b>", manager=self.uiManager)

    def setEntity(self, entity):
        self.entity = entity 

    def highlightActiveEntity(self):
        if self.entity is not None:
            self.entity.drawRectLines(self.surface)
            self.showStatistics

    def showStatistics(self):
        text = ""
        if isinstance(self.entity, Predator):
            text = f'Prey eaten: {self.entity.food_eaten}'
        else:
            text = 'Time survived:'

        self.statisticsTextBox.clear_text_surface()  
        self.statisticsTextBox.append_html_text(text)
    
    def checkClick(self, entities, mouseX, mouseY):
        entityFound = False

        for entity in entities:
            if entity.collidesWithPoint(mouseX, mouseY):
                self.entity = entity
                entityFound = True

        if entityFound == False:
            self.entity = None      

    def draw(self):
        self.uiManager.draw_ui(self.surface)   
        self.highlightActiveEntity()      

    def processEvents(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.toggleLinesButton:
                self.drawLines = not self.drawLines

        self.uiManager.process_events(event)  

    def updateTimeDelta(self, delta):
        self.uiManager.update(delta)          

