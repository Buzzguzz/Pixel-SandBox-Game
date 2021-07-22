import pygame
import random
################################# screen initialization 
(width, height) = 800 ,800 # w and h of screen in pixels
screen = pygame.display.set_mode((width, height)) # the screen variable has been assigned with width and height of the variables 
pygame.display.set_caption("voronoy") # name of the window
screen_background = (0 , 0, 0) # the background of the screen in RGB form
screen.fill(screen_background) # changes the screen background colour to the screen_background variable
pygame.display.flip() # used to display screen
#################################
clock = pygame.time.Clock()
#800 / 80 = num of pixels
#800 / num of pixels = 80 pixel size
pixel_size = 5

stone_colour = [(82, 82, 82), (87, 87, 87), (92, 92, 92)]
sand_colour = [(255, 243, 110), (219, 207, 72), (247, 231, 45)]
water_colour = [(0, 60, 255), (0, 58, 247), (13, 69, 252)]
smoke_colour = [(46, 46, 46)]
pink = [(242, 25, 250), (233, 58, 240), (202, 19, 209)]

##############################
class Stone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = random.choice(stone_colour)
        self.breakable = True
    
    def draw(self):
        self.x = round(self.x/pixel_size)*pixel_size
        self.y = round(self.y/pixel_size)*pixel_size
        pygame.draw.rect(screen,self.colour,(self.x, self.y, pixel_size, pixel_size))
##############################
class Sand():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = random.choice(sand_colour)
        self.breakable = True

    def update(self):
        if self.y == height - pixel_size: return # if bottom of screen stay there lol
        if screen.get_at((self.x, self.y + pixel_size)) == (0,0,0):
            move_down(self)
        elif screen.get_at((self.x - pixel_size, self.y + pixel_size)) == (0,0,0):
            move_down_left(self)
        elif screen.get_at((self.x + pixel_size, self.y + pixel_size)) == (0,0,0):
            move_down_right(self)

    def draw(self):
        self.update()
        self.x = round(self.x/pixel_size)*pixel_size
        self.y = round(self.y/pixel_size)*pixel_size
        pygame.draw.rect(screen,self.colour,(self.x, self.y, pixel_size, pixel_size))
##############################
class Water():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = random.choice(water_colour)
        self.breakable = True

    def update(self):
        left = False
        right = False
        if screen.get_at((self.x, self.y + pixel_size)) == (0,0,0):
            move_down(self)
        elif screen.get_at((self.x - pixel_size, self.y + pixel_size)) == (0,0,0):
            move_down_left(self)
        elif screen.get_at((self.x + pixel_size, self.y + pixel_size)) == (0,0,0):
            move_down_right(self)
        else:
            if screen.get_at((self.x - pixel_size, self.y)) == (0,0,0):
                left = True
            if screen.get_at((self.x + pixel_size, self.y)) == (0,0,0):
                right = True
            if left == True and right == True:
                res = random.choice([1, -1])
                self.x += pixel_size * res
            elif left == True and right == False:
                move_left(self)
            elif right == True and left == False:
                move_right(self)

    def draw(self):
        self.update()
        self.x = round(self.x/pixel_size)*pixel_size
        self.y = round(self.y/pixel_size)*pixel_size
        pygame.draw.rect(screen,self.colour,(self.x, self.y, pixel_size, pixel_size))
##############################
class Smoke():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = random.choice(smoke_colour)
        self.breakable = True

    def update(self):
        left = False
        right = False
        if screen.get_at((self.x, self.y - pixel_size)) == (0,0,0):
            move_up(self)
        elif screen.get_at((self.x - pixel_size, self.y - pixel_size)) == (0,0,0):
            move_up_left(self)
        elif screen.get_at((self.x + pixel_size, self.y - pixel_size)) == (0,0,0):
            move_up_right(self)
        move_across = random.choice([True,False])
        if move_across:
            if screen.get_at((self.x - pixel_size, self.y)) == (0,0,0):
                left = True
            if screen.get_at((self.x + pixel_size, self.y)) == (0,0,0):
                right = True
            if left == True and right == True:
                res = random.choice([1, -1])
                self.x += pixel_size * res
            elif left == True and right == False:
                move_left(self)
            elif right == True and left == False:
                move_right(self)

    def draw(self):
        self.update()
        self.x = round(self.x/pixel_size)*pixel_size
        self.y = round(self.y/pixel_size)*pixel_size
        pygame.draw.rect(screen,self.colour,(self.x, self.y, pixel_size, pixel_size))

def move_down(obj):
    global pixel_size
    obj.y += pixel_size
def move_down_left(obj):
    global pixel_size
    obj.y += pixel_size
    obj.x -= pixel_size
def move_down_right(obj):
    global pixel_size
    obj.y += pixel_size
    obj.x += pixel_size
def move_up(obj):
    global pixel_size
    obj.y -= pixel_size
def move_up_left(obj):
    global pixel_size
    obj.y -= pixel_size
    obj.x -= pixel_size
def move_up_right(obj):
    global pixel_size
    obj.y -= pixel_size
    obj.x += pixel_size
def move_left(obj):
    global pixel_size
    obj.x -= pixel_size
def move_right(obj):
    global pixel_size
    obj.x += pixel_size

def create_barrier():
    for x in range(1, width):
        p = Stone(x, 1)
        p.breakable = False
        x += pixel_size
        Particles.append(p)
    for x in range(1, width):
        p = Stone(x,height - pixel_size)
        p.breakable = False
        Particles.append(p)
        x += pixel_size
    for x in range(1, width):
        p = Stone(1, x)
        p.breakable = False
        x += pixel_size
        Particles.append(p)
    for x in range(1, width):
        p = Stone(height - pixel_size,x)
        p.breakable = False
        Particles.append(p)
        x += pixel_size

def create_particle(x, y, size, selected):
    places = [(x, y), (x + pixel_size, y ), (x , y + pixel_size), (x + pixel_size , y + pixel_size )]
    if selected == "stone":
        for place in places:
            p = Stone(place[0], place[1])
            Particles.append(p)
    elif selected == "sand":
        for place in places:
            p = Sand(place[0], place[1])
            Particles.append(p)
    elif selected == "water":
        for place in places:    
            p = Water(place[0], place[1])
            Particles.append(p)
    elif selected == "smoke":
        for place in places:    
            p = Smoke(place[0], place[1])
            Particles.append(p)
    else: return

def delete_particle(x,y):
    neighbour = [(x, y), (x + pixel_size, y), (x, y + pixel_size), (x + pixel_size, y + pixel_size)]
    i = 0
    for particle in Particles:
        if (particle.x, particle.y) in neighbour and particle.breakable == True:
            i += 1
            Particles.remove(particle)
    print(i)

(mouseX, mouseY) = pygame.mouse.get_pos()
pygame.mouse.set_visible(False)
Particles = []
running = True
create_barrier()
selected = 'stone'
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if the X is pressed it closes the program
            running = False
        if pygame.mouse.get_pressed()[0]:
            create_particle(mouseX, mouseY, 1, selected)
        if pygame.mouse.get_pressed()[2]:
            delete_particle(mouseX, mouseY)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected = 'stone'
            elif event.key == pygame.K_2:
                selected = 'sand'
            elif event.key == pygame.K_3:
                selected = 'water'
            elif event.key == pygame.K_4:
                selected = 'smoke'
    for particle in Particles:
        particle.draw()
    
    (mouseX, mouseY) = pygame.mouse.get_pos()
    mouseX = round(mouseX/pixel_size)*pixel_size
    mouseY = round(mouseY/pixel_size)*pixel_size
    pygame.draw.rect(screen,(255,255,255),(mouseX , mouseY , pixel_size * 2, pixel_size * 2), 1)
    pygame.display.flip()
    screen.fill(screen_background)