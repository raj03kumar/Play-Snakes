import pygame
import random
import os

pygame.mixer.init()

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
bgimg=pygame.image.load("snake.jpg")
bgimg=pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

start_img=pygame.image.load("start.jpg")
start_img=pygame.transform.scale(start_img, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snakes")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# WELCOME WINDOW
def welcome():
    exit_game=False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(start_img, (0,0))

        text_screen("Welcome To Snakes", yellow, 260, 240)
        text_screen("Press space bar to play", yellow, 260, 280)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    pygame.mixer.music.load('back.wav')
                    pygame.mixer.music.play(-1)   #to play background music -1 to play music infinitly
                    gameloop()

        pygame.display.update()
        clock.tick(60)

# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    snk_list = []
    snk_length = 1

    # check if highscore file exist:
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w")as f:
            f.write("0") 

    with open("highscore.txt","r") as f:
        highscore=f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w")as f:
                f.write(str(highscore))

            gameWindow.fill(black)
            gameWindow.blit(start_img, (0,0))
            # text_screen("Game Over! Press Enter to continue", white, screen_width/2, screen_height/2)
            text_screen("Your final Score: " + str(score), green, 280, 50)
            text_screen("HighScore: "+str(highscore), yellow, 315, 350)
            text_screen("Game Over! Press Enter to continue", white, 110, 450)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    exit_game = True

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

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<14 and abs(snake_y - food_y)<14:
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
                if score>int(highscore):
                    highscore=score

            gameWindow.fill(black)
            gameWindow.blit(bgimg, (0,0))
            text_screen("Score: " + str(score)+" HighScore: "+str(highscore), yellow, 5, 5)
            pygame.draw.rect(gameWindow, green, [food_x, food_y, snake_size-8, snake_size-8])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            # to check if snake doesn't crosses the window
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()   #to play background music

            # to check if snake doesn't collide with itself we check that the coordinate of head is not equal to any of the snake part
            if head in snk_list[:-1]:   #snk_list[:-1]means all the elements excluding the last element
                game_over=True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()   #to play background music

            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, white, snk_list, snake_size)


        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

#to start the game
welcome()