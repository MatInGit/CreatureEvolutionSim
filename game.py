import sys, pygame,time
import math
import random
import numpy as np
size = width, height = 1800, 1000
black = 120,55, 50
grey = 122,122,122

pygame.init()
dt = 10
class Food():
    def __init__(self,id):
        pygame.time.delay(20)
        #random.seed(time.time())
        self.x= random.randint(1, width)
        self.y= random.randint(1, height)
        self.size= random.randint(10,200)
        self.id = id
        self.state = 0
        self.eaten = 0
        self.eaten_time = time.time()
    def draw_food(self,j):
        if self.eaten != 0 and (-self.eaten_time + j >= 7500):
            self.eaten = 0
        pygame.draw.circle(screen, (0,255,255*self.eaten), (self.x,self.y), int(self.size/40))
    def get_coord(self):
        return (self.x,self.y)
    def eat(self,j):
        self.eaten_time = j
        self.eaten = 1
        return self.size
        #print(self.eaten_time)
        self.eaten = 1
    def get_id(self):
        return self.id
    def eee(self):
        return self.eaten

class Food_dead_body():
    def __init__(self,id):
        pygame.time.delay(20)
        #random.seed(time.time())
        self.x= random.randint(1, width)
        self.y= random.randint(1, height)
        self.size= random.randint(10,200)
        self.id = id
        self.state = 0
        self.eaten = 0
        self.eaten_time = time.time()
    def draw_food(self,j):
        if self.eaten != 0 and (-self.eaten_time + j >= 7500):
            self.eaten = 0
        pygame.draw.circle(screen, (0,255,255*self.eaten), (self.x,self.y), int(self.size/40))
    def get_coord(self):
        return (self.x,self.y)
    def eat(self,j):
        self.eaten_time = j
        self.eaten = 1
        return self.size
        #print(self.eaten_time)
        self.eaten = 1
    def get_id(self):
        return self.id
    def eee(self):
        return self.eaten



class Blob():
    def __init__(self,id_lst,dna = None, parent = None):
        if parent is None:
            pygame.time.delay(50)
            random.seed(time.time())
            self.x= random.randint(1, width)
            self.y= random.randint(1, height)
            self.size = 5
            self.speed = 3
            self.tspeed = self.speed/100
            self.radians = random.randint(1, 628)/100
            self.d_range = 40
            self.fov = 0.5
            self.energy = 600
            self.energy_max = 800
            self.id = id_lst
            self.state = 0
            self.max_offspirng = 1
            self.bday = time.time()
            self.gen = 0
            self.j = 0
            self.pattern= [.01,.01,.01,-.01,-.01,-.01,.01,-.01,.01,.01,.01,.01,-.01,-.01,-.01,.01,-.01,.01]
            self.pi = 0
            print(self.bday)
            print(self.id)
        else:
            self.reb(id_lst,dna,parent)

    def reb(self,id_lst,dna,parent):
        pygame.time.delay(50)
        random.seed(time.time())
        self.x= parent.x
        self.y= parent.y
        self.size = dna[0] +random.randint(-1,1)
        if self.size <= 0:
            self.size = 1
        self.speed = dna[1] +random.randint(-1,1)
        self.tspeed = self.speed/100
        self.radians = random.randint(1, 628)/100
        self.d_range = dna[2] +random.randint(-30,30)
        if self.d_range <= 0:
            self.d_range = 0
        self.fov = 0.5
        self.pattern= []
        for i in range(len(parent.pattern)):
            self.pattern.append(parent.pattern[i]+random.randint(-5,5)/100)
        if random.randint(0,99) >= 95:
            self.pattern.append(random.randint(-5,5)/100)
        self.pi = 0
        self.energy_max = 10*(self.size*self.size*self.size)+20
        self.energy = self.energy_max/parent.max_offspirng
        self.id = id_lst
        self.state = 0
        self.max_offspirng = dna[4] + random.randint(-1,1)
        if self.max_offspirng <= 0:
            self.max_offspirng = 1
        self.bday = time.time()
        self.gen = parent.gen + 1
        self.j = 0
        print(self.bday,self.gen)
        print(self.id)

    def birth(self,blobs,idlst):
        for i in range(len(blobs)):
            if blobs[i].id == self.id:
                self.j = i
                break
        for i in range(random.randint(1,self.max_offspirng)):
            new_blob = Blob(idlst.pop(),[self.size,self.speed,self.d_range,self.energy_max,self.max_offspirng],blobs[self.j])
            blobs.append(new_blob)
            print([self.size,self.speed,self.d_range,self.energy_max,self.max_offspirng,self.pattern])
            self.energy  -= self.energy_max/self.max_offspirng
            if self.energy <= 0:
                break


    def get_pos(self):
        self.pos = (self.x,self.y)
        return self.pos

    def print_vars(self):
        print(self.x,self.y,self.size)

    def get_id(self):
        return self.id

    def draw_blob(self):
        pygame.draw.circle(screen, black, (self.x,self.y), self.size)
        pygame.draw.line(screen,black,(self.x,self.y),(int(self.x+self.d_range*math.cos(self.radians)),int(self.y-self.d_range*math.sin(self.radians))),1)

    def move_blob(self,tspd,spd):
        self.energy -= 0.5*self.size*self.speed*self.speed*(10/dt)*spd/100
        #print(self.energy)
        self.radians += self.speed*tspd*10/dt
        self.x += int(self.speed*math.cos(self.radians)*spd*10/dt)
        self.y -= int(self.speed*math.sin(self.radians)*spd*10/dt)
        if self.x < 0:
            self.x = 0
            self.radians += math.pi
        if self.x > width:
            self.x = width
            self.radians += math.pi
        if self.y < 0:
            self.y = 0
            self.radians += math.pi
        if self.y > height:
            self.y = height
            self.radians += math.pi

        #gps[i] = (self.x,self.y,self.id)
        #print(self.x,self.y)
    def die(self,blobs):
        self.state == 2;
        #print("dead!")

    def brain(self,food,blobs,idlst,timer):
        self.speed_mod = 0.
        if self.state == 3:
            self.state = 0
            #for i in range(self.max_offspirng):
            self.birth(blobs,idlst)
        if self.state == 2:
            self.state = 2
            #print("in dead state")
        if self.state == 1:
            self.energy -= np.abs(self.d_range)/300
            self.move_blob(0,1-self.speed_mod)
            for j in range(len(food)):
                if self.targeti == food[j].get_id():
                    if food[j].eee() == 1:
                        self.state = 0
                        break
                    else:
                        break
            dx = self.target[0]-self.x
            dy = self.y - self.target[1]
            if math.sqrt(dx*dx) <= 0:
                dx = 0.00001
            dist = math.sqrt(dx*dx+dy*dy)
            #print("moving to target!",dist)
            #print(self.radians)
            if dx >=0 and dy >=0:
                self.radians = math.atan(dy/dx)
                #print(self.radians)
            if dx >=0 and dy <0:
                self.radians = math.pi*2 + math.atan(dy/dx)
                #break
            #   print(self.radians)
            if dx <0 and dy >= 0:
                self.radians = math.atan(dy/dx)+ math.pi
                #break
            if dx <0 and dy < 0:
                self.radians =math.pi + math.atan(dy/dx)
                #break
                #self.move_blob(0,0.5)
            if dist <= 5:
                self.speed_mod = 0.1
            if dist <= 3:
                for j in range(len(food)):
                    if self.targeti == food[j].get_id():
                        self.energy += food[j].eat(timer)
                        break
                self.state = 0

        if self.state == 0: # nothing detected
            self.energy -= self.d_range/300
            if timer%100 == 0:
                self.pi += 1
                if self.pi >= len(self.pattern):
                    self.pi = 0

            self.move_blob(self.pattern[self.pi],.75)
            if self.energy < self.energy_max:
                for i in range(len(food)):
                    fcoords = x,y = food[i].get_coord()
                    dx = fcoords[0] - self.x
                    if math.sqrt(dx*dx) <= 0:
                        dx = 0.00001
                    dy = self.y - fcoords[1]
                    dist = math.sqrt(dx*dx+dy*dy)

                    if dist <= self.d_range and food[i].eee() == 0:
                        self.target = fcoords
                        self.targeti = food[i].get_id()
                        #print("target Acqured!")
                        #print("dx:",dx,"dy:",dy)
                        self.state = 1
                        if dx >=0 and dy >=0:
                            self.radians = math.atan(dy/dx)
                        if dx >=0 and dy <0:
                            self.radians = math.pi*2 + math.atan(dy/dx)
                        if dx <0 and dy >= 0:
                            self.radians = math.atan(dy/dx)+ math.pi
                        if dx <0 and dy < 0:
                            self.radians =math.pi + math.atan(dy/dx)
                        break
            if self.energy <= 0:
                self.state = 2
                #print("dead!")
            if self.energy > self.energy_max:
                self.state = 3
                #print("dead!")





screen = pygame.display.set_mode(size)

pop = 100
food = 150
blobs = []
foods = []
new_blobs = []
idlst = list(range(0,10000))
fidlst = list(range(0,1000))
print(idlst)
for i in range(pop):
    blob = Blob(idlst.pop())
    blobs.append(blob)
for i in range(food):
    foodd = Food(fidlst.pop())
    foods.append(foodd)

j= 0
b = 0

while 1:
    #print(j)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(grey)
    for i in range(pop):
        blobs[i].brain(foods,blobs,idlst,j)
        blobs[i].draw_blob()

    for i in range(len(blobs)):
        if blobs[i].state != 2:
            new_blobs.append(blobs[i])
        if blobs[i].state == 2:
            idlst.append(blobs[i].id)
    blobs = new_blobs
    new_blobs = []
    pop = len(blobs)
    j +=dt
    if j%1000 == 0:
        print("population:",pop)

    for i in range(food):
        foods[i].draw_food(j)

    #blobby.print_vars()
    pygame.time.delay(dt)
    pygame.display.flip()
