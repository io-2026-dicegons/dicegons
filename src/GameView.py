import pygame
import sys
import math
import json 
#importy

#komentarze sa po to bo mam wrazenier ze nie ogarne kodu sam zaraz a co dopiero wy

# statystyki hexow
scale = 2
hexScale = 1
hex_unscaled_number_x = 30 * hexScale
hex_unscaled_number_y = 20 * hexScale
hex_unscaled_size = 16 / hexScale
proportions = math.sqrt(3) / 2

# tutaj jest system od skalowania mapy bo bez tego to strasznie spixelizowane bylo
hex_number_x = hex_unscaled_number_x 
hex_number_y = hex_unscaled_number_y 
hex_size = hex_unscaled_size * scale

viewSize = (hex_unscaled_number_x * 2 * proportions * hex_unscaled_size + hex_unscaled_size, 3/2 * hex_unscaled_number_y * hex_unscaled_size + 1/2*hex_unscaled_size)
screenSize = (hex_number_x * 2 * proportions * hex_size + hex_size, 3/2 * hex_number_y * hex_size + 1/2*hex_size)
#screenSize = (1000, 1000)


#pygamestuff
gameWindow = pygame.display.set_mode(viewSize)
viewSurface = pygame.Surface(screenSize)

clock = pygame.time.Clock()
pygame.display.set_caption("IOIOIOIO")

finView = pygame.transform.smoothscale(gameWindow, viewSize)

with open("scenario_one.json") as f:
    data = json.load(f)

provinces = data["provinces"]


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
    

def draw_border_hex(surface, color, width, position, edge):  
    #     0
    #  1 / \ 5
    #   |   | 
    #  2 \ / 4
    #     3
    a = hex_size # bok 
    h = proportions * a 
    b = a/2 


    points = [
        (position[0], position[1]-a),      # 0
        (position[0]-h, position[1]-b),    # 1
        (position[0]-h, position[1]+b),    # 2
        (position[0], position[1]+a),      # 3
        (position[0]+h, position[1]+b),    # 4
        (position[0]+h, position[1]-b)     # 5
    ]

    p1 = points[edge]
    p2 = points[(edge + 1) % 6]

    pygame.draw.line(surface, color, p1, p2, width)

def draw_border_map(surface, hex_list, color, width): #granice miedzy prowincjami
    i = 0
    j = 0
    for i, j in hex_list:
        w = math.sqrt(3) * hex_size
        h = 2 * hex_size

        x_offset = w * i
        y_offset = 1.5 * hex_size * j

        if j % 2 == 1:
            x_offset += w / 2

        if j % 2 == 0: # if my beloved
            if[i - 1, j - 1] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 0)
            if[i - 1, j] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 1)
            if[i - 1, j + 1] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 2)
            if[i, j + 1] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 3)
            if[i + 1, j] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 4)
            if[i, j - 1] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 5)
        else:
            if[i, j - 1] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 0)
            if[i - 1, j] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 1)
            if[i, j + 1] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 2)
            if[i + 1, j + 1] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 3)
            if[i + 1, j] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 4)
            if[i + 1, j - 1] not in hex_list:
                draw_border_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset), 5)

def draw_full_map(surface, color, width): # cala mapa 
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


def draw_map(surface, hex_list, color, width):  #mapa z listy
    i,j = (0, 0)
    for i,j in hex_list: 
        w = math.sqrt(3) * hex_size
        h = 2 * hex_size

        x_offset = w * i
        y_offset = 1.5 * hex_size * j

        if j % 2 == 1:
            x_offset += w / 2
        
        draw_hex( surface, color, width, (start_draw_pos[0] + x_offset, start_draw_pos[1] + y_offset))

#pygame stuff v2
start_draw_pos = (proportions*hex_size, hex_size)

background = pygame.Surface(screenSize, pygame.SRCALPHA) 
background.fill("grey") 

running = True
while running:
    

    viewSurface.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # rysuje cala mape poza jako wode 
    draw_full_map(viewSurface, "blue", 0)

    #a tutaj bierze z scenariusza prowincje i je maluje na dany kolor (wczytywanie typow terenu zrobie potem)
    province_zero_hexes = provinces[0]["hexList"]
    draw_map(viewSurface, province_zero_hexes, "white", 0)
    province_one_hexes = provinces[1]["hexList"]
    draw_map(viewSurface, province_one_hexes, "red", 0)
    province_two_hexes = provinces[2]["hexList"]
    draw_map(viewSurface, province_two_hexes, "green", 0)
    

    # draw_full_map(  viewSurface, "Black", 1)
    #granice prowincji 
    draw_border_map(viewSurface, province_zero_hexes, "black", 2 * scale)
    draw_border_map(viewSurface, province_one_hexes, "black", 2 * scale)
    draw_border_map(viewSurface, province_two_hexes, "black", 2 * scale)

    scaled = pygame.transform.smoothscale(viewSurface, viewSize)
    gameWindow.blit(scaled, (0, 0))
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()

