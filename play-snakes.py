# import the modules 
import pygame
import random
import os

#Below line is for initialising mixer which helps us to put music into our game
pygame.mixer.init()

# below line initialised all the packages of pygame
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green=(0, 255, 0)
yellow=(255, 255, 0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# background image
bgimg=pygame.image.load("game_files/img/snake.jpg")
#we have to scale our image so that it fits perfectly into the screen
bgimg=pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()  
#the start image
start_img=pygame.image.load("game_files/img/start.jpg")
start_img=pygame.transform.scale(start_img, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Play-Snakes")
pygame.display.update()     #we have to update our display so that everytime comes
#Creates a new Clock object that can be used to track an amount of time. The clock also provides several functions to help control a game's framerate.
clock = pygame.time.Clock()     

font = pygame.font.SysFont(None, 55)    #initialising font

# a function to write text on screen in pygame
def text_screen(text, color, x, y):         
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

# a function to plot the snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


# WELCOME WINDOW
def welcome():
    exit_game=False
    while not exit_game:
        gameWindow.fill(white)      #to fill the screen with white color
        gameWindow.blit(start_img, (0,0))       #this puts the start_img to background

        #to write something on the screen
        text_screen("Welcome To Snakes", yellow, 260, 240)      
        text_screen("Press space bar to play", yellow, 260, 280)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:         #pygame.QUIT stands for the close button on title bar
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:       #if user presses space then the game starts
                    pygame.mixer.music.load('game_files/sounds/back.wav')       #to lead the music file
                    pygame.mixer.music.play(-1)   #to play background music, -1 to play music infinitly
                    gameloop()      #to start the game loop the function we have defined below

        pygame.display.update()     #to update the display. NOTE: we have to always update our display
        clock.tick(60)  #clock tick sets the fps of the game. It is frames per second. increasing fps increases the speed of the game

# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 45
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(20, screen_width/2)         #to generate random int in python
    food_y = random.randint(20, screen_height/2)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    snk_list = []           #list that contains the snake. Our snake is basically the list. all the element co-ordinantes are stored in list and that forms the snake
    snk_length = 1

    # check if highscore file exist:        basically to handle that error
    if(not os.path.exists("game_files/highscore.txt")):
        with open("game_files/highscore.txt", "w")as f:         #note if we open file in write mode then automatically file gets created.
            f.write("0") 

    with open("game_files/highscore.txt","r") as f:
        highscore=f.read()

    while not exit_game:
        if game_over:
            with open("game_files/highscore.txt", "w")as f:
                f.write(str(highscore))
            gameWindow.fill(black)
            gameWindow.blit(start_img, (0,0))       #puts start_img if the game gets over

            text_screen("Your final Score: " + str(score), green, 280, 50)
            text_screen("HighScore: "+str(highscore), yellow, 315, 350)
            text_screen("Game Over! Press Enter to continue", white, 110, 450)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:          #K_RETURN is basically the ENTER key
                        welcome()
        else:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    exit_game = True

                #just the keys control to move the snake
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            #this is the proximity that checks if the food is near then it assues it to be eaten.
            if abs(snake_x - food_x)<14 and abs(snake_y - food_y)<14:       
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
                if score>int(highscore):
                    highscore=score

            gameWindow.fill(black)
            gameWindow.blit(bgimg, (0,0))   #sets bgimg to the background
            text_screen("Score: " + str(score)+" HighScore: "+str(highscore), yellow, 5, 5) #prints the score everytime snake eats
            pygame.draw.rect(gameWindow, green, [food_x, food_y, snake_size-8, snake_size-8])       #to create new food

            #this is the head of the snake and it always appends the snake 
            #we have to cut the head of snake everytime otherwise its size always keeps on increasing
            head = []      
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            #we have to cut the head of snake everytime otherwise its size always keeps on increasing
            if len(snk_list)>snk_length:
                del snk_list[0]

            # to check if snake doesn't crosses the window
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True
                pygame.mixer.music.load('game_files/sounds/gameover.wav')
                pygame.mixer.music.play()   #to play background music

            # to check if snake doesn't collide with itself we check that the coordinate of head is not equal to any of the snake part
            if head in snk_list[:-1]:   #snk_list[:-1]means all the elements excluding the last element
                game_over=True
                pygame.mixer.music.load('game_files/sounds/gameover.wav')
                pygame.mixer.music.play()   #to play background music

            #to draw the snake
            plot_snake(gameWindow, white, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

#to start the game      
welcome()   
# --> ENJOY THE GAME AND TRY TO CREATE A NEW HIGH RECORD
