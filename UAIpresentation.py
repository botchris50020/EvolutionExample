from tkinter import *
import random
import time
import copy

class dot():
    def __init__(self,canvas,steps,goal,color="black",startcoords=[0,0],instructions=[],rate=10,best=False):
        self.canvas = canvas
        self.xspeed = 0
        self.yspeed = 0
        self.frame = 0
        self.score = [0,0,[]]
        self.alive = True
        self.id = canvas.create_oval(4, 4, 10, 10, fill=color)
        self.canvas.move(self.id,startcoords[0],startcoords[1])
        self.goal = goal
        if instructions == []:
            self.directions = []
            for i in range(steps):
                self.directions.append([random.randint(-1,1),random.randint(-1,1)])
        elif best:
            self.directions = instructions
        else:
            self.directions = copy.deepcopy(instructions)
            for i in range(rate):
                self.directions[random.randint(0,steps-1)] = [random.randint(-1,1),random.randint(-1,1)]


    def deadcheck(self,obstacles):
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.alive = False
        elif pos[2] >= canvas.winfo_width():
            self.alive = False
        elif pos[1] <= 0:
            self.alive = False
        elif pos[3] >= canvas.winfo_height():
            self.alive = False
        else:
            overlapping = self.canvas.find_overlapping(pos[0],pos[1],pos[2],pos[3])
            for thing in obstacles:
                if thing.id in overlapping:
                    self.alive = False
        if not self.alive:
            self.score[0] = (((pos[0]-self.goal[0])**2)+((pos[1]-self.goal[1])**2))**(1/2.0)
            self.score[1] = self.frame
            self.score[2] = copy.deepcopy(self.directions)

    def move(self):
        if -5 <= self.xspeed + self.directions[self.frame][0] <= 5:
            self.xspeed += self.directions[self.frame][0]
        if -5 <= self.yspeed + self.directions[self.frame][1] <= 5:
            self.yspeed += self.directions[self.frame][1]
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        self.frame += 1
    

class obstacle():
    def __init__(self,canvas,coords,xlength,ylength,color="blue"):
        self.id = canvas.create_rectangle(coords[0]-xlength,coords[1]-ylength,coords[0]+xlength,coords[1]+ylength, fill = color)

instructions = []
for i in range(1000):
    print(i)
    tk = Tk()
    tk.title("ballsim")
    canvas = Canvas(tk, width=400, height = 400, bd=0, bg='white')
    canvas.pack()
    tk.update()
    frames = 500
    dotnum = 300
    goal = [20,20]
    dotslist = []
    
    for l in range(dotnum-1):
        dotslist.append(dot(canvas,frames,goal,startcoords=[200,200],instructions=instructions))
    dotslist.append(dot(canvas,frames,goal,startcoords=[200,200],instructions=instructions,best=True))
    
    obstacles = []
    obstacles.append(obstacle(canvas,[150,120],100,20))
    obstacles.append(obstacle(canvas,[100,350],200,20))


    obstacles.append(obstacle(canvas,goal,10,10,color="red"))
    for l in range(frames):
        for k in dotslist:
            if k.alive:
                k.move()
                k.deadcheck(obstacles)
        tk.update()
    best = []
    for k in dotslist:
        best.append(k.score)
    
    best = sorted(best,key=lambda a:a[0])
    close = best[0][0]
    better = []
    for instruction in best:
        if instruction[0]-2 <= close:
            better.append(instruction)
    print(sorted(better,key=lambda a:a[1])[-1][0:2])
    instructions = sorted(better,key=lambda a:a[1])[-1][2]
    tk.destroy()
    #time.sleep(0.5)
