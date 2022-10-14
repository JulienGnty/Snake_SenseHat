from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED, DIRECTION_DOWN, DIRECTION_UP, DIRECTION_LEFT, DIRECTION_RIGHT
from time import sleep
import random

W = [255,255,255]
R = [255,0,0]
RD = [100,33,33]
B = [0,0,255]

START_SNAKE = [62,63]
START_MOUSE = [47]

RIGHT = +1
LEFT = -1
UP = -8
DOWN = +8

S = SenseHat()

def add_mouse(mouses,snakes):
    """
        Add 1 mouse in a random free tile of the grid
        Return mouses list
    """
    rnd = -1
    while rnd < 0:
        rnd = random.randint(0,63)
        if rnd in snakes or rnd in mouses:
            rnd = -1
            continue
        mouses.append(rnd)
    return mouses

def set_grid_pixels(snake, mouses):
    """
        Fill the grid with snake and mouses, then display the grid
    """
    global S
    grid = [W]*64
    grid[snake[0]] = RD
    for i in snake[1:]:
        grid[i] = R
    for i in mouses:
        grid[i] = B
    S.set_pixels(grid)

def move_snake(direction, snakes, mouses):
    """
        Return snake list and mouses list after moving the snake in the grid
    """
    if 0 <= snakes[0]+direction <= 63 and (0 <= (snakes[0]%8)+direction <= 7 or abs(direction)==8):
        if snakes[0]+direction in snakes:
            raise Exception("GAME OVER")
        if snakes[0]+direction in mouses:
            mouses = add_mouse(mouses,snakes)
            mouses.remove(snakes[0]+direction)
            snakes.append(-1)
        snakes[1:] = snakes[0:len(snakes)-1]
        snakes[0] += direction
    return snakes, mouses

def main():
    try:
        global S
        snake_list = START_SNAKE[:]
        #mouse_list = START_MOUSE[:]
        mouse_list = add_mouse([],snake_list)
        set_grid_pixels(snake_list, mouse_list)
        first_joystick_action = False
        direction = 0
        while True:
            already_treated = False
            for event in S.stick.get_events():
                if event.action in (ACTION_PRESSED, ACTION_HELD) and not already_treated:
                    first_joystick_action = True
                    if event.direction == DIRECTION_DOWN:
                        direction = DOWN
                        already_treated = True
                    if event.direction == DIRECTION_UP:
                        direction = UP
                        already_treated = True
                    if event.direction == DIRECTION_RIGHT:
                        direction = RIGHT
                        already_treated = True
                    if event.direction == DIRECTION_LEFT:
                        direction = LEFT
                        already_treated = True
            if first_joystick_action:
                snake_list, mouse_list = move_snake(direction,snake_list,mouse_list)
                set_grid_pixels(snake_list, mouse_list)
            sleep(0.25)
    except KeyboardInterrupt as e:
        S.clear()
    except BaseException as e:
        S.show_message("GAME OVER")
        S.clear()

if __name__ == "__main__":
    main()
