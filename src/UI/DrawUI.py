import pygame
import math

from DrawHexagonTile import DrawHexagonTile

class DrawUI:
    def __init__(self, screen, hex_size):
        self.screen = screen
        self.set_hex_size( hex_size )

    def set_hex_size(self, hex_size ):
        self.hex_size = hex_size
        self.vert_dist = 3/2 * hex_size
        self.horiz_dist = math.sqrt(3) * hex_size

    def get_grid_points(self, cols, rows, offset_x=0, offset_y=0):

        points = [];

        for col in range(cols):
            for row in range(rows):
                x = col * self.horiz_dist + offset_x
                y = row * self.vert_dist + offset_y

                if row % 2 == 1:
                    x += self.horiz_dist / 2

                points.append((x,y));

        return points
