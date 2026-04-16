import pygame

from DrawHexagonTile import DrawHexagonTile
from DrawUI import DrawUI

pygame.init()

WINDOW_SIZE = (800, 600)
SCREEN_SIZE = (1600, 1200)

screen = pygame.display.set_mode(WINDOW_SIZE)
view_surface = pygame.Surface(SCREEN_SIZE)
clock = pygame.time.Clock()

hex_size = 50;
draw_ui = DrawUI( view_surface, hex_size )
points = draw_ui.get_grid_points(cols=2, rows=2, offset_x=100, offset_y=100)

print( points )

running = True
while running:
    view_surface.fill((255, 255, 255))

    #draw_ui.draw_grid(cols=5, rows=5, offset_x=100, offset_y=100)

    draw_hex = DrawHexagonTile( view_surface, hex_size )

    draw_hex.draw_hex(points[0][0],points[0][1], color=(144, 238, 144), width=0)
    draw_hex.draw_hex(points[1][0],points[1][1], color=(144, 238, 144), width=0)
    draw_hex.draw_hex(points[2][0],points[2][1], color=(128, 128, 128), width=0)
    draw_hex.draw_hex(points[3][0],points[3][1], color=(128, 128, 128), width=0)

    #draw_hex.draw_hex_border(points[0][0],points[0][1],1,(255, 0, 0),4)
    draw_hex.draw_hex_border(points[0][0],points[0][1],2,(255, 0, 0),4)
    draw_hex.draw_hex_border(points[0][0],points[0][1],3,(255, 0, 0),4)
    draw_hex.draw_hex_border(points[0][0],points[0][1],4,(255, 0, 0),4)
    draw_hex.draw_hex_border(points[0][0],points[0][1],5,(255, 0, 0),4)
    draw_hex.draw_hex_border(points[0][0],points[0][1],6,(255, 0, 0),4)
    
    #draw_hex.draw_hex_line(points[0][0],points[0][1], 1, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[0][0],points[0][1], 2, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[0][0],points[0][1], 3, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[0][0],points[0][1], 4, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[0][0],points[0][1], 5, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[0][0],points[0][1], 6, color=(0, 0, 0), width=2)

    draw_hex.draw_hex_border(points[1][0],points[1][1],1,(255, 0, 0),4)
    draw_hex.draw_hex_border(points[1][0],points[1][1],2,(255, 0, 0),4)
    draw_hex.draw_hex_border(points[1][0],points[1][1],3,(255, 0, 0),4)
    #draw_hex.draw_hex_border(points[1][0],points[1][1],4,(255, 0, 0),4)
    draw_hex.draw_hex_border(points[1][0],points[1][1],5,(255, 0, 0),4)
    draw_hex.draw_hex_border(points[1][0],points[1][1],6,(255, 0, 0),4)
    
    draw_hex.draw_hex_line(points[1][0],points[1][1], 1, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[1][0],points[1][1], 2, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[1][0],points[1][1], 3, color=(0, 0, 0), width=2)
    #draw_hex.draw_hex_line(points[1][0],points[1][1], 4, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[1][0],points[1][1], 5, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[1][0],points[1][1], 6, color=(0, 0, 0), width=2)

    #draw_hex.draw_hex_border(points[2][0],points[2][1],1,(0, 255, 0),4)
    draw_hex.draw_hex_border(points[2][0],points[2][1],2,(0, 255, 0),4)
    draw_hex.draw_hex_border(points[2][0],points[2][1],3,(0, 255, 0),4)
    draw_hex.draw_hex_border(points[2][0],points[2][1],4,(0, 255, 0),4)
    draw_hex.draw_hex_border(points[2][0],points[2][1],5,(0, 255, 0),4)
    draw_hex.draw_hex_border(points[2][0],points[2][1],6,(0, 255, 0),4)
    
    #draw_hex.draw_hex_line(points[2][0],points[2][1], 1, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[2][0],points[2][1], 2, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[2][0],points[2][1], 3, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[2][0],points[2][1], 4, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[2][0],points[2][1], 5, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[2][0],points[2][1], 6, color=(0, 0, 0), width=2)

    draw_hex.draw_hex_border(points[3][0],points[3][1],1,(0, 255, 0),4)
    draw_hex.draw_hex_border(points[3][0],points[3][1],2,(0, 255, 0),4)
    draw_hex.draw_hex_border(points[3][0],points[3][1],3,(0, 255, 0),4)
    #draw_hex.draw_hex_border(points[3][0],points[3][1],4,(0, 255, 0),4)
    draw_hex.draw_hex_border(points[3][0],points[3][1],5,(0, 255, 0),4)
    draw_hex.draw_hex_border(points[3][0],points[3][1],6,(0, 255, 0),4)
    
    draw_hex.draw_hex_line(points[3][0],points[3][1], 1, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[3][0],points[3][1], 2, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[3][0],points[3][1], 3, color=(0, 0, 0), width=2)
    #draw_hex.draw_hex_line(points[3][0],points[3][1], 4, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[3][0],points[3][1], 5, color=(0, 0, 0), width=2)
    draw_hex.draw_hex_line(points[3][0],points[3][1], 6, color=(0, 0, 0), width=2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    scaled = pygame.transform.smoothscale(view_surface, SCREEN_SIZE)
    screen.blit(scaled, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()