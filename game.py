import pygame
from drawZone import *
from createZone import *
from startingScreen import StartingScreen
from watchZoneScreen import WatchZoneScreen
from constants import *
from pygame.locals import *


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        self.stageStartingScreen = True
        self.stageWatchZone = False
        self.startingScreen = StartingScreen()
        self.watchZone = WatchZoneScreen()
        self.stages = [self.startingScreen,self.watchZone]

        self.clock = pygame.time.Clock()


        pygame.init()
    
        pygame.display.set_caption("Ecosys")


    def update(self):

        events = pygame.event.get()
        #Eventos comunes
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                # Exit
                if event.key == K_q:
                    self.running = False
                # Fullscreen
                if event.key == K_F11:
                    if self.fullscreen: 
                        pygame.display.set_mode((1800,1100), pygame.RESIZABLE)
                        self.fullscreen = False
                        for x in range(0,len(self.stages)):
                            self.stages[x].updateScales(pygame.display.get_window_size())
                        
                    else:
                        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        self.fullscreen = True
                        for x in range(0,len(self.stages)):
                            self.stages[x].updateScales(pygame.display.get_window_size())
        #Eventos De Stages
        if self.stageStartingScreen:
           if self.startingScreen.update(events,pygame.mouse.get_pos()):
                self.stageStartingScreen = False
                self.stageWatchZone = True

        elif self.stageWatchZone:
            print("\nREPETICION!+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")         
            if self.watchZone.update(events,pygame.mouse.get_pos()):
                self.stageWatchZone = False   

    def render(self):

        self.screen.fill(black)

        if self.stageStartingScreen:
            self.startingScreen.render(self.screen)

        elif self.stageWatchZone:         
            self.watchZone.render(self.screen)

        pygame.display.flip()

    def loop(self):
        while self.running:
            self.update()
            self.render()
            self.clock.tick()
            
        pygame.quit()


Game().loop()