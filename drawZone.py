import pygame
from constants import *

def drawPlant (screen,pos):
    (xPos,yPos) = pos
    xPos = xPos * backSize + backSize #Dejamos márgenes
    yPos = yPos * backSize + backSize #Dejamos márgenes
    pygame.draw.rect(screen, dark_green, (1+xPos,1+yPos,backSize-1,backSize-1))

def drawGrass (screen,pos):
    (xPos,yPos) = pos
    xPos = xPos * backSize + backSize #Dejamos márgenes
    yPos = yPos * backSize + backSize #Dejamos márgenes
    pygame.draw.rect(screen, green, (1+xPos,1+yPos,backSize-1,backSize-1))

def drawWater (screen,pos):
    (xPos,yPos) = pos
    xPos = xPos * backSize + backSize #Dejamos márgenes
    yPos = yPos * backSize + backSize #Dejamos márgenes
    pygame.draw.rect(screen, blue, (1+xPos,1+yPos,backSize-1,backSize-1))

def drawRock (screen,pos):
    (xPos,yPos) = pos
    xPos = xPos * backSize + backSize #Dejamos márgenes
    yPos = yPos * backSize + backSize #Dejamos márgenes
    pygame.draw.rect(screen, light_grey, (1+xPos,1+yPos,backSize-1,backSize-1))

def drawRabbitFemOff(screen,pos):
    (xPos,yPos) = pos
    xPos = xPos * backSize + backSize #Dejamos márgenes
    yPos = yPos * backSize + backSize #Dejamos márgenes
    pygame.draw.rect(screen, white, (1+xPos,1+yPos,backSize-1,backSize-1))

def drawRabbitFemOn(screen,pos):
    (xPos,yPos) = pos
    xPos = xPos * backSize + backSize #Dejamos márgenes
    yPos = yPos * backSize + backSize #Dejamos márgenes
    pygame.draw.rect(screen, pink, (1+xPos,1+yPos,backSize-1,backSize-1))

def drawRabbitMasOff(screen,pos):
    (xPos,yPos) = pos
    xPos = xPos * backSize + backSize #Dejamos márgenes
    yPos = yPos * backSize + backSize #Dejamos márgenes
    pygame.draw.rect(screen, light_brown, (1+xPos,1+yPos,backSize-1,backSize-1))

def drawRabbitMasOn(screen,pos):
    (xPos,yPos) = pos
    xPos = xPos * backSize + backSize #Dejamos márgenes
    yPos = yPos * backSize + backSize #Dejamos márgenes
    pygame.draw.rect(screen, brown, (1+xPos,1+yPos,backSize-1,backSize-1))

def drawTile(screen,race,pos):
    #1-screen 2-race 3-pos
    if race == grassRace:
        drawGrass(screen,pos)
    elif race == waterRace:
        drawWater(screen,pos)
    elif race == plantRace:
        drawPlant(screen,pos)
    elif race == rockRace:
        drawRock(screen,pos)
    elif race == rabbitFemOffRace:
        drawRabbitFemOff(screen,pos)
    elif race == rabbitFemOnRace:
        drawRabbitFemOn(screen,pos) 
    elif race == rabbitMasOffRace:
        drawRabbitMasOff(screen,pos) 
    elif race == rabbitMasOnRace:
        drawRabbitMasOn(screen,pos) 


def drawZone(screen,zone):
    for x in range(0,len(zone)):
        for y in range(0,len(zone[x])):
            drawTile(screen,zone[x][y],(x,y))