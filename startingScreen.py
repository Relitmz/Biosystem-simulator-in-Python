from constants import *
import pygame
from pygame.locals import *
from fonts import *

class StartingScreen:
    def __init__(self):
        self.changeStage = False
        #Imagen
        self.img = pygame.image.load("sprites/ecosystem.png")
        self.background_width = SCREEN_WIDTH
        self.background_height = SCREEN_HEIGHT
        self.img = pygame.transform.scale(self.img, (self.background_width, self.background_height))
        self.imgRect = self.img.get_rect(bottomleft=(0,SCREEN_HEIGHT))
        #Textos Juego, switch full reduced, quit
        self.gameName1 = startingScreenFontBig.render("Eco",True,black)
        self.gameName1Rect = self.gameName1.get_rect()
        self.gameName1Rect.top = self.background_height/2 
        self.gameName1Rect.left = self.background_width * 12/60
        self.gameName2 = startingScreenFontBig.render("sys",True,black)
        self.gameName2Rect = self.gameName2.get_rect()
        self.gameName2Rect.top = self.background_height/2 
        self.gameName2Rect.left = self.background_width * 4/6
        self.quitText = startingScreenSmallFont.render("\"q\" to quit",True,black)
        self.quitTextRect = self.quitText.get_rect()
        self.quitTextRect.top = self.background_height -4* startingScreenFontSmallSize
        self.quitTextRect.left = self.background_width -10 * startingScreenFontSmallSize
        self.resizeText = startingScreenSmallFont.render("\"F11\" to resize screen",True,black)
        self.resizeTextRect = self.resizeText.get_rect()
        self.resizeTextRect.top = self.background_height -3 * startingScreenFontSmallSize
        self.resizeTextRect.left = self.background_width -10 * startingScreenFontSmallSize
        #Boton
        self.button = pygame.image.load("sprites/button.png").convert_alpha()
        self.button = pygame.transform.scale(self.button, (130,130))
        self.buttonRect = self.button.get_rect()
        self.buttonRect.top = self.background_height * 42/50
        self.buttonRect.left = self.background_width/2 - 130/2
        #Lista de visibles
        self.visible = [(self.img,self.imgRect),(self.gameName1,self.gameName1Rect),(self.gameName2,self.gameName2Rect),(self.quitText,self.quitTextRect),(self.resizeText,self.resizeTextRect),(self.button,self.buttonRect)]


    def updateScales(self, screenSize):
        (self.background_width,self.background_height) = screenSize
        self.img = pygame.transform.scale(self.img, (self.background_width, self.background_height))
        self.imgRect = self.img.get_rect(bottomleft=(0,self.background_height))

        self.gameName1Rect.top = self.background_height/2 
        self.gameName1Rect.left = self.background_width * 12/60
        self.gameName2Rect.top = self.background_height/2 
        self.gameName2Rect.left = self.background_width * 4/6

        self.quitTextRect.top = self.background_height -3* startingScreenFontSmallSize
        self.quitTextRect.left = self.background_width -10 * startingScreenFontSmallSize
        self.resizeTextRect.top = self.background_height -2 * startingScreenFontSmallSize
        self.resizeTextRect.left = self.background_width -10 * startingScreenFontSmallSize

        self.buttonRect.top = self.background_height * 42/50
        self.buttonRect.left = self.background_width/2 - 100/2
        
        self.visible = [(self.img,self.imgRect),(self.gameName1,self.gameName1Rect),(self.gameName2,self.gameName2Rect),(self.quitText,self.quitTextRect),(self.resizeText,self.resizeTextRect),(self.button,self.buttonRect)]
        
    def update(self, events, mousePos):
        for event in events:
            if mousePos[0] > self.buttonRect.left and mousePos[0] < self.buttonRect.right and mousePos[1] > self.buttonRect.top and mousePos[1] < self.buttonRect.bottom:
                self.button = pygame.transform.scale(self.button, (150,150))
                self.buttonRect = self.button.get_rect()
                self.buttonRect.top = self.background_height * 42/50 - 15
                self.buttonRect.left = self.background_width/2 - 150/2
                if event.type == pygame.MOUSEBUTTONUP:
                    self.changeStage = True
            else:
                self.button = pygame.transform.scale(self.button, (100,100))
                self.buttonRect = self.button.get_rect()
                self.buttonRect.top = self.background_height * 42/50
                self.buttonRect.left = self.background_width/2 - 100/2

        self.visible = [(self.img,self.imgRect),(self.gameName1,self.gameName1Rect),(self.gameName2,self.gameName2Rect),(self.quitText,self.quitTextRect),(self.resizeText,self.resizeTextRect),(self.button,self.buttonRect)]

        return (self.changeStage)

    def render(self, screen):
        for x in self.visible:
            screen.blit(x[0], x[1])

