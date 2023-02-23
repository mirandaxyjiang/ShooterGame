#Name: Miranda
#Date: Jan. 22, 2020
#Class: ICS3U1-04
#Description: Runs a game where the user has to shoot ewaste containers and achieve a certain number of points each level which get faster and faster the higher you get.

#Initializing random and pygame
import random

import pygame
pygame.init()
SIZE = (WIDTH,HEIGHT) = (1000,700)
screen = pygame.display.set_mode(SIZE)

#Colours

#For background
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 212, 0)
DARKERGREEN = (0, 171, 0)
EVENDARKERGREEN = (0, 150, 0)
DARKESTGREEN = (0, 125, 4)

#For water
BLUE = (0, 0, 255)
SKYBLUE = (135,206,235)
LIGHTERWATERBLUE = (0,167,190)
LIGHTWATERBLUE = (0,151,190)
WATERBLUE = (0, 135, 190)
DARKWATERBLUE = (0,119,190)
DARKERWATERBLUE = (0,103,190)

#For character
PEACH = (255,229,180)
BROWN = (101,67,33)
PANTSBLUE = (51,51,153)
DARKRED = (204,0,0)

#Accumulators        
charactercoordinate = 0
score = 0
goalscore = 50
ewastecountforlevel = 8
characterspeed = 8
containerspeed = 7

#Counters
ewastecount = 1
level = 1
beginning = 0

#Switches for states
runningMenu = True
runningGame = False
runningInstructions = False
gameOver = False
nextLevel = False
runningHighScore = False
KEY_RIGHT = False
KEY_LEFT = False
KEY_SPACE = False
shoot = False
maxewastecontainers = False
increaseewaste = False
increasenormal = False
characterright = True
characterleft = False

#Constants
CONTAINER_LENGTH = 200
CONTAINER_WIDTH = 95
BULLET_SIZE = 32

#Randomly generates positions for clouds
cloudx = random.randint(50,300)
cloudy = random.randint(50,250)
size = random.randint(10,35)

cloudx_2 = random.randint(350,600)
cloudy_2 = random.randint(50,250)
size_2 = random.randint(10,35)

cloudx_3 = random.randint(650,900)
cloudy_3 = random.randint(50,250)
size_3 = random.randint(10,35)

#Initializing images, fonts and sounds

#Images
riflePic = pygame.image.load("rifle.png")
rifle2Pic = pygame.image.load("rifle2.png")
skyPic = pygame.image.load("sky.png")
mountainsPic = pygame.image.load("mountains.png")
eWastePic = pygame.image.load("ewaste.png")
normalPic = pygame.image.load("normal.png")
bulletPic = pygame.image.load("bullet.png")
menuPic = pygame.image.load("menucontainer.png")
spacebarPic = pygame.image.load("spacebar.png")
arrowkeysPic = pygame.image.load("arrowkeys.png")

#Fonts
fontScore = pygame.font.SysFont("Times New Roman",30)
fontLevel = pygame.font.SysFont("Times New Roman",60)
fontMenu = pygame.font.SysFont("Times New Roman",60)
fontInstructions = pygame.font.SysFont("Times New Roman",25)

#Sounds
gunSound = pygame.mixer.Sound("gunsound.wav")
collisionSound = pygame.mixer.Sound("collision.wav")
clickSound = pygame.mixer.Sound("click.wav")

#Indicators
playindicator = pygame.Rect(WIDTH/4,250,WIDTH/2,100)
instructionsindicator = pygame.Rect(WIDTH/4,400,WIDTH/2,100)
quitindicator = pygame.Rect(WIDTH/4,550,WIDTH/2,100)
backindicator = pygame.Rect(25,625,100,50)
highscoreindicator = pygame.Rect(775,625,200,50)
nextlevelindicator = pygame.Rect(775,625,200,50)
quitlevelindicator = pygame.Rect(25,625,100,50)

#Lists

#Starting positions
container_pos_ewaste = [-200, 50]
container_pos_normal = [-450, 50]

#Contains coordinates for all containers and bullets
container_list_ewaste = [container_pos_ewaste]
container_list_normal = [container_pos_normal]
bullet_list = []

#Contains the index position of the containers and bullets that collide
collided_ewaste_index = []
collided_normal_index = []
collided_bullet_index = []

#Contains high score after the game is over
highscore = []

#Functions
        
#Draws the menu with rectangles and title and prints the text on the corresponding rectangle. Checks to see if the mouse is hovering over an option and draw a lighter rectangle if it is.
def drawMenu(screen, mx, my):
    screen.blit(menuPic, pygame.Rect(0, 0, 1000, 700))
    
    #Title of game
    text = fontMenu.render("SHOOT THE E-WASTE" , 1, WHITE)
    screen.blit(text, pygame.Rect(200,100,WIDTH/2,100))    
    
    #Draws rectangles
    pygame.draw.rect(screen, BLUE, playindicator)
    pygame.draw.rect(screen, BLUE, instructionsindicator)
    pygame.draw.rect(screen, BLUE, quitindicator)
    
    #Prints text
    text = fontMenu.render("Play" , 1, WHITE)
    screen.blit(text, pygame.Rect(450,265,WIDTH/2,100))
   
    text = fontMenu.render("Instructions" , 1, WHITE)
    screen.blit(text, pygame.Rect(350,415,WIDTH/2,100))
    
    text = fontMenu.render("Quit" , 1, WHITE)
    screen.blit(text, pygame.Rect(435,565,WIDTH/2,100))
    
    #Checking if mouse is hovering
    if playindicator.collidepoint(mx,my):
        pygame.draw.rect(screen, WATERBLUE, playindicator, 0)
        text = fontMenu.render("Play" , 1, WHITE)
        screen.blit(text, pygame.Rect(450,265,WIDTH/2,100))  
        
    elif instructionsindicator.collidepoint(mx,my):
        pygame.draw.rect(screen, WATERBLUE, instructionsindicator, 0)
        text = fontMenu.render("Instructions" , 1, WHITE)
        screen.blit(text, pygame.Rect(350,415,WIDTH/2,100)) 
        
    elif quitindicator.collidepoint(mx,my):
        pygame.draw.rect(screen, WATERBLUE, quitindicator, 0)
        text = fontMenu.render("Quit" , 1, WHITE)
        screen.blit(text, pygame.Rect(435,565,WIDTH/2,100))     

#Draws the instructions page and will check if the mouse is hovering over the back button
def drawInstructions(screen, mx, my):
    screen.blit(menuPic, pygame.Rect(0, 0, 1000, 700))
    
    #Explains the objective
    text = fontInstructions.render("Objective: There are e-waste containers being shipped out illegally! Help the environment" , 1, WHITE)
    screen.blit(text, pygame.Rect(50,50,600,100))    
    text = fontInstructions.render("by shooting them down. There are normal containers and e-waste containers. Aim for the" , 1, WHITE)
    screen.blit(text, pygame.Rect(50,75,600,100))  
    text = fontInstructions.render("e-waste containers which are worth 10 points each and be careful to not hit the normal ones" , 1, WHITE)
    screen.blit(text, pygame.Rect(50,100,600,100))
    text = fontInstructions.render("which will make you lose 20. Each level, you will have a certain amount of points you need", 1, WHITE)
    screen.blit(text, pygame.Rect(50,125,600,100))
    text = fontInstructions.render("to achieve. If you don't achieve the goal, the game will end. The higher the level you are, " , 1, WHITE)
    screen.blit(text, pygame.Rect(50,150,600,100))
    text = fontInstructions.render("the faster the containers will move. Have fun!", 1, WHITE)
    screen.blit(text, pygame.Rect(50,175,600,100))    
    
    #How to play title
    text = fontMenu.render("How To Play" , 1, BLACK)
    screen.blit(text, pygame.Rect(350,225,200,100))
    
    #Graphics for which one is the normal container and which one is the ewaste container
    screen.blit(normalPic, pygame.Rect(50,300,1,1))
    text = fontInstructions.render("Normal" , 1, WHITE)
    screen.blit(text, pygame.Rect(110,330,100,100))
    
    screen.blit(eWastePic, pygame.Rect(300,300,1,1))
    text = fontInstructions.render("E-waste" , 1, WHITE)
    screen.blit(text, pygame.Rect(360,330,100,100))    
    
    #Graphics and explanation for the space bar
    screen.blit(spacebarPic, pygame.Rect(50,425,1,1))  
    
    pygame.draw.line(screen, BLACK, (274, 545), (274, 575), 3)
    text = fontInstructions.render("Hit the space bar to shoot the bullets" , 1, BLACK)
    screen.blit(text, pygame.Rect(100,580,200,100))
    
    #Graphics and explanation for the arrow keys
    screen.blit(arrowkeysPic, pygame.Rect(600,300,1,1))
    
    pygame.draw.line(screen, BLACK, (660, 540), (660, 615), 3)
    text = fontInstructions.render("Press to move left" , 1, BLACK)
    screen.blit(text, pygame.Rect(575,625,200,100))
    
    pygame.draw.line(screen, BLACK, (875, 540), (875, 615), 3)
    text = fontInstructions.render("Press to move right" , 1, BLACK)
    screen.blit(text, pygame.Rect(790,625,200,100))
    
    pygame.draw.rect(screen, BLUE, backindicator, 0)
    text = fontScore.render("Back" , 1, WHITE)
    screen.blit(text, pygame.Rect(45,635,50,50))
    
    #Checks if mouse is hovering
    if backindicator.collidepoint(mx,my):
        pygame.draw.rect(screen, WATERBLUE, backindicator, 0)
        text = fontScore.render("Back" , 1, WHITE)
        screen.blit(text, pygame.Rect(45,635,50,50))    
    
#Returns the coordinate of the mouse  
def getmouse():
    mx, my = pygame.mouse.get_pos()
    mb = pygame.mouse.get_pressed()[0]
    return (mx, my, mb) 
    
#Draws the triangles on the grass
def drawGrassTriangle(WIDTH):
    y = 0
    
    #Uses loop to draw each layer. Each time "i" is counted, it will decrease the y-coordinate of where the layer is drawn. Each time it loops back around, the colour will change to a darker one  
    for i in range(100,0,-20):
        x = 0
        
        if y == 0:
            colour = GREEN
        elif y == 1:
            colour = DARKGREEN
        elif y == 2:
            colour = DARKERGREEN
        elif y == 3:
            colour = EVENDARKERGREEN
        elif y == 4:
            colour = DARKESTGREEN
        
        #Loop that continuously draws triangles with different heights across the screen until it reaches the edge   
        while x < WIDTH:
            pygame.draw.polygon(screen, colour, ((x,700-i), (x+5,700-i-5), (x+10, 700-i)))
            x += 10
            pygame.draw.polygon(screen, colour, ((x,700-i), (x+5,700-i-10), (x+10, 700-i)))
            x += 10
            pygame.draw.polygon(screen, colour, ((x,700-i), (x+5,700-i-15), (x+10, 700-i)))
            x += 10
            pygame.draw.polygon(screen, colour, ((x,700-i), (x+5,700-i-10), (x+10, 700-i)))
            x += 10
            
        y += 1 #Changes the colour

#Draws the main background of the game
def drawBackground():
    screen.blit(skyPic, pygame.Rect(0,-150,1000,700))
    screen.blit(mountainsPic, pygame.Rect(0,150,1000,700))
    pygame.draw.rect(screen, LIGHTERWATERBLUE, pygame.Rect(0, 400, 1000, 200))
    pygame.draw.rect(screen, LIGHTWATERBLUE, pygame.Rect(0, 440, 1000, 200))
    pygame.draw.rect(screen, WATERBLUE, pygame.Rect(0, 480, 1000, 200))
    pygame.draw.rect(screen, DARKWATERBLUE, pygame.Rect(0, 520, 1000, 200))
    pygame.draw.rect(screen, DARKERWATERBLUE, pygame.Rect(0, 560, 1000, 200))
    pygame.draw.rect(screen, DARKERGREEN, pygame.Rect(0, 380, 1000, 20))
    pygame.draw.rect(screen, GREEN, pygame.Rect(0, 600, 1000, 100))
    pygame.draw.rect(screen, DARKGREEN, pygame.Rect(0, 620, 1000, 100))
    pygame.draw.rect(screen, DARKERGREEN, pygame.Rect(0, 640, 1000, 100))
    pygame.draw.rect(screen, EVENDARKERGREEN, pygame.Rect(0, 660, 1000, 100))
    pygame.draw.rect(screen, DARKESTGREEN, pygame.Rect(0, 680, 1000, 100))    
    drawGrassTriangle(WIDTH)

#Draws the character facing right 
def drawCharacterRight(xcoordinate):
    #Head
    pygame.draw.rect(screen, PEACH, pygame.Rect(xcoordinate, 500, 30, 30))
    pygame.draw.rect(screen, BROWN, pygame.Rect(xcoordinate, 500, 35, 5))
    pygame.draw.rect(screen, BROWN, pygame.Rect(xcoordinate, 500, 5, 15))
    pygame.draw.rect(screen, BROWN, pygame.Rect(xcoordinate + 15, 495, 20, 5))
    pygame.draw.rect(screen, BROWN, pygame.Rect(xcoordinate, 520, 5, 10))
    pygame.draw.rect(screen, PEACH, pygame.Rect(xcoordinate + 10, 530, 10, 10))
    
    #Body
    pygame.draw.rect(screen, RED, pygame.Rect(xcoordinate, 540, 30, 50))
    
    #Left arm
    pygame.draw.rect(screen, DARKRED, pygame.Rect(xcoordinate + 25, 540, 10, 30))
    pygame.draw.rect(screen, DARKRED, pygame.Rect(xcoordinate + 25, 560, 30, 10))
    pygame.draw.rect(screen, PEACH, pygame.Rect(xcoordinate + 55, 560, 10, 10))
    
    #Legs
    pygame.draw.polygon(screen, PANTSBLUE, ((xcoordinate, 590), (xcoordinate - 10, 640), (xcoordinate + 5, 640), (xcoordinate + 15, 590)))
    pygame.draw.polygon(screen, PANTSBLUE, ((xcoordinate + 15, 590), (xcoordinate + 25, 640), (xcoordinate + 40, 640), (xcoordinate + 30, 590)))
    pygame.draw.rect(screen, BLACK, pygame.Rect(xcoordinate - 15, 640, 20, 5))
    pygame.draw.rect(screen, BLACK, pygame.Rect(xcoordinate + 25, 640, 20, 5))    
    
    #Rifle
    screen.blit(riflePic, pygame.Rect(xcoordinate - 10, 490, 0, 0))
    
    #Right arm
    pygame.draw.rect(screen, DARKRED, pygame.Rect(xcoordinate - 5, 540, 10, 40))
    pygame.draw.rect(screen, DARKRED, pygame.Rect(xcoordinate - 5, 570, 30, 10))
    pygame.draw.rect(screen, PEACH, pygame.Rect(xcoordinate + 25, 570, 10, 10))

#Draws the character facing left    
def drawCharacterLeft(xcoordinate):
    #Head
    pygame.draw.rect(screen, PEACH, pygame.Rect(xcoordinate - 30, 500, 30, 30))
    pygame.draw.rect(screen, BROWN, pygame.Rect(xcoordinate - 35, 500, 35, 5))
    pygame.draw.rect(screen, BROWN, pygame.Rect(xcoordinate - 5, 500, 5, 15))
    pygame.draw.rect(screen, BROWN, pygame.Rect(xcoordinate - 35, 495, 20, 5))
    pygame.draw.rect(screen, BROWN, pygame.Rect(xcoordinate - 5, 520, 5, 10))
    pygame.draw.rect(screen, PEACH, pygame.Rect(xcoordinate - 20, 530, 10, 10))
    
    #Body
    pygame.draw.rect(screen, RED, pygame.Rect(xcoordinate - 30, 540, 30, 50))
    
    #Right arm
    pygame.draw.rect(screen, DARKRED, pygame.Rect(xcoordinate - 35, 540, 10, 30))
    pygame.draw.rect(screen, DARKRED, pygame.Rect(xcoordinate - 55, 560, 30, 10))
    pygame.draw.rect(screen, PEACH, pygame.Rect(xcoordinate - 65, 560, 10, 10))     
    
    #Legs
    pygame.draw.polygon(screen, PANTSBLUE, ((xcoordinate, 590), (xcoordinate + 10, 640), (xcoordinate - 5, 640), (xcoordinate - 15, 590)))
    pygame.draw.polygon(screen, PANTSBLUE, ((xcoordinate - 15, 590), (xcoordinate - 25, 640), (xcoordinate - 40, 640), (xcoordinate - 30, 590)))
    pygame.draw.rect(screen, BLACK, pygame.Rect(xcoordinate - 5, 640, 20, 5))
    pygame.draw.rect(screen, BLACK, pygame.Rect(xcoordinate - 45, 640, 20, 5))    
    
    #Rifle
    screen.blit(rifle2Pic, pygame.Rect(xcoordinate - 110, 490, 0, 0))
    
    #Left arm
    pygame.draw.rect(screen, DARKRED, pygame.Rect(xcoordinate - 5, 540, 10, 40))
    pygame.draw.rect(screen, DARKRED, pygame.Rect(xcoordinate - 25, 570, 30, 10))
    pygame.draw.rect(screen, PEACH, pygame.Rect(xcoordinate - 35, 570, 10, 10))    

#Draws clouds    
def drawClouds(x,y,size):
    pygame.draw.circle(screen, WHITE, (x, y), size)
    pygame.draw.circle(screen, WHITE, (x-size//2, y-size//2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2, y-size//2*2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2, y+size//2*2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2*3, y+size//2*2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2*3, y+size//2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2*4, y-size//2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2*6, y+size//2*2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2*5, y+size//2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2*7, y-size//2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2*6, y-size//2), size)
    pygame.draw.circle(screen, WHITE, (x-size//2*2, y-size//2), size)
    pygame.draw.circle(screen, WHITE, (x+size//2, y), size)
    pygame.draw.circle(screen, WHITE, (x+size//2, y+size//4), size)

#Draws the containers    
def add_containers(container_list_ewaste, container_list_normal):
    global container_type
    global ewastecount
    global ewastecountforlevel
    global maxewastecontainers
    
    #Checks if the container chosen is ewaste and will add a container if the previous one is at least 50 pixels away from the edge by going through a list of scenarios
    if container_type >= 8 and ewastecount < ewastecountforlevel:
        
        #Scenario when there are at least one of each container on the screen
        if len(container_list_ewaste) != 0 and len(container_list_normal) != 0:
            
            #Adds container if it meets the requirements of at least 50 pixels
            if container_list_ewaste[-1][0] > 50 and container_list_normal[-1][0] > 50:
                x_pos = -200
                y_pos = 50         
                container_list_ewaste.append([x_pos, y_pos])
                ewastecount += 1
                
        #Scenario of adding a container if nothing is on the screen
        elif len(container_list_ewaste) == 0 and len(container_list_normal) == 0:
            x_pos = -200
            y_pos = 50         
            container_list_ewaste.append([x_pos, y_pos])
            ewastecount += 1
        
        #Scenario if there are no ewaste containers on the screen
        elif len(container_list_ewaste) == 0:
            
            #Adds container if it meets the requirements of at least 50 pixels
            if container_list_normal[-1][0] > 50:
                x_pos = -200
                y_pos = 50         
                container_list_ewaste.append([x_pos, y_pos])
                ewastecount += 1
    
        #Scenario if there are no normal containers on the screen
        elif len(container_list_normal) == 0:
            
            #Adds container if it meets the requirements of at least 50 pixels
            if container_list_ewaste[-1][0] > 50:
                x_pos = -200
                y_pos = 50         
                container_list_ewaste.append([x_pos, y_pos])
                ewastecount += 1
                
        #Checks after containers are added if the max number of ewaste containers for the level was met   
        if ewastecount >= ewastecountforlevel:
            maxewastecontainers = True
    
    #Checks if the container chosen is normal and will add a container if the previous one is at least 50 pixels away by running the same scenarios from above
    elif 1 <= container_type <= 7:
        
        #Scenario when there are at least one of each container on the screen
        if len(container_list_ewaste) != 0 and len(container_list_normal) != 0:
            
            #Adds container if it meets the requirements of at least 50 pixels
            if container_list_ewaste[-1][0] > 50 and container_list_normal[-1][0] > 50:
                x_pos = -200
                y_pos = 50         
                container_list_normal.append([x_pos, y_pos])
        
        #Scenario of adding a container if nothing is on the screen
        elif len(container_list_ewaste) == 0 and len(container_list_normal) == 0:
            x_pos = -200
            y_pos = 50         
            container_list_normal.append([x_pos, y_pos])
        
        #Scenario if there are no ewaste containers on the screen    
        elif len(container_list_ewaste) == 0:
            
            #Adds container if it meets the requirements of at least 50 pixels
            if container_list_normal[-1][0] > 50:
                x_pos = -200
                y_pos = 50         
                container_list_normal.append([x_pos, y_pos])
        
        #Scenario if there are no normal containers on the screen
        elif len(container_list_normal) == 0:
            
            #Adds container if it meets the requirements of at least 50 pixels
            if container_list_ewaste[-1][0] > 50:
                x_pos = -200
                y_pos = 50         
                container_list_normal.append([x_pos, y_pos])            

#Draws ewaste containers
def draw_containers_ewaste(container_list_ewaste):
    #Loop that goes through each x and y coordinate that is in the ewaste container list and uses the coordinates to draw the container
    for container_pos_ewaste in container_list_ewaste:
        screen.blit(eWastePic, pygame.Rect(container_pos_ewaste[0], container_pos_ewaste[1], CONTAINER_LENGTH, CONTAINER_WIDTH))
        
#Draws normal containers       
def draw_containers_normal(container_list_normal):
    #Loop that goes through each x and y coordinate that is in the normal container list and uses the coordinates to draw the container
    for container_pos_normal in container_list_normal:
        screen.blit(normalPic, pygame.Rect(container_pos_normal[0], container_pos_normal[1], CONTAINER_LENGTH, CONTAINER_WIDTH))

#Updates all the container positions
def update_container_pos(container_list_ewaste, container_list_normal, containerspeed):
    global increaseewaste
    global increasenormal
    
    #Uses 2 loops, one for each container list and goes through each position and adds the container speed to the x coordinate
    for i in range(len(container_list_ewaste)):
        container_list_ewaste[i][0] += containerspeed
        
        #Checks if the y coordinate of the container is smaller than 10 or greater than 150. According to the current position of the container it will make increaseewaste True or False.
        if container_list_ewaste[i][1] <= 10:
            increaseewaste = True
            
        elif container_list_ewaste[i][1] >= 150:
            increaseewaste = False
        
        #If it's True, the y coordinate increases, if it's False, the y coordinate decreases.
        if increaseewaste == True:     
            container_list_ewaste[i][1] += 5
            
        elif increaseewaste == False:
            container_list_ewaste[i][1] -= 5
        
    for i in range(len(container_list_normal)):
        container_list_normal[i][0] += containerspeed
        
        #Checks if the y coordinate of the container is smaller than 10 or greater than 150. According to the current position of the container it will make increasenormal True or False.
        if container_list_normal[i][1] <= 10:
            increasenormal = True
            
        elif container_list_normal[i][1] >= 150:
            increasenormal = False
            
         #If it's True, the y coordinate increases, if it's False, the y coordinate decreases.
        if increasenormal == True:     
            container_list_normal[i][1] += 5
            
        elif increasenormal == False:
            container_list_normal[i][1] -= 5   

#Deletes containers from the list
def del_container(container_list_normal, container_list_ewaste):
    global collided_ewaste_index
    global collided_normal_index
    
#Uses 2 loops, one for each container index list which contains the index position of the collided containers in the container lists that hold the x and y coordinates of each container. It deletes the set of coordinates in the container lists using the index each time it runs through.
    for i in range(len(collided_normal_index)):
        del container_list_normal[collided_normal_index[i]]
        
    for i in range(len(collided_ewaste_index)):
        del container_list_ewaste[collided_ewaste_index[i]]
    
    #Resets both index lists after all the collided containers are deleted   
    collided_normal_index = []
    collided_ewaste_index = []    
    
    #Will only check to see if a normal container should be deleted if there is at least 1
    if len(container_list_normal) > 1:
        
        #If the first container is off the screen, then it will be deleted
        if container_list_normal[0][0] > WIDTH:
            del container_list_normal[0]
    
    #Will only check to see if an ewaste container should be deleted if there is at least 1 or the last one left is the last ewaste container for that level
    if len(container_list_ewaste) > 1 or (len(container_list_ewaste) == 1 and maxewastecontainers == True) :
        
        #If the first container is off the screen, then it will be deleted
        if container_list_ewaste[0][0] > WIDTH:
            del container_list_ewaste[0]

#Draws bullets                
def drawBullet(bullet_list):
    #Loop that goes through each position in the bullet list and uses the coordinates to draw the bullet image in the correct spot
    for bullet_pos in bullet_list:
        screen.blit(bulletPic, pygame.Rect(bullet_pos[0], bullet_pos[1], BULLET_SIZE, BULLET_SIZE)) 

#Adds a bullet to the bullet list at the current position of the character
def add_bullet(bullet_list):
    global charactercoordinate
    global characterright
    global characterleft
    
    #Checks which way the character is facing so it knows which side to fire the bullet
    if characterright == True:
        x_pos = charactercoordinate + 80
        y_pos = 490
        bullet_list.append([x_pos, y_pos])
        
    elif characterleft == True:
        x_pos = charactercoordinate - 100
        y_pos = 490
        bullet_list.append([x_pos, y_pos])        
    
#Updates the bullet list            
def update_bullet_pos(bullet_list):
    #Will not update if there are no bullets
    if len(bullet_list) > 0:
        
        #Goes through each bullet position and subtracts 20 from the y-coordinate to make the bullet shoot up
        for i in range(len(bullet_list)):
            bullet_list[i][1] -= 20

#Deletes bullets          
def del_bullet(bullet_list):
    global collided_bullet_index
    
    #Loops through all the bullet indices in the bullet index list and deletes them
    for i in range(len(collided_bullet_index)):
        del bullet_list[collided_bullet_index[i]]
        collisionSound.play()
    
    #Will only check if there is more than 0 bullet in the list
    if len(bullet_list) > 0:
        
        #Checks if a bullet is off the screen
        if bullet_list[0][1] < 0 - BULLET_SIZE:
            del bullet_list[0]
    
    #Resets the bullets that were collided after they're deleted
    collided_bullet_index = []

#Checks for collision with normal containers                
def normal_container_collision(bullet_list, container_list_normal, collided_normal_index, collided_bullet_index):
    global score
    
    #Loops through each bullet coordinate
    for i in range(len(bullet_list)):
        
        #Loops through each normal container coordinate
        for x in range(len(container_list_normal)):
             
            #Checks if the bullet coordinates are in range of any normal containers   
            if container_list_normal[x][0] <= bullet_list[i][0] <= container_list_normal[x][0] + 175 and container_list_normal[x][1] <= bullet_list[i][1] <= container_list_normal[x][1] + 60:
                
                #Will only add them to the collided list if it isn't in there already
                if x not in collided_normal_index:
                    collided_normal_index.append(x)
                    collided_bullet_index.append(i)
                    score -= 20

#Checks for collision with ewaste containers                    
def ewaste_container_collision(bullet_list, container_list_ewaste, collided_ewaste_index, collided_bullet_index):
    global score
    
    #Loops through each bullet coordinate
    for i in range(len(bullet_list)):
        
        #Loops through each ewaste container coordinate
        for x in range(len(container_list_ewaste)):
            
            #Checks if the bullet coordinates are in range of any ewaste containers    
            if container_list_ewaste[x][0] <= bullet_list[i][0] <= container_list_ewaste[x][0] + 175 and container_list_ewaste[x][1] <= bullet_list[i][1] <= container_list_ewaste[x][1] + 60:
                
                #Will only add them to the collided list if it isn't in there already
                if x not in collided_ewaste_index:
                    collided_ewaste_index.append(x)
                    collided_bullet_index.append(i)
                    score += 10

#Checks if you passed the level or not                
def level_check():
    global maxewastecontainers
    global ewastecountforlevel
    global ewastecount
    global score
    global goalscore
    global containerspeed
    global characterspeed
    global level
    global charactercoordinate
    global container_list_ewaste
    global container_list_normal
    global bullet_list
    global beginning
    global runningGame
    global gameOver
    global nextLevel
    global KEY_LEFT
    global KEY_RIGHT
    
    #Will only check if all the ewaste containers for that level has finished coming out
    if maxewastecontainers == True:
        
        #All ewaste container will have to be off the screen before it is checked
        if len(container_list_ewaste) == 0:
            
            #Checks if the score is lower than the goal
            if score < goalscore:
                runningGame = False
                gameOver = True
                maxewastecontainers = False
                KEY_LEFT = False
                KEY_RIGHT = False                    
                #Reads and updates the high score board
                read_highscore()
                update_highscore()
                
                #Resets game settings to level 1
                charactercoordinate = 0
                score = 0
                goalscore = 50
                ewastecountforlevel = 8
                ewastecount = 1
                level = 1
                containerspeed = 7
                characterspeed = 8
                beginning = 0
                container_list_ewaste = [[-200, 50]]
                container_list_normal = [[-450, 50]]
                bullet_list = []
                
                #Runs game over function
                gameover()
                
            #Checks if you achieved the goal
            elif score >= goalscore:
                #Makes game settings more difficult for the next level
                containerspeed += 3
                characterspeed += 2
                ewastecountforlevel += 5
                ewastecount = 1
                score = 0
                goalscore += 50
                level += 1
                container_list_ewaste = [[-200, 50]]
                container_list_normal = [[-450, 50]]
                bullet_list = []
                
                #Resets some settings for the start of the next level
                maxewastecontainers = False
                KEY_LEFT = False
                KEY_RIGHT = False
                nextLevel = True
                
                #Runs next level function
                next_level()

#Reads the high score file               
def read_highscore():
    global level
    global highscore
    
    #First adds your level to the list of high scores
    highscore.append(level)
    
    #Opens file
    highscoreFile = open("highscore.txt", "r")
    
    #Loops through each line of the file and adds the number to the high score list
    while True:
        text = highscoreFile.readline()
        text = text.rstrip("\n")
        if text == "":
            break
        
        highscore.append(int(text))
    
    #Closes file
    highscoreFile.close()

#Updates the high score board    
def update_highscore():
    global highscore
    
    #Sorts high score list
    highscore.sort(reverse=True)
    
    #Only takes the top 5 scores
    if len(highscore) > 5:
        highscore = highscore[:5]
    
    #Opens the file to write in
    highscoreFile = open("highscore.txt", "w")
    
    #Loops through the high score list and writes each number into the file
    for i in range(len(highscore)):
        highscoreFile.write(str(highscore[i]) + "\n")
    
    #Closes the file    
    highscoreFile.close()

#Game over screen
def gameover():
    global gameOver
    global runningMenu
    global runningHighScore
    
    #Loop that will constantly run the code until the user clicks out of it
    while gameOver:
        
        # Check all the events that happen
        for evnt in pygame.event.get():
            
            # If the user tries to close the window, then raise the "flag"
            if evnt.type == pygame.QUIT:
                gameOver = False
                runningMenu = False
            
            # Checks if the user clicked on an option
            if evnt.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                button = evnt.button
                
                #Exits the user out
                if backindicator.collidepoint(mx,my):
                    clickSound.play()
                    gameOver = False
                
                #Brings user to the high score page
                if highscoreindicator.collidepoint(mx,my):
                    clickSound.play()
                    runningHighScore = True
                    highscoreScreen()
                
        #Draws game over screen and checks where the mouse is constantly    
        mx, my, mb = getmouse()
        drawGameOver(screen, mx, my)
        pygame.display.flip()                    

#Draws the game over screen        
def drawGameOver(screen, mx, my):
    drawBackground()
    
    #Prints text
    text = fontLevel.render("Game Over" , 1, WHITE)
    screen.blit(text, pygame.Rect(350,300,200,100))
    
    pygame.draw.rect(screen, BLUE, backindicator, 0)
    text = fontScore.render("Menu" , 1, WHITE)
    screen.blit(text, pygame.Rect(40,635,50,50))
    
    pygame.draw.rect(screen, BLUE, highscoreindicator, 0)
    text = fontScore.render("High Scores" , 1, WHITE)
    screen.blit(text, pygame.Rect(800,635,50,50))
    
    #Checks to see if the mouse is hovering over an option. If it is, it will draw the button in a lighter colour.
    if backindicator.collidepoint(mx,my):
        pygame.draw.rect(screen, WATERBLUE, backindicator, 0)
        text = fontScore.render("Menu" , 1, WHITE)
        screen.blit(text, pygame.Rect(40,635,50,50))
        
    elif highscoreindicator.collidepoint(mx,my):
        pygame.draw.rect(screen, WATERBLUE, highscoreindicator, 0)
        text = fontScore.render("High Scores" , 1, WHITE)
        screen.blit(text, pygame.Rect(800,635,50,50))     
    
    pygame.display.flip()    

#Next level screen        
def next_level():
    global nextLevel
    global gameOver
    global runningMenu
    global runningHighScore
    global runningGame
    global charactercoordinate
    global score
    global goalscore
    global ewastecountforlevel
    global ewastecount
    global level
    global beginning
    global containerspeed
    global characterspeed
    global container_list_ewaste
    global container_list_normal
    global bullet_list
    
    #Loops that continuously runs the code until the user clicks out of it
    while nextLevel:
        
        # Check all the events that happen
        for evnt in pygame.event.get():
            
            # If the user tries to close the window, then raise the "flag"
            if evnt.type == pygame.QUIT:
                nextLevel = False
                runningGame = False
                runningMenu = False
            
            # Checks if the user clicked on an option in the menu 
            if evnt.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                button = evnt.button
                
                #User ends the game
                if quitlevelindicator.collidepoint(mx,my):
                    clickSound.play()
                    
                    #Reset game settings to level one
                    nextLevel = False
                    runningGame = False
                    gameOver = True
                    
                    read_highscore()
                    update_highscore()                    
                    
                    charactercoordinate = 0
                    score = 0
                    goalscore = 50
                    ewastecountforlevel = 8
                    ewastecount = 1
                    level = 1
                    containerspeed = 7
                    characterspeed = 8
                    beginning = 0
                    container_list_ewaste = [[-200, 50]]
                    container_list_normal = [[-450, 50]]
                    bullet_list = []
                    
                    #Runs game over function
                    gameover()
                
                #User chooses to play the next level    
                if nextlevelindicator.collidepoint(mx,my):
                    clickSound.play()
                    
                    #Exits out of the next level screen and the game continues
                    nextLevel = False
                
        #Draws the next level screen and checks where the mouse is constantly    
        mx, my, mb = getmouse()
        draw_next_level(screen, mx, my)
        pygame.display.flip()
 
#Draws next level screen     
def draw_next_level(screen, mx, my):
    global level
    global goalscore
    
    drawBackground()
    
    #Prints text (which level you're on and your goal)
    text = fontLevel.render("Level " + str(level), 1, WHITE)
    screen.blit(text, pygame.Rect(400,300,200,100))    
    
    text = fontLevel.render("New Goal: " + str(goalscore) , 1, WHITE)
    screen.blit(text, pygame.Rect(300,400,200,100))
    
    pygame.draw.rect(screen, BLUE, quitlevelindicator, 0)
    text = fontScore.render("Quit" , 1, WHITE)
    screen.blit(text, pygame.Rect(50,630,50,50))
    
    pygame.draw.rect(screen, BLUE, nextlevelindicator, 0)
    text = fontScore.render("Next Level" , 1, WHITE)
    screen.blit(text, pygame.Rect(810,635,50,50))
    
    #Checks to see if the mouse is hovering over an option. If it is, it will draw the button in a lighter colour.
    if backindicator.collidepoint(mx,my):
        pygame.draw.rect(screen, WATERBLUE, quitlevelindicator, 0)
        text = fontScore.render("Quit" , 1, WHITE)
        screen.blit(text, pygame.Rect(50,630,50,50))
        
    elif nextlevelindicator.collidepoint(mx,my):
        pygame.draw.rect(screen, WATERBLUE, nextlevelindicator, 0)
        text = fontScore.render("Next Level" , 1, WHITE)
        screen.blit(text, pygame.Rect(810,635,50,50))    
    
    pygame.display.flip()   

#Draws the high score screen    
def drawHighscore(screen, mx, my):
    global highscore
    
    drawBackground()
    
    #Prints text
    text = fontLevel.render("High Scores" , 1, WHITE)
    screen.blit(text, pygame.Rect(350,100,200,100))
    
    pygame.draw.rect(screen, BLUE, backindicator, 0)
    text = fontScore.render("Menu" , 1, WHITE)
    screen.blit(text, pygame.Rect(40,635,50,50))
    
    #Checks to see if the mouse is hovering over an option. If it is, it will draw the button in a lighter colour.
    if backindicator.collidepoint(mx,my):
        pygame.draw.rect(screen, WATERBLUE, backindicator, 0)
        text = fontScore.render("Menu" , 1, WHITE)
        screen.blit(text, pygame.Rect(40,635,50,50))       

    #Loops through each high score in the list and prints it on the screen in order    
    for i in range(len(highscore)):
        text = fontLevel.render(str(i+1) + ". Level " + str(highscore[i]) , 1, WHITE)
        screen.blit(text, pygame.Rect(375,150 + 75*(i+1),50,50))
    
    pygame.display.flip()

#High score             
def highscoreScreen():
    global gameOver
    global runningMenu
    global runningHighScore
    global highscore
    
    #Continuously runs the code until the user clicks out
    while runningHighScore:
        
        # Check all the events that happen
        for evnt in pygame.event.get():
            
            # If the user tries to close the window, then raise the "flag"
            if evnt.type == pygame.QUIT:
                runningHighScore = False
                gameOver = False
                runningMenu = False
            
            # Checks if the user clicked on an option in the menu 
            if evnt.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                button = evnt.button
                
                #Clicks out of the high score screen
                if backindicator.collidepoint(mx,my):
                    clickSound.play()
                    runningHighScore = False
                    gameOver = False
                    highscore = [] #Resets the highscore list right before it exits
                
        #Draws the high score screen and checks where the mouse is constantly    
        mx, my, mb = getmouse()
        drawHighscore(screen, mx, my)
        pygame.display.flip()                            
        
#Runs the menu continously until the user clicks on an option
while runningMenu:
    
    # Check all the events that happen
    for evnt in pygame.event.get():
        
        # If the user tries to close the window, then raise the "flag"
        if evnt.type == pygame.QUIT:
            runningMenu = False
        
        # Checks if the user clicked on an option in the menu 
        if evnt.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evnt.pos
            button = evnt.button
            
            #Starts the game if play button is clicked
            if playindicator.collidepoint(mx,my):
                clickSound.play()
                
                #Will only show the level 1 screen if the game has just begun
                if beginning == 0:
                    beginning += 1
                    
                    drawBackground()
                    
                    text = fontLevel.render("Level " + str(level), 1, WHITE)
                    screen.blit(text, pygame.Rect(400,300,200,100))    
                    
                    text = fontLevel.render("Goal: " + str(goalscore) , 1, WHITE)
                    screen.blit(text, pygame.Rect(380,400,200,100))   
                    
                    pygame.display.flip()  
                    pygame.time.wait(3000)
                
                runningGame = True
                
                #Continuously runs game loop until the user quits or loses
                while runningGame:
                    # Check all the events that happen
                    for evnt in pygame.event.get():
                        
                        # if the user tries to close the window, then raise the "flag"
                        if evnt.type == pygame.QUIT:
                            runningGame = False
                            runningMenu = False
                        
                        #Checks if the mouse was pressed
                        if evnt.type == pygame.MOUSEBUTTONDOWN:
                            mx, my = evnt.pos
                            button = evnt.button
                            
                            #Pauses game if the pause button was pressed
                            if backindicator.collidepoint(mx,my):
                                clickSound.play()
                                runningGame = False                            
                        
                        #Checks if a key was pressed    
                        if evnt.type == pygame.KEYDOWN:
                            
                            #Will change states to allow the character to move and face left if the left key was pressed
                            if evnt.key == pygame.K_LEFT:
                                KEY_LEFT = True
                                characterleft = True
                                characterright = False
                            
                            #Will change states to allow the character to move and face right if the right key was pressed
                            if evnt.key == pygame.K_RIGHT:
                                KEY_RIGHT = True
                                characterright = True
                                characterleft = False
                                
                            #Will change states to allow bullets to be shot if the space key was pressed    
                            if evnt.key == pygame.K_SPACE:
                                shoot = True
                                add_bullet(bullet_list)
                                gunSound.play()
                        
                        #Checks if any keys were lifted        
                        if evnt.type == pygame.KEYUP:
                            
                            #Changes states to stop the character from moving left if the left key was pressed
                            if evnt.key == pygame.K_LEFT:
                                KEY_LEFT = False
                            
                            #Changes states to stop the character from moving right if the right key was pressed  
                            if evnt.key == pygame.K_RIGHT:
                                KEY_RIGHT = False
                    
                    #Checks if the left key is True, if it is, it will move the character to the left by the current speed of the character            
                    if KEY_LEFT == True:
                        charactercoordinate -= characterspeed
                        
                        #Makes the character wrap around the the other side if they reached the edge of the screen
                        if charactercoordinate < -44:
                            charactercoordinate = WIDTH    
                            
                    #Checks if the right key is True, if it is, it will move the character to the right by the current speed of the character    
                    if KEY_RIGHT == True:
                        charactercoordinate += characterspeed
                        
                        #Makes the character wrap around the the other side if they reached the edge of the screen
                        if charactercoordinate > WIDTH:
                            charactercoordinate = -44
                    
                    #Chooses a random number that will determine which type of container should be drawn
                    container_type = random.randint(1,10) 

                    drawBackground()
                    
                    drawClouds(cloudx, cloudy, size)
                    drawClouds(cloudx_2, cloudy_2, size_2)
                    drawClouds(cloudx_3, cloudy_3, size_3)
                    
                    #Checks whether the charcter is facing right or left and will draw the corresponding character
                    if characterright == True:
                        drawCharacterRight(charactercoordinate)
                    
                    elif characterleft == True:
                        drawCharacterLeft(charactercoordinate)
                    
                    #Will only draw the bullets if bullets have been shot    
                    if shoot == True:
                        drawBullet(bullet_list)
                    
                    #Updates bullet positions
                    update_bullet_pos(bullet_list)
                    
                    #Adds, draws, and updates the normal and ewaste containers
                    add_containers(container_list_ewaste, container_list_normal)
                    draw_containers_ewaste(container_list_ewaste)
                    draw_containers_normal(container_list_normal)
                    update_container_pos(container_list_ewaste, container_list_normal, containerspeed)
                    normal_container_collision(bullet_list, container_list_normal, collided_normal_index, collided_bullet_index)
                    ewaste_container_collision(bullet_list, container_list_ewaste, collided_ewaste_index, collided_bullet_index)
                    
                    #Deletes the ewaste and normal containers, as well as the bullets
                    del_container(container_list_normal, container_list_ewaste)
                    del_bullet(bullet_list)
                    
                    #Prints the current score at the bottom of the screen
                    text = fontScore.render("Score: " + str(score) , 1, WHITE)
                    screen.blit(text, pygame.Rect(WIDTH - 200, HEIGHT - 50, 50, 50))
                    
                    #Constantly checks if you passed or not but only runs through the whole function when the level is over
                    level_check()
                    
                    #Draws back button
                    pygame.draw.rect(screen, BLUE, backindicator, 0)
                    text = fontScore.render("Pause" , 1, WHITE)
                    screen.blit(text, pygame.Rect(40,635,50,50))                    
                    
                    mx, my, mb = getmouse()
                    
                    #Checks if the mouse is hovering over the mouse button. If it is, it will draw a light rectangle
                    if backindicator.collidepoint(mx,my):
                        pygame.draw.rect(screen, WATERBLUE, backindicator, 0)
                        text = fontScore.render("Pause" , 1, WHITE)
                        screen.blit(text, pygame.Rect(40,635,50,50))                      
                    
                    pygame.display.flip()
                    pygame.time.wait(10)                
            
            #Checks if the user clicked the instructions option   
            elif instructionsindicator.collidepoint(mx,my):
                clickSound.play()
                
                runningInstructions = True
                
                #Continuously runs the code until the user clicks out
                while runningInstructions:
                # Check all the events that happen
                    for evnt in pygame.event.get():
                       
                       # If the user tries to close the window, then raise the "flag"
                        if evnt.type == pygame.QUIT:
                            runningInstructions = False
                            runningMenu = False
                       
                       # Checks if the user clicked on an option in the menu 
                        if evnt.type == pygame.MOUSEBUTTONDOWN:
                            mx, my = evnt.pos
                            button = evnt.button
                            
                            #Exits out of the instructions page and goes back to the menu loop
                            if backindicator.collidepoint(mx,my):
                                clickSound.play()
                                runningInstructions = False                              
                        
                        #Constantly draws the instructions screen and gets the coordinates of the mouse   
                        mx, my, mb = getmouse()
                        drawInstructions(screen, mx, my)
                        pygame.display.flip()                        
            
            #Checks if the user clicked on quit and will exit out of the program if they did        
            elif quitindicator.collidepoint(mx,my):
                clickSound.play()
                runningMenu = False 
        
        #Draws menu and checks where the mouse is constantly    
        mx, my, mb = getmouse()
        drawMenu(screen, mx, my)
        pygame.display.flip()            
    
pygame.quit()            