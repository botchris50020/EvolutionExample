"""Main File for the Evolution Example Code"""
from tkinter import Tk,Canvas
import random
import copy
import time

class Dot():
    """ Dot class
    Displays the Dots that learn a path through evolution
    """
    def __init__(self,canvas_object,steps,goal_coords,startcoords,instruction_list,
                 color="black",rate=10,best_dot=False):
        self.xspeed = 0
        self.yspeed = 0
        self.frame = 0
        self.score = [0,0,[]]
        self.alive = True
        self.canvas_object = canvas_object
        self.canvas_id = canvas.create_oval(4, 4, 10, 10, fill=color)
        self.canvas_object.move(self.canvas_id,startcoords[0],startcoords[1])
        self.goal_coords = goal_coords
        self.directions = []
        if instruction_list == []:
            for _ in range(steps):
                self.directions.append([random.randint(-1,1),random.randint(-1,1)])
        elif best_dot:
            self.directions = instruction_list
        else:
            self.directions = copy.deepcopy(instruction_list)
            for _ in range(rate):
                self.directions[random.randint(0,steps-1)] = \
                                [random.randint(-1,1),random.randint(-1,1)]


    def deadcheck(self,obstacle_list):
        """ deadcheck function
        Checks if the dot is dead and if it is dead, how close to the goal it died.
        """
        pos = self.canvas_object.coords(self.canvas_id)
        if pos[0] <= 0:
            self.alive = False
        elif pos[2] >= self.canvas_object.winfo_width():
            self.alive = False
        elif pos[1] <= 0:
            self.alive = False
        elif pos[3] >= self.canvas_object.winfo_height():
            self.alive = False
        else:
            overlapping = self.canvas_object.find_overlapping(pos[0],pos[1],pos[2],pos[3])
            for item in obstacle_list:
                if item in overlapping:
                    self.alive = False
        if not self.alive:
            middle = [pos[0]+abs(pos[0]-pos[2]),pos[1]+abs(pos[1]-pos[3])]
            distance = (((middle[0]-self.goal_coords[0])**2)+((middle[1]-self.goal_coords[1])**2)) \
                            **(1/2.0)
            if distance < 10:
                self.score[0] = -1
            else:
                self.score[0] = distance
            self.score[1] = self.frame
            self.score[2] = copy.deepcopy(self.directions)

    def move(self):
        """ move function
        moves the dot in the direction dictated by the direction set.
        Caps the speed in any direction at 5.
        """
        if -5 <= self.xspeed + self.directions[self.frame][0] <= 5:
            self.xspeed += self.directions[self.frame][0]
        if -5 <= self.yspeed + self.directions[self.frame][1] <= 5:
            self.yspeed += self.directions[self.frame][1]
        self.canvas_object.move(self.canvas_id, self.xspeed, self.yspeed)
        self.frame += 1


def obstacle(canvas_object,coords,xlength,ylength,color="blue"):
    """ obstacle function
    Creates a rectangular obstacle and returns the id of the obstacle on the canvas.
    """
    return canvas_object.create_rectangle(coords[0]-xlength,coords[1]-ylength,
                                          coords[0]+xlength,coords[1]+ylength,
                                          fill = color)


FRAMES = 500
DOTNUM = 200
GENERATIONS = 1000
START = [200,20]
GOAL = [200,320]
DELAY = 120
instructions = []
for generation in range(GENERATIONS):
    genstart = time.time()
    tk = Tk()
    tk.title("Evolution")
    canvas = Canvas(tk, width=400, height = 400, bd=0, bg='white')
    canvas.pack()
    tk.update()
    dotslist = []
    for _ in range(DOTNUM):
        dotslist.append(Dot(canvas,FRAMES,GOAL,START,instructions))
    dotslist.append(Dot(canvas,FRAMES,GOAL,START,instructions,best_dot=True,color="green"))
    obstacles = []

    obstacles.append(obstacle(canvas,[200,130],100,10))
    obstacles.append(obstacle(canvas,[280,300],10,100))
    obstacles.append(obstacle(canvas,[120,300],10,100))
    obstacles.append(obstacle(canvas,[200,200],10,60))
    obstacles.append(obstacle(canvas,[200,350],200,10))
    obstacles.append(obstacle(canvas,GOAL,10,10,color="red"))
    simstart = time.time()
    for _ in range(FRAMES):
        start = time.time()
        for k in dotslist:
            if k.alive:
                k.move()
                k.deadcheck(obstacles)

        end = time.time()
        difference = end - start
        if difference < 1/DELAY:
            time.sleep((1/DELAY)-difference)
        tk.update()
    simend = time.time()
    best = []
    for k in dotslist:
        best.append(k.score)
    best = sorted(best,key=lambda a:a[0])
    instructions = best[0][2]
    close = best[0][0]
    if close == -1:
        better = []
        for instruction in best:
            if instruction[0]-2 <= close:
                better.append(instruction)
        instructions = sorted(better,key=lambda a:a[1])[0][2]
    tk.destroy()
    print("Generation:",generation)
    print("Time taken in s:",time.time()-genstart)
    print("Simulation time in s:",simend-simstart)
    if close == -1:   
        print("Distance to goal:",sorted(better,key=lambda a:a[1])[0][0])
        print("Speed to get there:",sorted(better,key=lambda a:a[1])[0][1])
    else:
        print("Distance to goal:",sorted(best,key=lambda a:a[0])[0][0])
        print("Speed to get there:",sorted(best,key=lambda a:a[0])[0][1])
    print("=======================================")
