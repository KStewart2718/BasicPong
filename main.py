import random

import pygame as pg
import sys
import numpy as np
from pygame.locals import *

# Initialise the PyGame Engine
pg.init()


def main():

    # Creates a Clock object to manage FPS
    FPS = 60
    gameClock = pg.time.Clock()

    # Predefined colour values for ease of use (R, G, B)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Sets and tracks score to be displayed
    playerScore = 0
    enemyScore = 0

    # Creates font objects
    pointObj = pg.font.Font(None, 32)
    endTextObject = pg.font.Font(None, 96)

    # Sets end screen text to be displayed once the win condition has been met
    playerWin = endTextObject.render("PLAYER WINS", True, WHITE, None)
    enemyWin = endTextObject.render("ENEMY WINS", True, WHITE, None)

    # Define Screen Information
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Creates a window of fixed size (x,y), with the bottom right-most
    # corner being of position (x,y)
    DISPLAYSURFACE = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Creates two random integers between -5 and 5 while excluding 0
    randY = random.randint(-5, 5)
    randX = random.randint(-5, 5)

    while randY == 0:
        randY = random.randint(-5, 5)
    while randX == 0:
        randX = random.randint(-5, 5)

    # Generates either 1 or -1 depending on the random number that was generated
    initDirectionY = randY/abs(randY)
    initDirectionX = randX/abs(randX)

    # Ball information
    ballX = SCREEN_WIDTH / 2
    ballY = SCREEN_HEIGHT / 2
    ballVelocityX = 2 * (initDirectionX/abs(initDirectionX))
    ballVelocityY = 1 * (initDirectionY/abs(initDirectionY))
    BALL_RADIUS = 5

    # Universal Rect Info
    PADDLE_WIDTH = 12
    PADDLE_HEIGHT = 60
    PADDLE_INSET = 20

    # Player info
    Player_xPos = PADDLE_INSET
    Player_yPos = (SCREEN_HEIGHT / 2) - PADDLE_HEIGHT / 2

    # Enemy info
    Enemy_xPos = SCREEN_WIDTH - PADDLE_INSET - PADDLE_WIDTH
    Enemy_yPos = (SCREEN_HEIGHT / 2) - PADDLE_HEIGHT / 2

    # Paddle Velocity (Number of pixels moved from an input per frame)
    VELOCITY = 5

    # Sets a background colour for the screen
    # Sets a title in the game window
    pg.display.set_caption("PONG")

    # Creates Player and Enemy Rects to be displayed on the first frame
    # when the game is initially loaded
    Player = pg.Rect((Player_xPos, Player_yPos), (PADDLE_WIDTH, PADDLE_HEIGHT))
    Enemy = pg.Rect((Enemy_xPos, Enemy_yPos), (PADDLE_WIDTH, PADDLE_HEIGHT))

    running = True

    # The Game Loop
    # This is where all game events occur, update and get drawn to the screen
    # until we QUIT the game
    while running:
        # Checks every event in the event queue for a QUIT event
        # If the QUIT event is found, the game closes
        for event in pg.event.get():
            if event.type == QUIT:
                # Uninitalises all PyGame modules
                pg.quit()
                # Exits the interpreter
                sys.exit()

        # Sets a background colour for the screen
        DISPLAYSURFACE.fill(BLACK)
        # Draws the center line of the centre screen
        pg.draw.line(DISPLAYSURFACE, WHITE, (400, 0), (400, 600))

        # Creates the display objects for the player points and enemy points
        # to be displayed on screen
        playerPoints = pointObj.render(str(playerScore), True, WHITE, None)
        enemyPoints = pointObj.render(str(enemyScore), True, WHITE, None)

        # Blits the player scores to the screen
        DISPLAYSURFACE.blit(playerPoints, (SCREEN_WIDTH / 4, 20))
        DISPLAYSURFACE.blit(enemyPoints, ((3 * SCREEN_WIDTH / 4), 20))

        # Draws our
        pg.draw.rect(DISPLAYSURFACE, WHITE, Enemy)
        pg.draw.rect(DISPLAYSURFACE, WHITE, Player)
        pg.draw.circle(DISPLAYSURFACE, WHITE, (ballX, ballY), BALL_RADIUS)


        if Player_yPos < 0:
            Player_yPos += 5
        if Player_yPos + PADDLE_HEIGHT > SCREEN_HEIGHT:
            Player_yPos -= 5

        if Enemy_yPos < 0:
            Enemy_yPos += 5
        if Enemy_yPos + PADDLE_HEIGHT > SCREEN_HEIGHT:
            Enemy_yPos -= 5

        if ballX - BALL_RADIUS <= Player_xPos + PADDLE_WIDTH:
            if Player_yPos <= ballY <= Player_yPos + PADDLE_HEIGHT:
                ballVelocityX = (ballVelocityX - 1) * -1
                ballVelocityY += 1

        if ballX + BALL_RADIUS >= Enemy_xPos:
            if Enemy_yPos <= ballY <= Enemy_yPos + PADDLE_HEIGHT:
                ballVelocityX = (ballVelocityX + 1) * -1
                ballVelocityY += 1

        if ballY - BALL_RADIUS <= 0 or ballY + BALL_RADIUS >= SCREEN_HEIGHT:
            ballVelocityY = ballVelocityY * -1

        ballX += ballVelocityX
        ballY += ballVelocityY

        if ballX + 2 * BALL_RADIUS < 0:
            ballX = SCREEN_WIDTH / 2
            ballY = SCREEN_HEIGHT / 2
            ballVelocityX = -1
            ballVelocityY = ballVelocityY/abs(ballVelocityY)
            enemyScore += 1

        if ballX - 2 * BALL_RADIUS > SCREEN_WIDTH:
            ballX = SCREEN_WIDTH / 2
            ballY = SCREEN_HEIGHT / 2
            ballVelocityX = 2
            ballVelocityY = ballVelocityY/abs(ballVelocityY)
            playerScore += 1

        Player = pg.Rect((Player_xPos, Player_yPos), (PADDLE_WIDTH, PADDLE_HEIGHT))
        Enemy = pg.Rect((Enemy_xPos, Enemy_yPos), (PADDLE_WIDTH, PADDLE_HEIGHT))

        pressed = pg.key.get_pressed()
        if pressed[K_UP] or pressed[K_w]:
            Player_yPos -= VELOCITY
        if pressed[K_DOWN] or pressed[K_s]:
            Player_yPos += VELOCITY
        if pressed[K_k]:
            Enemy_yPos += VELOCITY
        if pressed[K_i]:
            Enemy_yPos -= VELOCITY

        if playerScore == 5:
            ballVelocityX = 0
            ballVelocityY = 0
            playerPoints = pointObj.render(str(playerScore), True, GREEN, None)
            DISPLAYSURFACE.fill(BLACK)
            DISPLAYSURFACE.blit(playerPoints, (SCREEN_WIDTH / 4, 20))
            DISPLAYSURFACE.blit(playerWin, (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 25))
            pg.display.update()
            pg.time.delay(5000)
            main()
        if enemyScore == 5:
            ballVelocityX = 0
            ballVelocityY = 0
            enemyPoints = pointObj.render(str(enemyScore), True, GREEN, None)
            DISPLAYSURFACE.fill(BLACK)
            DISPLAYSURFACE.blit(enemyPoints, ((3 * SCREEN_WIDTH / 4), 20))
            DISPLAYSURFACE.blit(enemyWin, (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 25))
            pg.display.update()
            pg.time.delay(5000)
            main()

        # Changes aren't implemented until the update method is called
        pg.display.update()
        gameClock.tick(FPS)

    return 0


if "__name__" == main():
    main()
