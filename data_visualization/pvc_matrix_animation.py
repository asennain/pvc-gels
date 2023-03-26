import pygame
import pandas as pd 
from time import sleep


def main():
    # Initialize Pygame
    pygame.init()


    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Set up the screen
    SCREEN_WIDTH = SCREEN_HEIGHT = 475

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PVC Gel Matrix")

    # Set up the squares
    square_size = 100
    square_padding = 100
    square1_pos = (square_padding, square_padding)
    square2_pos = (SCREEN_WIDTH - square_padding - square_size, square_padding)
    square3_pos = (square_padding, SCREEN_HEIGHT - square_padding - square_size)
    square4_pos = (SCREEN_WIDTH - square_padding - square_size, SCREEN_HEIGHT - square_padding - square_size)

    # square1_color = WHITE
    # square2_color = WHITE
    # square3_color = WHITE
    # square4_color = WHITE

    # Set up the clock
    clock = pygame.time.Clock()

    # Read the DataFrame and populate list of voltages for each junction before iterating through animation loop
    volt_data = pd.read_excel(
        io = r"C:\Users\asenn\OneDrive\School\Research\SPIE 2023\Data\Position Sensor\positionsensing(processed).xlsx",
        header = 18,
        index_col = 0,
        usecols = ["Time", "CH111", "CH112", "CH113", "CH114"]
    )


    j1_voltages = list(volt_data["CH111"])
    j2_voltages = list(volt_data["CH112"])
    j3_voltages = list(volt_data["CH113"])
    j4_voltages = list(volt_data["CH114"])

    # Now zip lists together to form a list of tuples (psuedo-array)
    # Be mindful to convert zip object to list
    volt_data = list(zip(j1_voltages, j2_voltages, j3_voltages, j4_voltages))

    # Main animation loop
    # Iterates through a list of tuples stored in # volt_data 
    for volt_tuple in volt_data: 

        # Find intensity of junction based on voltage
        intensity_list = volt_to_intensity(volt_tuple)

        # Change square colors based on intensity value
        junction_colors = intensity_to_RGB(intensity_list)
    
        square1_color = junction_colors[0]
        square2_color = junction_colors[1]
        square3_color = junction_colors[2]
        square4_color = junction_colors[3]


        # Draw the squares
        screen.fill(WHITE)
        pygame.draw.rect(screen, square1_color, (square1_pos[0], square1_pos[1], square_size, square_size))
        pygame.draw.rect(screen, square2_color, (square2_pos[0], square2_pos[1], square_size, square_size))
        pygame.draw.rect(screen, square3_color, (square3_pos[0], square3_pos[1], square_size, square_size))
        pygame.draw.rect(screen, square4_color, (square4_pos[0], square4_pos[1], square_size, square_size))
        
        
        # Update the screen
        pygame.display.update()
        
        # .2177
        sleep(.095)
        # Set the frame rate
        clock.tick(60)


# Need to define a function that varies the intensity of the color based on the read voltage
# Threshold is 12 mV minimum to 39 mV max

def volt_to_intensity(volt_tuple):
    """
    Takes volt_tuple (voltage for all junctions) and returns a tuple of color 
    intensity values related to each junction 
    """

    # Initialize return intensity list 
    intensity_list = []

    # This loop is taking volt_tuple (Kiethley data) and iterating through each element 
    # (v1, v2, v3, v4) to yield an appropriate intensity value
    for volt_tuple_element in volt_tuple:

        if volt_tuple_element > 12 and volt_tuple_element < 39:
            # 12mV is minimum reference voltage so this is the new "zero"
            volt_tuple_element -= 12
            # Lower intensity yields darker colors 
            volt_tuple_element = 255 - volt_tuple_element*9.4444 
            
        else:
            volt_tuple_element = 220

        intensity_list.append(volt_tuple_element)
    
    return intensity_list

# Generate a list populated with RGB tuples for each junction at each time instant 
# Given an intensity_list 
# [( (R, G, B), (R, G, B), (R, G, B), (R, G, B) ), ...]
def intensity_to_RGB(intensity_list):
    # initialize return
    color_profile = []
    for intensity in intensity_list:
        color = (255, intensity, intensity)
        color_profile.append(color)
    return color_profile 


main()

