"""
Makes a series of maps of the united states and displays seedling data per state
depending on the year (the year is changed by pressing certain letters)
"""

import pygame
import sys
import matplotlib.path
import us_map
import pandas as pd

# initializes the screen
WHITE = (250, 250, 250)
width, height = 2000, 1000
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)
filename = 'seedlings_2008.csv'
# draw_states()



def remap_interval(val, input_start, input_end, output_start, output_end):
    """
    takes an input interval, a value in the input interval and returns a 
    subsequent value in the output interval 

    >>> remap_interval(5, 0, 10, 0, 20)
    10
    """
    #everything needs to be a float
    float(val)
    float(input_end)
    float(input_start)
    float(output_end)
    float(output_start)

    #everything needs to be a float
    input_space = float(input_end-input_start)
    output_space = float(output_end-output_start)
    diff = val - input_start

    #gets the value in a form that compares it to the input interval
    ratio = output_space/input_space
    newval = output_start + diff*ratio
    return int(newval)

def panda_file_to_list(file_name, title1, title2):
    """
    The opens a saved csv file and convert it to a panda file. The 
    panda file is separated into columns and the columns are made into
    lists. The lists are the output of the funciton. 
    """
    datafile = pd.read_csv(file_name) #opens a data file

    # converts the data file into columns
    for col in datafile.columns:
        datafile[col] = datafile[col].astype(str)
    column1 = datafile[title1]
    column2 = datafile[title2].astype(float)

    # creates lists from the columns
    list1 = []
    list2 = []
    for col_value in column2:
        list1.append(col_value)
    for col_value in column1:
        list2.append(col_value)
    output = [list1, list2]

    return output


def point_in_polygon(pt, polygon):
    """Returns True iff `pt` is inside `polygon`.
    `polygon` is a list of tuples `(x, y)`."""
    return matplotlib.path.Path(polygon).contains_point(pt)

# Draw the polygons for the state.
def draw_states():
    """
    Defines the states depending on the data file being read. Draws the 
    states in pygame and color codes them (in grayscale) depending on the 
    value associated with each state.
    """
    # grayscale values
    TWELVE = (0, 0, 0)
    ELEVEN = (40,40,40)
    TEN = (60, 60, 60)
    NINE = (80,80,80)
    EIGHT = (100, 100, 100)
    SEVEN = (120,120,120)
    SIX = (140,140,140)
    FIVE = (160, 160, 160)
    FOUR = (180,180,180)
    THREE = (200, 200, 200)
    TWO = (220,220,220)
    ONE = (250, 250, 250)

    # puts the grayscale values into a list
    COLOR = [ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE,TEN,ELEVEN,TWELVE]

    # used to update the filename
    
    info = panda_file_to_list(filename, 'code', 'total')
    seedlings_list = info[0]
    state_list = info[1]

    # creates the states in pygame 
    for state in state_list:
        for polygon in us_map.states[state]:
            # `polygon` points are tuples `(float, float)`. PyGame requires `(int, int)`.
            points = [(int(x), int(y)) for x, y in polygon]
            # Draw the interior
            data1 = remap_interval(seedlings_list[state_list.index(state)],600, 50000,1,len(COLOR)-1)
            # data1 = remap_interval(seedlings_list[state_list.index(state)],int(min(seedlings_list)), int(max(seedlings_list)),1,len(COLOR)-1)
            pygame.draw.polygon(screen, COLOR[data1], points)
            # Draw the boundary
            pygame.draw.polygon(screen, TWELVE, points, 2)

draw_states()

def what_state(mouse_position):
    """
    depending on the data file being used, this function get the position
    of the mouse and then returns what state the mouse is in.
    """
    # used to update the filename
    info = panda_file_to_list(filename, 'code', 'total')
    seedlings_list = info[0]
    state_list = info[1]

    # finds which state the mouse is in
    for state in state_list:
        for polygon in us_map.states[state]:
            mouse_in_state = any(point_in_polygon(pygame.mouse.get_pos(), polygon) for polygon in us_map.states[state])
            if mouse_in_state:
                return state

def update_lists():
    """
    updates the filename in the while true loop
    """
    info = panda_file_to_list(filename, 'code', 'total')
    return info

pygame.display.flip()
last_mouse_in_state = False
seedlings_list = update_lists()[0]
state_list = update_lists()[1]
BLACK = (0, 0, 0)
while True:
    if any(event.type == pygame.QUIT for event in pygame.event.get()):
        sys.exit()

    current_state = what_state(pygame.mouse.get_pos())
    try:
        current_index = state_list.index(current_state) # keeps track of the current index
    except:
        current_index = 0

    # creates the labels shown on the map
    data_text = 'seedling count in '+ str(current_state)+ ' = '+ str(seedlings_list[current_index]) 
    key_text = 'd = 2008, f = 2009, g = 2010, h = 2011, j = 2012, k = 2013'
    title_text = 'Seedling Count in the United States'
    myfont = pygame.font.SysFont('monospace', 25)
    label = myfont.render(data_text, 1, BLACK)
    key_label = myfont.render(key_text, 1, BLACK)
    title_label = myfont.render(title_text, 1, BLACK)


    # creates the backgrounds for the text
    background = pygame.Surface((screen.get_width()/1.5, screen.get_height()/14))
    key_background = pygame.Surface((screen.get_width(), screen.get_height()/14))
    title_background = pygame.Surface((screen.get_width(), screen.get_height()/18))

    # defines the positions
    textpos = background.get_rect()
    keypos = background.get_rect()
    titlepos = background.get_rect()

    # fills in the background color
    background.fill(WHITE)
    key_background.fill(WHITE)
    title_background.fill(WHITE)

    # makes text appear
    background.blit(label, textpos)
    key_background.blit(key_label, keypos)
    title_background.blit(title_label, titlepos)
    screen.blit(background, (0,625))
    screen.blit(key_background, (0, 675))
    screen.blit(title_background, (screen.get_width()/4, 0))
    pygame.display.flip()

    #updates the map depending on the key pressed
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_d]:
        filename = 'seedlings_2008.csv'
        draw_states()
    elif pressed[pygame.K_f]:
        filename = 'seedlings_2009.csv'
        draw_states()
    elif pressed[pygame.K_g]:
        filename = 'seedlings_2010.csv'
        draw_states()
    elif pressed[pygame.K_h]:
        filename = 'seedlings_2011.csv'
        draw_states()
    elif pressed[pygame.K_j]:
        filename = 'seedlings_2012.csv'
        draw_states()
    elif pressed[pygame.K_k]:
        filename = 'seedlings_2013.csv'
        draw_states()
    else:
        filename = 'seedlings_2008.csv' 
        draw_states()

    #updates the lists
    seedlings_list = update_lists()[0]
    state_list = update_lists()[1]


