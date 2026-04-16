import pygame
import sys
import math
import json 


scale = 2
hex_unscaled_number_x = 30
hex_unscaled_number_y = 20
hex_unscaled_size = 16
proportions = math.sqrt(3) / 2

hex_number_x = hex_unscaled_number_x 
hex_number_y = hex_unscaled_number_y 
hex_size = hex_unscaled_size * scale

viewSize = (hex_unscaled_number_x * 2 * proportions * hex_unscaled_size + hex_unscaled_size, 3/2 * hex_unscaled_number_y * hex_unscaled_size + 1/2*hex_unscaled_size)
screenSize = (hex_number_x * 2 * proportions * hex_size + hex_size, 3/2 * hex_number_y * hex_size + 1/2*hex_size)
#screenSize = (1000, 1000)
gameWindow = pygame.display.set_mode(viewSize)
viewSurface = pygame.Surface(screenSize)

clock = pygame.time.Clock()
pygame.display.set_caption("IOIOIOIO")

finView = pygame.transform.smoothscale(gameWindow, viewSize)

with open("scenario_one.json") as f:
    data = json.load(f)

players = data["players"]


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
    


def draw_full_map(surface, color, width):
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
            
            draw_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset))

def draw_map(surface, hex_list, color, width):
    i,j = (0, 0)
    for i,j in hex_list:
        w = math.sqrt(3) * hex_size
        h = 2 * hex_size

        x_offset = w * i
        y_offset = 1.5 * hex_size * j

        if j % 2 == 1:
            x_offset += w / 2
        
        draw_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset))

start_draw_pos = (proportions*hex_size, hex_size)

background = pygame.Surface(screenSize, pygame.SRCALPHA) 
background.fill("grey") 

running = True
while running:
    
    viewSurface.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    draw_full_map(viewSurface, "blue", 0)
    player_one_hexes = players[0]["hexList"]
    draw_map(viewSurface, player_one_hexes, "white", 0)

    
    draw_full_map(  viewSurface, "Black", 1)


    scaled = pygame.transform.smoothscale(viewSurface, viewSize)
    gameWindow.blit(scaled, (0, 0))
    pygame.display.update()
    clock.tick(60)
    


pygame.quit()
