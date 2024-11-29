from constants import *
from pathFinder import *
import random

import pyautogui as pt

def adjacent(zone, pos, objRace):
    #abajo
    if pos[1] > 0: #check we are not in the top corner
        if zone[pos[0]][pos[1]-1] == objRace:
            return True
    #izq
    if pos[0] > 0: #check we are not in the left corner
        if zone[pos[0]-1][pos[1]] == objRace:
            return True
    #derecha
    if pos[0] < WIDTH - 1:
        if zone[pos[0]+1][pos[1]] == objRace:
            return True
    #arriba
    if pos[1] < HEIGHT - 1:
        if zone[pos[0]][pos[1]+1] == objRace:
            return True
    return False

def lookFor(zone, pos, objRace, sensoryRadius):
    objetivos = []
    distancias = []
    maxDis = 1 + 2*sensoryRadius
    for x in range(int((maxDis-1)/-2),int((maxDis-1)/2)):
        for y in range(int((maxDis-1)/-2),int((maxDis-1)/2)):
            if pos[0] + x >= 0 and pos[1] + y >= 0 and pos[0] + x <= WIDTH and pos[1] + y <= HEIGHT:
                if zone[pos[0]+x][pos[1]+y] == objRace:
                    objetivos.append((pos[0]+x,pos[1]+y))
    
    print("objetivos => ",objetivos)

    if not objetivos: return False #NO HAY ENEMIGOS
    
    for objetivo in objetivos:
        distancias.append(abs(pos[0]-objetivo[0]) + abs(pos[1]-objetivo[1]))

    print("distancias =>",distancias)

    value = min(distancias)
    index = distancias.index(value)

    return objetivos[index]
   

def randomMove(zone,pos):
    posiblesMovs = []

    if pos[1] > 0:
        if not zone[pos[0]][pos[1]-1] == waterRace and not zone[pos[0]][pos[1]-1] == plantRace and not zone[pos[0]][pos[1]-1] == rockRace:
            posiblesMovs.append((0,-1))
    if pos[0] > 0:
        if not zone[pos[0]-1][pos[1]] == waterRace and not zone[pos[0]-1][pos[1]] == plantRace and not zone[pos[0]-1][pos[1]] == rockRace:
            posiblesMovs.append((-1,0))
    if pos[0] < WIDTH - 1:
        if not zone[pos[0]+1][pos[1]] == waterRace and not zone[pos[0]+1][pos[1]] == plantRace and not zone[pos[0]+1][pos[1]] == rockRace:
            posiblesMovs.append((1,0))
    if pos[1] < HEIGHT - 1:
        if not zone[pos[0]][pos[1]+1] == waterRace and not zone[pos[0]][pos[1]+1] == plantRace and not zone[pos[0]][pos[1]+1] == rockRace:
            posiblesMovs.append((0,1))
    
    if posiblesMovs: #Hay algo
        return posiblesMovs[random.randint(0,len(posiblesMovs)-1)]
    else: #No hay nada?
        return (0,0)


class Rabbit:
    def __init__(self, gens):
        #gens->pos,gender,age,sensoryRadius,reproductiveUrge,gestation/desiderability(genderChar)
        self.gens = gens
        self.pos = gens[0]
        self.gender = gens[1]
        self.age = gens[2]
        self.sensoryRadius = gens[3]
        self.reproductiveUrge = gens[4]
        self.genderChar = gens[5]
        #Changing Props
        self.alive = True
        self.hunger= float(0)
        self.thrist = float(0)
        self.newPos = (0,0)
        #Color
        if self.gender: self.color = rabbitMasOffRace
        else: self.color = rabbitFemOffRace
        #Reproduccion
        self.copulationAsk = False
        
        

    def play(self, zona, copulationAsks):
        #zone >_> alive,lastPos,newPos,


        #Aumentar valores
        self.hunger += HUNGERGROW
        self.thrist += THRISTGROW
    
    
        #Acciones
        if self.reproductiveUrge >= self.hunger and self.reproductiveUrge >= self.thrist:
            print("Reproducción ¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
            if self.gender: #male------------------------------------------------------------------------------------
                self.color = rabbitMasOnRace

                if not adjacent(zona,self.pos,rabbitFemOnRace):#Acercarse a fem
                    print("ACERCARSE")
                    goal = lookFor(zona,self.pos,rabbitFemOnRace,self.sensoryRadius)
                    if goal:#Rabbit femenina en celo encontrada
                        print("CON PATH celo")
                        mov = pathFinder(zona,self.pos,goal)
                        print("MOV",mov)
                        if not mov:
                            mov = randomMove(zona,self.pos)
                        self.newPos = (mov[0],mov[1])
                    else:#Rabbit femenina en celo NO encontrada, pero femenina normal si
                        goal = lookFor(zona,self.pos,rabbitFemOffRace,self.sensoryRadius)

                        if goal:#Rabbit femenina encontrada
                            print("CON PATH no celo")
                            mov = pathFinder(zona,self.pos,goal)
                            print("MOV",mov)
                            if not mov:
                                mov = randomMove(zona,self.pos)
                            self.newPos = (mov[0],mov[1])
                        else:
                            print("RAND")
                            mov = randomMove(zona,self.pos)
                            print("MOV",mov)
                            self.newPos = (self.pos[0]+mov[0],self.pos[1]+mov[1])

                if adjacent(zona,self.pos,rabbitFemOnRace):#Enviar solicitud
                    self.copulationAsk = (self.pos,self.genderChar,self.gens)

            else: #female-----------------------------------------------------------------------------------------------
                self.color = rabbitFemOnRace


            print("CON RAND")
            mov = randomMove(zona,self.pos)
            print("MOV",mov)
            self.newPos = (self.pos[0]+mov[0],self.pos[1]+mov[1])


        elif self.hunger >= self.thrist and self.hunger >= self.reproductiveUrge:
            print("\nHAMBRE")
            if self.gender: #male
                self.color = rabbitMasOffRace
            else: #female
                self.color = rabbitFemOffRace
            #Accion de hunger(comer o acercarse a comida)
            if adjacent(zona,self.pos,plantRace):#Comer
                print("ADYACENTE")
                self.hunger = float(0)
                self.newPos = self.pos
            else:#Acercarse a comer
                print("ACERCARSE")
                goal = lookFor(zona,self.pos,plantRace,self.sensoryRadius)
                print(self.pos,goal)
                if goal:#Hay un goal
                    print("CON PATH")
                    mov = pathFinder(zona,self.pos,goal)
                    print("MOV",mov)
                    if not mov:
                        mov = randomMove(zona,self.pos)
                    self.newPos = (mov[0],mov[1])
                else:#No hay un goal
                    print("CON RAND")
                    mov = randomMove(zona,self.pos)
                    print("MOV",mov)
                    self.newPos = (self.pos[0]+mov[0],self.pos[1]+mov[1])

       
                
        elif self.thrist >= self.hunger and self.thrist >= self.reproductiveUrge:
            print("\nSEDIENTO")
            if self.gender: #male
                self.color = rabbitMasOffRace
            else: #female
                self.color = rabbitFemOffRace
            #Accion de thrist(beber o acercarse a beber)
            if adjacent(zona,self.pos,waterRace):#Beber
                print("ADYACENTE")
                self.thrist = float(0)
                self.newPos = self.pos
            else:#Acercarse a beber
                goal = lookFor(zona,self.pos,waterRace,self.sensoryRadius)
                print("ACERCARSE")
                if goal:#Hay un goal
                    print("CON PATH")
                    mov = pathFinder(zona,self.pos,goal)
                    print("MOV",mov)
                    if not mov:
                        mov = randomMove(zona,self.pos)
                    self.newPos = (mov[0],mov[1])
                else:#No hay un goal
                    print("CON RAND")
                    mov = randomMove(zona,self.pos)
                    print("MOV",mov)
                    self.newPos = (self.pos[0]+mov[0],self.pos[1]+mov[1])




        print("\nURGES => ",self.hunger,self.thrist)

        #Chequeos Vivo
        if self.hunger >= 1 or self.thrist >= 1:
            self.alive = False

        #Return
        solution = (self.alive,self.pos,self.newPos,self.color,self.copulationAsk)
        self.pos = self.newPos
        self.newPos = (0,0)
        self.copulationAsk = False
        return solution

            
            
        
        