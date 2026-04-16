import pygame
import math

class DrawHexagonTile:
    def __init__(self,screen,hex_size=20):
        self.screen = screen
        self.hex_size = hex_size

    def hex_corners(self, x, y):
        corners = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            corner_x = x + self.hex_size * math.cos(angle_rad)
            corner_y = y + self.hex_size * math.sin(angle_rad)
            corners.append((corner_x, corner_y))
        return corners
    
    def draw_hex(self, x, y, color, width):
        points = self.hex_corners(x, y)

        pygame.draw.polygon(self.screen, color, points, width)
    
    def draw_hex_line(self, x, y, index, color, width):
        corners = self.hex_corners(x, y)

        p0 = corners[(index + 0) % 6]
        p1 = corners[(index + 1) % 6]

        points = [ p0, p1 ]

        pygame.draw.polygon(self.screen, color, points, width)


    def draw_hex_border(self, x, y, index, color, width):
        corners = self.hex_corners(x, y)

        p0 = corners[(index - 1) % 6]
        p1 = corners[(index + 0) % 6]
        p2 = corners[(index + 1) % 6]
        p3 = corners[(index + 2) % 6]

        if( index == 3 ):
            mid1 = (math.floor(width / 16 * (p0[0] - p1[0]) + p1[0]), math.floor(width / 16 * (p0[1] - p1[1]) + p1[1]))
            mid2 = (math.floor(width / 16 * (p3[0] - p2[0]) + p2[0]), math.floor(width / 16 * (p3[1] - p2[1]) + p2[1]))
        elif( index == 4 ):
            mid1 = (math.floor(width / 16 * (p0[0] - p1[0]) + p1[0]), math.floor(width / 16 * (p0[1] - p1[1]) + p1[1]))
            mid2 = (round(width / 16 * (p3[0] - p2[0]) + p2[0]), round(width / 16 * (p3[1] - p2[1]) + p2[1]))
        else:
            mid1 = (round(width / 16 * (p0[0] - p1[0]) + p1[0]), round(width / 16 * (p0[1] - p1[1]) + p1[1]))
            mid2 = (round(width / 16 * (p3[0] - p2[0]) + p2[0]), round(width / 16 * (p3[1] - p2[1]) + p2[1]))

        points = [mid1, p1, p2, mid2]

        pygame.draw.polygon(self.screen, color, points)
