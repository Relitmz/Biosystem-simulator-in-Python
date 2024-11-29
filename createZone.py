import random
from constants import *

def createProb(size,defaultValue):
    (Width,Height) = size
    prob = []
    for x in range(0,Width):
        prob.append([])
        for y in range(0,Height):
            prob[x].append(defaultValue)

    return prob

def addProbToAdjacent(pos,list,value):
    (x,y) = pos
    if y > 0 : list[x][y-1] = value
    if y < len(list[x]) - 1 : list[x][y+1] = value
    if x > 0 : list[x-1][y] = value
    if x < len(list) -1 : list[x+1][y] = value

    return list

def addProbToCorners(pos,list,value):
    (x,y) = pos
    if y > 0 and x > 0 : list[x-1][y-1] = value
    if y > 0 and x < len(list) -1 : list[x+1][y-1] = value
    if y < len(list[x]) - 1 and x > 0 : list[x-1][y+1] = value
    if y < len(list[x]) - 1 and x < len(list) -1 : list[x+1][y+1] = value

    return list

def addProbToSecondLine(pos,list,value):
    (x,y) = pos
    if y-2 >= 0 and x-2 >=0: list[x-2][y-2] = value
    if y-2 >= 0 and x-1 >=0: list[x-1][y-2] = value
    if y-2 >= 0 : list[x][y-2] = value
    if y-2 >= 0 and x+1 <= len(list)-1: list[x+1][y-2] = value
    if y-2 >= 0 and x+2 <= len(list)-1: list[x+2][y-2] = value

    if y-1 >= 0 and x-2 >=0: list[x-2][y-1] = value
    if x-2 >=0: list[x-2][y] = value
    if y+1 <= len(list[x])-1 and x-2 >=0: list[x-2][y+1] = value

    if y-1 >= 0 and x+2 <= len(list)-1: list[x+2][y-1] = value
    if x+2 <= len(list)-1: list[x+2][y] = value
    if y+1 <= len(list[x])-1 and x+2 <= len(list)-1: list[x+2][y+1] = value

    if y+2 <= len(list[x])-1 and x-2 >=0: list[x-2][y+2] = value
    if y+2 <= len(list[x])-1 and x-1 >=0: list[x-1][y+2] = value
    if y+2 <= len(list[x])-1 : list[x][y+2] = value
    if y+2 <= len(list[x])-1 and x+1 <= len(list)-1: list[x+1][y+2] = value
    if y+2 <= len(list[x])-1 and x+2 <= len(list)-1: list[x+2][y+2] = value

    return list
 
def searchWater(probWater,pos,dist):
    (x,y) = pos
    suma = 0
    
    for y1 in range(0,dist):
        for x1 in range(0,dist - y1):
            if x-x1 >= 0 or y-y1 >= 0 : suma += probWater[x-x1][y-y1]
            if x-x1 >= 0 or y+y1 <= len(probWater[x])-1 : suma += probWater[x-x1][y+y1]
            if x+x1 <= len(probWater)-1 or y-y1 >= 0 : suma += probWater[x+x1][y-y1]
            if x+x1 <= len(probWater)-1 or y+y1 <= len(probWater[x])-1 : suma += probWater[x+x1][y+y1]

    if suma > 0 : return False
    return True

        
def createZone (size):
    Width,Height = size

    #Creacion de zona llano, nos sirve createProb
    zone = createProb(size,grassRace)

    #Creacion prob ocenano
    probCreateOcean = createProb(size,probOcean)

    #Creamos probWater
    probWater = createProb(size,0)

    #Creamos océanos y asignamos prob de mares/lagunas
    for x in range(0,Width):
        for y in range(0,Height):
            if random.random()<=probCreateOcean[x][y]:
                #Oceano
                probWater[x][y] = 3
                zone[x][y] = waterRace
                #Prob mares adyacentes
                probWater = addProbToAdjacent((x,y),probWater,probSea)
                #Prob lagunas esquinas
                probWater = addProbToCorners((x,y),probWater,probLake)

    #Creamos mares y lagunas
    for x in range(0,Width):
        for y in range(0,Height):
            if probWater[x][y] < 1.1 and random.random()<=probWater[x][y]: #No 
                probWater[x][y] = 2
                zone[x][y] = waterRace
    
    #Relleno de aguas x2
    for t in range(0,2):      
        for x in range(0,Width):
            for y in range(0,Height):
                suma = 0

                if x-1 >= 0: suma += int(zone[x-1][y])
                else: suma += 1
                if x+1 <= len(probWater)-1: suma += int(zone[x+1][y])
                else: suma += 1
                if y-1 >= 0: suma += int(zone[x][y-1])
                else: suma += 1
                if y+1 <= len(probWater[x])-1: suma += int(zone[x][y+1])
                else: suma += 1

                if suma >= 3 : 
                    probWater[x][y] = 2
                    zone[x][y] = waterRace
    
    #Relleno de islas

    #Creacion Prob comida
    probPlant = createProb(size,probFood)
    
    #Ponemos prob alrededor doble de agua a 0
    for x in range(0,Width):
        for y in range(0,Height):
            if zone[x][y] == waterRace:
                #1 linea
                probPlant = addProbToAdjacent((x,y),probPlant,0)
                probPlant = addProbToCorners((x,y),probPlant,0)
                #2 linea
                probPlant = addProbToSecondLine((x,y),probPlant,0)
                
    #Creamos food y asignamos probs alrededor doble de comida a 0
    for x in range(0,Width):
        for y in range(0,Height):
            if zone[x][y] == grassRace and random.random()<=probPlant[x][y]: # Es grass y prob
                zone[x][y] = plantRace
                #Ponemos prob alrededor doble de planta a 0
                #1 linea
                probPlant = addProbToAdjacent((x,y),probPlant,0)
                probPlant = addProbToCorners((x,y),probPlant,0)
                #2 linea
                probPlant = addProbToSecondLine((x,y),probPlant,0)


    #Creación prob montaña
    probRock = createProb(size,probObstacle)

    #Creamos montaña
    for x in range(0,Width):
        for y in range(0,Height):
            if zone[x][y] == grassRace and random.random()<=probRock[x][y]: # Es grass y prob
                zone[x][y] = rockRace


    #Colocamos a los rabbits (en el futuro mejorar)
    
    return (zone)
