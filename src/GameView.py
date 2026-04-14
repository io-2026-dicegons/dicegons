import pygame
import sys
import math 

hex_number_x = 30
hex_number_y = 20
hex_size = 16
proportions = math.sqrt(3) / 2
screenSize = (hex_number_x * 2 * proportions * hex_size + hex_size, 3/2 * hex_number_y * hex_size + 1/2*hex_size)
#screenSize = (1000, 1000)
gameWindow = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
pygame.display.set_caption("IOIOIOIO")


def draw_hex(surface, color, width, position ):
    
    a = hex_size # bok
    h = proportions * a
    b = a/2

    points = [  (position[0] , position[1]- a),
                (position[0] - h, position[1] - b),
                (position[0] - h, position[1] + b),
                (position[0], position[1] + a),
                (position[0] + h, position[1] + b),
                (position[0] + h, position[1] - b)]

    pygame.draw.polygon(surface, color, points, width)
    
def draw_map(surface):
    pass



start_draw_pos = (proportions*hex_size, hex_size)

background = pygame.Surface(screenSize, pygame.SRCALPHA) 
background.fill("grey") 

running = True
while running:
    
    gameWindow.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # for i in range(int(screenSize[0] / (proportions * hex_size))):
    #     for j in range(int(screenSize[1] / ( 2 * hex_size))):
    for i in range(hex_number_x):
        for j in range(hex_number_y):
            w = math.sqrt(3) * hex_size
            h = 2 * hex_size

            x_offset = w * i
            y_offset = 1.5 * hex_size * j

            if j % 2 == 1:
                x_offset += w / 2
            

            color = "white"
            player_one_hexes = [(0, 0), (0, 1), (1, 0), (1, 2), (2, 2), (1, 1), (2, 1)] 
            if(i, j) in player_one_hexes:
                color = "red"
            else:
                color = "white"
            draw_hex( gameWindow, color, 0, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset))

            
    i = 0
    j = 0
    for i in range(hex_number_x):
        for j in range(hex_number_y):
            w = math.sqrt(3) * hex_size
            h = 2 * hex_size

            x_offset = w * i
            y_offset = 1.5 * hex_size * j

            if j % 2 == 1:
                x_offset += w / 2
            
            draw_hex( gameWindow, "black", 1, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset))

    pygame.display.update()
    clock.tick(60)
    


pygame.quit()
