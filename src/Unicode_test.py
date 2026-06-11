import pygame
import pygame.freetype

pygame.init()

screen = pygame.display.set_mode((800, 600))
font = pygame.freetype.Font(r"fonts/Noto_Emoji/NotoEmoji-VariableFont_wght.ttf", 32)

str = "⚔🐴  ⛪🏰🌾"

font.render_to(screen, (50, 50), str, (255, 255, 255))

pygame.display.flip()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            raise SystemExit