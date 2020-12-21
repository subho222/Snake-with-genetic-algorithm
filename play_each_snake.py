import numpy as np
from Snake import *
from neural_network import *

# def convert(predictions,current):
# 	x = np.argmax(predictions)
# 	if(x == 0):
# 		return current
# 	elif(x == 1):
# 		return left
# 	elif(x==2):
# 		return right

def check_fail_temp(snake,snake_head):
		if not 0 <= snake_head[0] < cell_number or not 0 <= snake_head[1] < cell_number:
			return True

		for block in snake[1:]:
			if (block == snake_head).all():
				return True
		return False




def collision_with_boundaries(snake_start):
    if not 0 <= snake_start[0] < cell_number or not 0 <= snake_start[1] < cell_number:
    	return True
    return False


def collision_with_self(snake_start, snake_position):
    for block in snake_position[1:]:
    	if (block == snake_start).all():
    		return True
    return False
    # if snake_start in snake_position[1:]:
    #     return 1
    # else:
    #     return 0


def run(indivisual,screen,clock):
	steps_per_game = 5000
	max_score = -1
	game = generate_game()
	snake_head = np.array(game.snake.head)
	fruit_pos = np.array(game.fruit.pos)
	score = game.score
	score1 = score2 = score3 = 0
	same_direction = 0 
	steps = 0
	prev_direction = 0
	play_area_matrix = np.zeros(shape = (resolution))
	prev_score = 0
	for _ in range(steps_per_game):
		game_state = game.get_game_state()
		front = game_state["front"]
		left = game_state["left"]
		right = game_state["right"]
		angle_with_fruit = game_state["food_angle"]
		curr_direction = game_state["direction"]
		features = np.array([front,left,right,angle_with_fruit]).reshape(-1,4)
		predictions = think_with_NN(features, indivisual)
		predicted_direction = np.argmax(predictions) -1
		if predicted_direction == prev_direction:
			same_direction+=1
		else:
			same_direction=0
			prev_direction = predicted_direction
		
		new_direction = curr_direction
		if predicted_direction == -1:
			new_direction = np.array([new_direction[1], -new_direction[0]])
		if predicted_direction == 1:
			new_direction = np.array([-new_direction[1], new_direction[0]])
		# game_copy = game
		# game.snake.direction = curr_direction
		nex = snake_head + curr_direction
		if collision_with_boundaries(snake_head) or collision_with_self(nex,game.snake.body):
			score1+= -150
			break
		else:
			score1 += 0
		#game.snake.direction = new_direction
		snake_head, fruit_pos, score, state = play_game(game,screen,clock,new_direction)
		if score == prev_score + 1:
			prev_score = score 
			play_area_matrix = np.zeros(shape = (resolution))
		else:
			prev_score = score
		if score > max_score:
			max_score = score
		if same_direction > 8 and predicted_direction != 1:
			score2 -= 1
		else:
			score2 += 2
		play_area_matrix[snake_head[0],snake_head[1]] += 1
		random_idx1 = random.randint(0,resolution[0]-1)
		random_idx2 = random.randint(0,resolution[0]-1)
		if play_area_matrix[snake_head[0],snake_head[1]] - play_area_matrix[random_idx1,random_idx2]  >= 10:
			score3 += -100
			break




	

		# if predicted_direction == 0:
		# 	new_direction = curr_direction
		# 	same_direction +=1
		# #print(predicted_direction)
		# elif(predicted_direction == 1):
		# 	new_direction = left
			
		# else:
		# 	new_direction = right

		# game_copy = game
		# game_copy.snake.direction = new_direction
		# game_copy.snake.move_snake()
		# if(game_copy.check_fail()):
		# 	score1 += -100
		# 	break
		# game.snake.direction = new_direction
		# game.update()
		# snake_head, fruit_pos, score, state = play_game(game,screen,clock)
		# if(score>max_score): max_score = score
		# if(same_direction > 10 and (predicted_direction == curr_direction).all()):
		# 	score2 += -10
		# else:
		# 	score2 += 20
		# steps+=1
	return score1 + score2 + score3 +  max_score * 5000





		


	