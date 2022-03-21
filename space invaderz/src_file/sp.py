import pygame
import random
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((900,600))

background = pygame.image.load("background.png")

pygame.display.set_caption("Space Invaderz")
icon = pygame.image.load("woman.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0


enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies = 6

for i in range(enemies):
	enemyImg.append(pygame.image.load("alien.png"))
	enemyX.append(random.randint(0, 800))
	enemyY.append(random.randint(60, 120))
	enemyX_change.append(0.7)
	enemyY_change.append(40)

rocketImg = pygame.image.load("rocket.png")
rocketX = 0
rocketY = 480
rocketX_change = 0
rocketY_change = 2
rocket_state = "ready"


def player(x, y):
	screen.blit(playerImg, (x, y))

def enemy(x, y, i):
	screen.blit(enemyImg[i], (x, y))

def attack(x, y):
	global rocket_state
	rocket_state = "fire"
	screen.blit(rocketImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, rocketX, rocketY):
	distance = ((enemyX-rocketX)**2 + (enemyY-rocketY)**2)**1/2
	if distance < 27:
		return True
	else:
		return False

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 736
scoreY = 20

game_over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
	score = font.render("Score : " + str(score_value), True, (255, 255, 255))
	screen.blit(score, (x, y))

def game_over_text():
	game_over = game_over_font.render("GAME OVER", True, (255, 255, 255))
	screen.blit(game_over, (250, 250))



running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				playerX_change = -0.9
			if event.key == pygame.K_d:
				playerX_change = 0.9
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				if rocket_state == "ready":
					rocketX = playerX
					attack(rocketX, rocketY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a or event.key == pygame.K_d:
				playerX_change = 0
	screen.fill((0,0,0,))

	screen.blit(background, (0,0))

	playerX += playerX_change

	if playerX <= 0:
		playerX = 0
	elif playerX >= 836:
		playerX = 836


	if rocketY <=0:
		rocketY = 480
		rocket_state = "ready"
	if rocket_state == "fire":
		attack(rocketX, rocketY)
		rocketY -= rocketY_change

	for i in range(enemies):

		if enemyY[i] >= 460:
			for j in range(enemies):
				enemyY[j] = 2000
			game_over_text()
			break

		enemyX[i] += enemyX_change[i]

		if enemyX[i] <= 0:
			enemyX_change[i] = 0.7
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 836:
			enemyX_change[i] = -0.7
			enemyY[i] += enemyY_change[i]
		collision = isCollision(enemyX[i], enemyY[i], rocketX, rocketY)
		if collision:
			rocketY = 480
			rocket_state = "ready"
			score_value += 1
			enemyX[i] = random.randint(0, 800)
			enemyY[i] = random.randint(60, 120)

		enemy(enemyX[i], enemyY[i], i)
	

	player(playerX, playerY)
	show_score(scoreX, scoreY)
	pygame.display.update()

