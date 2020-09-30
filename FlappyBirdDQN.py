'''
This is simple process
'''

import random #for generating random numbers
import pygame #for game development
from pygame.locals import *  #Basic pygame imports
import sys  #We will use sys.exit() to exit the game

#Global varialbles for the game
FPS = 32   #Frame/sec
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN  = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUND_Y = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'Gallery/sprites/bird.png'
BACKGROUND = 'Gallery/sprites/back.png'
PIPE = 'Gallery/sprites/pipe.png'


def welcomeScreen():
    '''
    To shows welcome screen in front of the user
    '''
    #To get player X & Y value
    player_X = int(SCREENWIDTH/5)
    player_Y = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2) 
    
    #To get message X & Y value
    message_X = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2) 
    message_Y = int(SCREENHEIGHT * 0.13) 
    
    #To get base X value
    base_X = 0

    while True:
        for event in pygame.event.get():
            #If users click on the cross button the game will be exit
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #If the user presses space bar or up key button then the game will be start
            elif event.type==KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(player_X , player_Y))
                SCREEN.blit(GAME_SPRITES['message'],(message_X , message_Y))
                SCREEN.blit(GAME_SPRITES['base'],(base_X , GROUND_Y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)




def mainGame():
    '''
    This is the main function of the game 
    '''
    score = 0
    player_X = int(SCREENWIDTH/5)
    player_Y = int(SCREENWIDTH/2)
    base_X = 0

    #create 2 pipes for bliting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #My list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 +(SCREENWIDTH/2), 'y':newPipe2[0]['y']}
    ]
    
    #My list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 +(SCREENWIDTH/2), 'y':newPipe2[1]['y']}
    ]

    
    pipeVelocity_X = -4
    
    playerVelocity_Y = -9
    playerMaxVelocity_Y = 10
    playerMinVelocity_Y = -8
    playerAccleration_Y = 1

    playerFlapAccv = -8 #Velocity while flapping
    playerFlapped = False #it is true only when the bird is flapping


    #Game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_Y > 0:
                    playerVelocity_Y = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(player_X , player_Y , upperPipes , lowerPipes) #This funtion will return true if you get crash
        if crashTest:
            return

        #Check for score
        playerMidPos = player_X + GAME_SPRITES['player'].get_width()/2   #player middle position

        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2     #pipe middle position
            
            if pipeMidPos<= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()


        #player move
        if playerVelocity_Y < playerMaxVelocity_Y and not playerFlapped:
            playerVelocity_Y += playerAccleration_Y

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        player_Y = player_Y + min(playerVelocity_Y, GROUND_Y - player_Y - playerHeight)

        #Moves pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes , lowerPipes):

            upperPipe['x'] += pipeVelocity_X
            lowerPipe['x'] += pipeVelocity_X

        #Add a new pipe when the first pipe crosses left
        if 0<upperPipes[0]['x']<5:
            
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])


        #If the pipe is out of the screen , remove it
        if upperPipes[0]['x'] < - GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes): 
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'] , upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'] , lowerPipe['y']))
        
        SCREEN.blit(GAME_SPRITES['base'],(base_X , GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'],(player_X , player_Y))
 

        #Score bliting
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        
        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
             SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset, SCREENHEIGHT*0.12))
             xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


     
#Game over function
def isCollide(player_X , player_Y , upperPipes , lowerPipes):
    if player_Y > GROUND_Y - 25 or player_Y<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(player_Y < pipeHeight + pipe['y'] and abs(player_X - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    
    for pipe in lowerPipes:
        if(player_Y + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(player_X - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True



    return False

def getRandomPipe():
    '''
    Generate position of two pipe (one bottom straight and one top rotate) for bliting on the screen
    '''

    pipHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()- 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipHeight - y2 + offset
    pipe = [
        {'x':pipeX , 'y':-y1}, #upper pipe
        {'x':pipeX , 'y':y2} #lower pipe

    ]
    
    return pipe



if __name__ == "__main__":

    #This will be the main point from where our game will start
    pygame.init() #Initialize pygame module
    FPS_CLOCK = pygame.time.Clock() 
    pygame.display.set_caption('Flappy Bird by Bappy')
    
    #Kept all png number images in this dictionary
    GAME_SPRITES['numbers'] = (
        pygame.image.load('Gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/9.png').convert_alpha()
    )
    
    #kept the message,base,background,player & pipe image in this dictionary
    GAME_SPRITES["message"] = pygame.image.load('Gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES["base"] = pygame.image.load('Gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES["player"] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES["pipe"] = (
       pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
       pygame.image.load(PIPE).convert_alpha()
    )


    #Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('Gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('Gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('Gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('Gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('Gallery/audio/wing.wav')


    while True:
        welcomeScreen()  #shows welcome screen until users press the button
        mainGame()   #This is the main game function
        
        

    
