import numpy as np
import heapq

from constants import *
import copy

def heuristic(a, b):

    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]#,(1,1),(1,-1),(-1,1),(-1,-1)

    close_set = set()

    came_from = {}

    gscore = {start:0}

    fscore = {start:heuristic(start, goal)}

    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
 

    while oheap:

        current = heapq.heappop(oheap)[1]

        if current == goal:

            data = []

            while current in came_from:

                data.append(current)

                current = came_from[current]

            return data

        close_set.add(current)

        for i, j in neighbors:

            neighbor = current[0] + i, current[1] + j

            tentative_g_score = gscore[current] + heuristic(current, neighbor)

            if 0 <= neighbor[0] < array.shape[0]:

                if 0 <= neighbor[1] < array.shape[1]:                

                    if array[neighbor[0]][neighbor[1]] == 1:

                        continue

                else:

                    # array bound y walls

                    continue

            else:

                # array bound x walls

                continue
 

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):

                continue
 

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:

                came_from[neighbor] = current

                gscore[neighbor] = tentative_g_score

                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                heapq.heappush(oheap, (fscore[neighbor], neighbor))
 

    return False


def pathFinder(map,start,goal):
    #Grid, start, goal
    #Change 
    mapa = copy.deepcopy(map)
    for x in range(0,len(mapa)):
        for y in range(0,len(mapa[x])):
            if not (mapa[x][y] == waterRace) and not(mapa[x][y] == plantRace) and not (mapa[x][y] == rockRace):
                mapa[x][y] = 0
            else:
                mapa[x][y] = 1 
    mapa[goal[0]][goal[1]] = 0
    mapa = np.array(mapa)
    #Route
    route = astar(mapa, start, goal)
    if not route: return False

    route = route + [start]
    route = route[::-1]

    return route[1]

