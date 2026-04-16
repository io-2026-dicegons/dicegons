import pygame

from DrawHexagonTile import DrawHexagonTile

pygame.init()

WINDOW_SIZE = (800, 600)
SCREEN_SIZE = (800, 600)

screen = pygame.display.set_mode(WINDOW_SIZE)
view_surface = pygame.Surface(SCREEN_SIZE)
clock = pygame.time.Clock()

hex_size = 24
draw_hex = DrawHexagonTile( view_surface, hex_size )

running = True
while running:
    view_surface.fill((255, 255, 255))

    x = 300
    y = 300

    for i in range(0,6):
        draw_hex.draw_hex_border(x,y,i,(255, 0, 0),3)

    for i in range(0,6):
        draw_hex.draw_hex_line( x, y, i, (0, 0, 0), 2 )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    scaled = pygame.transform.smoothscale(view_surface, SCREEN_SIZE)
    screen.blit(scaled, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()