import pygame
import sys
#from pygame.math import np.array
import random
import math
import time
import numpy as np

class FRUIT:
	def __init__(self):
		self.randomize()
	
	def draw_fruit(self):
		#create a rectangle 
		fruit_rect = pygame.Rect(int(self.pos[0]*cell_size),int(self.pos[1]*cell_size),cell_size,cell_size)
		#draw rect --> fruit
		pygame.draw.rect(screen, food_colour,fruit_rect)

	def randomize(self):
		self.x = random.randint(0,cell_number-1)
		self.y = random.randint(0,cell_number-1)
		self.pos = np.array([self.x,self.y])


class SNAKE:
	def __init__(self):
		self.body = [np.array([int(cell_number/2)-1,int(cell_number/2)-1]),np.array([int(cell_number/2)-1,int(cell_number/2)-1+1]),np.array([int(cell_number/2)-1,int(cell_number/2)-1+2])]#,np.array(list(4,10),np.array(list(3,10)]
		self.head = np.array([int(cell_number/2)-1,int(cell_number/2)-1])
		self.direction = up
		self.new_block = False
	def draw_snake(self):
		f = 0
		for block in self.body:
			if(f==0):
				x_pos = int(block[0] * cell_size)
				y_pos = int(block[1] * cell_size)
				block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
				pygame.draw.rect(screen,head_colour,block_rect)
				f = 1
			else:
				x_pos = int(block[0] * cell_size)
				y_pos = int(block[1] * cell_size)
				block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
				pygame.draw.rect(screen,snake_colour,block_rect)


	def move_snake(self,dircn):
		if self.new_block == True:
			# body_copy = self.body
			# body_copy.insert(0,body_copy[0] + direction)
			# self.body = body_copy[:]
			self.body.insert(0,self.head + dircn)
			self.new_block = False
			self.head = self.body[0]
		else:
			self.body.insert(0,self.head + dircn) 
			# self.body = self.body[:len(self.body)-1]
			self.body.pop()
			self.head = self.body[0]
		self.direction = np.array(self.head - self.body[1])



	def add_block(self):
		self.new_block = True

	# def reset(self):
	# 	self.body = [np.array(list(5,10),np.array(list(4,10),np.array(list(3,10)]
	# 	self.direction = np.array(list(0,0)


class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()
		self.state = {"front":-1,"left":-1,"right":-1,"food_angle":-1,"direction":  self.snake.direction}
		self.score = 0
	def update(self,dircn):
		self.snake.move_snake(dircn)
		self.check_collision()
		# self.check_fail()
	def draw_elements(self):
		self.snake.draw_snake()
		self.fruit.draw_fruit()

	def check_collision(self):
		if (self.fruit.pos == self.snake.head).all():
			self.fruit.randomize()
			self.snake.add_block()
			self.score +=1
		for block in self.snake.body[1:]:
			if (block == self.fruit.pos).all():
				self.fruit.randomize()

	def check_fail(self):
		if not 0 <= self.snake.head[0] < cell_number or not 0 <= self.snake.head[1] < cell_number:
			return True

		for block in self.snake.body[1:]:
			if (block == self.snake.body[0]).all():
				return True
		return False




	def get_game_state(self):
		dist_head_food = ((self.snake.body[0][0] - self.fruit.pos[0])**2 +(self.snake.body[0][1] - self.fruit.pos[1])**2)**(1/2)
		perp_x = self.fruit.pos[0] - self.snake.body[0][0]
		perp_y = self.fruit.pos[1] - self.snake.body[0][1]
		self.state["direction"] = self.snake.direction
		if (self.snake.direction == up).all():
			for i in range(1,4):
				if self.snake.body[0][0] + i == self.fruit.pos[0] or self.snake.body[0][0] + i == cell_number :
					self.state["right"] = 1
				else: self.state["right"] = 0

				if self.snake.body[0][0] - i == self.fruit.pos[0] or self.snake.body[0][0] - i == 0 :
					self.state["left"] = 1
				else:
					self.state["left"] = 0


				if self.snake.body[0][1] - i == self.fruit.pos[1] or self.snake.body[0][1] - i == 0 :
					self.state["front"] = 1
				else:
					self.state["front"] = 0 

			self.state["food_angle"] = perp_x/dist_head_food



		elif (self.snake.direction == down).all():
			for i in range(1,4):
				if self.snake.body[0][0] + i == self.fruit.pos[0] or self.snake.body[0][0] + i == cell_number :
					self.state["left"] = 1
				else: self.state["left"] = 0

				if self.snake.body[0][0] - i == self.fruit.pos[0] or self.snake.body[0][0] - i == 0 :
					self.state["right"] = 1
				else:
					self.state["right"] = 0


				if self.snake.body[0][1] + i == self.fruit.pos[1] or self.snake.body[0][1] + i == cell_number :
					self.state["front"] = 1
				else:
					self.state["front"] = 0

			self.state["food_angle"] = -perp_x/dist_head_food


		elif (self.snake.direction == left).all():
			for i in range(1,4):
				if self.snake.body[0][0] - i == self.fruit.pos[0] or self.snake.body[0][0] - i == 0 :
					self.state["front"] = 1
				else:
					self.state["front"] = 0


				if self.snake.body[0][1] + i == self.fruit.pos[1] or self.snake.body[0][1] + i == cell_number :
					self.state["left"] = 1
				else:
					self.state["left"] = 0

				if self.snake.body[0][1] - i == self.fruit.pos[1] or self.snake.body[0][1] - i == 0 :
					self.state["right"] = 1
				else:
					self.state["right"] = 0
			self.state["food_angle"] = -perp_y/dist_head_food


		elif (self.snake.direction == right).all():
			for i in range(1,4):
				if self.snake.body[0][0] + i == self.fruit.pos[0] or self.snake.body[0][0] + i == 0 :
					self.state["front"] = 1
				else:
					self.state["front"] = 0


				if self.snake.body[0][1] + i == self.fruit.pos[1] or self.snake.body[0][1] + i == cell_number :
					self.state["right"] = 1
				else:
					self.state["right"] = 0

				if self.snake.body[0][1] - i == self.fruit.pos[1] or self.snake.body[0][1] - i == 0 :
					self.state["left"] = 1
				else:
					self.state["left"] = 0

			
			self.state["food_angle"] = perp_y/dist_head_food



		return self.state





	# def game_over(self):
	# 	pygame.quit()
	# 	sys.exit()



def play_game(game,screen, clock,direction):
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
          
        screen.fill((175,215,70))

        game.draw_elements()
        game.update(direction)
        state = game.get_game_state()
        pygame.display.set_caption("SCORE: " + str(game.score))
        pygame.display.update()
        clock.tick(50000)

        return np.array(game.snake.head), game.fruit.pos, game.score, state


def generate_game():
	game = MAIN()
	return game




pygame.init()


red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)
food_colour = (126,166,114)
snake_colour = red#(183,111,122)
screen_colour = (175,215,70)
head_colour = black
cell_size = 10
cell_number = 50
resolution = (cell_number * cell_size, cell_number * cell_size)



screen  = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()








#Vectors
up = np.array([0,-1])
right = np.array([1,0])
down = np.array([0,1])
left = np.array([-1,0])
no_direction = np.array([0,0])

# main_game = MAIN()

# while True:
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			pygame.quit()
# 			sys.exit()
# 		if event.type == SCREEN_UPDATE:
# 			main_game.update()
# 		if event.type == pygame.KEYDOWN:
# 			if event.key == pygame.K_UP:
# 				if main_game.snake.direction.y != 1:
# 					main_game.snake.direction = np.array(list(0,-1)
# 			if event.key == pygame.K_RIGHT:
# 				if main_game.snake.direction.x != -1:
# 					main_game.snake.direction = np.array(list(1,0)
# 			if event.key == pygame.K_DOWN:
# 				if main_game.snake.direction.y != -1:
# 					main_game.snake.direction = np.array(list(0,1)
# 			if event.key == pygame.K_LEFT:
# 				if main_game.snake.direction.x != 1:
# 					main_game.snake.direction = np.array(list(-1,0)
# 			# if event.key == pygame.K_SPACE:
# 			# 	time.sleep(10)

# 	screen.fill((175,215,70))
# 	main_game.draw_elements()
# 	pygame.display.update()
# 	clock.tick(60)


# g = generate_game()
# while True:
# 	play_game(g,screen,clock)
