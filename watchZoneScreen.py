from constants import *
from drawZone import *
from createZone import *
import pygame
from pygame.locals import *
from fonts import *
from rabbit import *
import numpy as np

class WatchZoneScreen:
    def __init__(self, Width = WIDTH, Height = HEIGHT):
        self.visiblePlaying = []
        self.visibleStop = []
        self.changeStage = False
        self.currentlyPlaying = True
        #Tamaño pantalla
        self.background_width = SCREEN_WIDTH
        self.background_height = SCREEN_HEIGHT
        #Zone
        self.Width = Width
        self.Height = Height
        self.zone = []
        self.buildZone()
        #Boton play
        self.buttonPlay = pygame.image.load("sprites/button.png").convert_alpha()
        self.buttonPlay = pygame.transform.scale(self.buttonPlay, (60,60))
        self.buttonRectPlay = self.buttonPlay.get_rect()
        self.buttonRectPlay.top = self.background_height/20
        self.buttonRectPlay.left = self.background_width*0.9
        #Switch full reduced, quit
        self.quitText = startingScreenSmallFont.render("\"q\" to quit",True,light_grey)
        self.quitTextRect = self.quitText.get_rect()
        self.quitTextRect.top = self.background_height -1* startingScreenFontSmallSize
        self.quitTextRect.left = self.background_width -8 * startingScreenFontSmallSize
        self.resizeText = startingScreenSmallFont.render("\"F11\" to resize screen",True,light_grey)
        self.resizeTextRect = self.resizeText.get_rect()
        self.resizeTextRect.top = self.background_height -0.1 * startingScreenFontSmallSize
        self.resizeTextRect.left = self.background_width -8 * startingScreenFontSmallSize
        #Lista de visibles
        self.visiblePlaying = [(self.quitText,self.quitTextRect),(self.resizeText,self.resizeTextRect),(self.buttonPlay,self.buttonRectPlay)]
        self.visibleStop = [(self.quitText,self.quitTextRect),(self.resizeText,self.resizeTextRect),(self.buttonPlay,self.buttonRectPlay)]
        #Rabbits lists
        self.maleRabbits = []
        self.maleRabbits.append(Rabbit([(10,10), True, 1, 5, 0.37, 0]))
        self.zone[10][10] = rabbitMasOffRace
        self.femaleRabbits = []
        self.maleRabbits.append(Rabbit([(11,11), False, 1, 5, 0.37, 0]))
        self.zone[11][11] = rabbitFemOffRace
        
        


    def setSize(self,size):
        (self.Width,self.Height) = size
        
    def buildZone(self):
        self.zone = createZone((self.Width,self.Height))

    def updateScales(self, screenSize):
        (self.background_width,self.background_height) = screenSize

        self.quitTextRect.top = self.background_height -2* startingScreenFontSmallSize
        self.quitTextRect.left = self.background_width -8 * startingScreenFontSmallSize
        self.resizeTextRect.top = self.background_height -1 * startingScreenFontSmallSize
        self.resizeTextRect.left = self.background_width -8 * startingScreenFontSmallSize

        self.buttonRectPlay.top = self.background_height/20
        self.buttonRectPlay.left = self.background_width*0.9

        self.visiblePlaying = [(self.quitText,self.quitTextRect),(self.resizeText,self.resizeTextRect),(self.buttonPlay,self.buttonRectPlay)]

        self.visibleStop = [(self.quitText,self.quitTextRect),(self.resizeText,self.resizeTextRect),(self.buttonPlay,self.buttonRectPlay)]

    def update(self, events, mousePos):
        # Update buttons
        for event in events:    
            if mousePos[0] > self.buttonRectPlay.left and mousePos[0] < self.buttonRectPlay.right and mousePos[1] > self.buttonRectPlay.top     and mousePos[1] < self.buttonRectPlay.bottom and event.type == pygame.MOUSEBUTTONUP:
                self.currentlyPlaying = not self.currentlyPlaying
        # Update zones
        if self.currentlyPlaying:
            
            eliminados = []
            casillasAbandonadas = []
            casillasAmparadas = []

            #BUCLE PLAY DE MALES-------------------------------------------------------------------------------------------------
            copulationPropositions = []

            for index in range(0,len(self.maleRabbits)):
                
                solution = self.maleRabbits[index].play(self.zone,copulationPropositions)
                print("\nSolution =>",solution)

                if solution[0]:#Alive
                    casillasAbandonadas.append( solution[1] )
                    casillasAmparadas.append( (solution[2][0], solution[2][1] , solution[3]) )

                    if solution[4]:#Copulation Ask
                        copulationPropositions.append(solution[4])

                else:#Dead
                    eliminados.append(index)
                    self.zone[solution[1][0]][solution[1][1]] = grassRace


            #CAMBIOS A ZONE DE MALES
            for x in casillasAbandonadas:
                self.zone[x[0]][x[1]] = grassRace

            for x in casillasAmparadas:
                self.zone[x[0]][x[1]] = x[2]

            casillasAbandonadas.clear()
            casillasAmparadas.clear()

            #ELIMINACION DE MALES
            arr = np.array(self.maleRabbits)
            new_arr = np.delete(arr, eliminados)
            self.maleRabbits = new_arr.tolist()
            eliminados.clear()

            #BUCLE PLAY DE FEMALES-------------------------------------------------------------------------------------------------
            for index in range(0,len(self.femaleRabbits)):
                
                solution = self.femaleRabbits[index].play(self.zone,copulationPropositions)
                print("\nSolution =>",solution)

                if solution[0]:#Alive
                    casillasAbandonadas.append( solution[1] )
                    casillasAmparadas.append( (solution[2][0], solution[2][1] , solution[3]) )
                else:#Dead
                    eliminados.append(index)
                    self.zone[solution[1][0]][solution[1][1]] = grassRace

            #CAMBIOS A ZONE DE FEMALES
            for x in casillasAbandonadas:
                self.zone[x[0]][x[1]] = grassRace

            for x in casillasAmparadas:
                self.zone[x[0]][x[1]] = x[2]

            casillasAbandonadas.clear()
            casillasAmparadas.clear()

            #ELIMINACION DE FEMALES
            arr = np.array(self.femaleRabbits)
            new_arr = np.delete(arr, eliminados)
            self.femaleRabbits = new_arr.tolist()
            eliminados.clear()

        return self.changeStage #Should be false unless change screen required
    
    def render(self, screen):
        screen.fill(dark_grey)
        
        if self.currentlyPlaying:
            pygame.time.delay(1000)
            #Circulo Play On
            self.circleOnPlay = pygame.draw.circle(screen, green,(self.background_width*0.9,self.background_height/20),backSize/2)
            #Visibles
            for x in self.visiblePlaying:
                screen.blit(x[0], x[1])
            #Zone
            drawZone(screen,self.zone)
        else:
            #Circulo Play Off
            self.circleOnPlay = pygame.draw.circle(screen, red,(self.background_width*0.9,self.background_height/20),backSize/2)
            #Visibles
            for x in self.visibleStop:
                screen.blit(x[0], x[1])