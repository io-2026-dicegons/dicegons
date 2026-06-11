import pygame
import pygame.freetype
import random
import sys
import math
import json 
#importy
from game.resourceManager import ResourceManager
from game.game_controller import GameController
from game.turn import *
from game.scenario_creator import ScenarioCreator


#komentarze sa po to bo mam wrazenier ze nie ogarne kodu sam zaraz a co dopiero wy
class GameWindowClass:
    def __init__(self, window, startX, startY, hex_scale, hex_size, origin_X_hex_number, origin_Y_hex_number):
        self.gameWindow = window
        self.startX =  startX
        self.startY = startY
        self.hexScale = hex_scale
        self.hex_size = hex_size
        self.origin_X_hex_number = origin_X_hex_number
        self.origin_Y_hex_number = origin_Y_hex_number

        self.province_clicked_1 = None
        self.selected_unit_type = None
        self.win = False

        # wczytywanie bazy danych
        self.resource_manager = ResourceManager()
        self.resource_manager.load_definitions()
        self.game_controler = GameController(self.resource_manager)

        self.scenario_loader = ScenarioCreator()
        
        scenario_count = 2
        n = random.randint(1, scenario_count)

        if n == 1:
            self.game_controler = self.scenario_loader.scenario_1(self.game_controler)
        if n == 2:
            self.game_controler = self.scenario_loader.scenario_2(self.game_controler)

        self.error = False
            
        # statystyki hexow
        self.scale = 1
        hexScale = 1 # <--------------------------------------------------------------
        hex_unscaled_number_x = int(self.origin_X_hex_number * hexScale) #30
        hex_unscaled_number_y = int(self.origin_Y_hex_number * hexScale) #20
        hex_unscaled_size = hex_size / hexScale
        self.proportions = math.sqrt(3) / 2

        self.waterColor = GameController.get_terrain_color(self, 0)

        self.glow = None
        self.glow_color = [150, 150, 150, 3]
        
        self.font = "Times new roman"

        self.clicked = None

        # tutaj jest system od skalowania mapy bo bez tego to strasznie spixelizowane bylo
        self.hex_number_x = hex_unscaled_number_x 
        self.hex_number_y = hex_unscaled_number_y 
        self.hex_size = hex_unscaled_size * self.scale # <------------------------------------------------------------------

        self.viewSize = (hex_unscaled_number_x * 2 * self.proportions * hex_unscaled_size + hex_unscaled_size, 3/2 * hex_unscaled_number_y * hex_unscaled_size + 1/2*hex_unscaled_size)
        self.screenSize = (self.hex_number_x * 2 * self.proportions * self.hex_size + self.hex_size, 3/2 * self.hex_number_y * self.hex_size + 1/2*self.hex_size)
        # self.screenSize = (1000, 1000)

        self.start_draw_pos = (self.startX + self.proportions * self.hex_size , self.startY + self.hex_size)

        #pygamestuff

        self.GUIsize = (300, 100)
        self.GUI_color = [72, 74, 79]
        self.GUI_gradient = [109, 110, 112]
    
        self.gameSize = (self.viewSize[0] + self.GUIsize[0], self.viewSize[1] + self.GUIsize[1])

        self.gameWindow = pygame.display.set_mode((self.viewSize[0] + self.GUIsize[0], self.viewSize[1] + self.GUIsize[1]))
        self.viewSurface = pygame.Surface(self.viewSize, pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("IOIOIOIO")
        
        self.all_provinces = []

        # provinces = self.game_controler.map.get_province_list()
        # # for i in provinces:
        # #     self.all_provinces += self.game_controler.get_province_hex_list(i)
        # #     # print(self.game_controler.get_province_hex_list(i))

        # print(self.all_provinces)

        self.all_provinces = self.game_controler.get_player_provinces(1)
        self.all_provinces += self.game_controler.get_player_provinces(2)
    
    def draw_hex(self, surface, color, width, position ): 
        
        a = self.hex_size # bok
        h = self.proportions * a
        b = a/2

        points = [  (position[0] , position[1]- a),
                    (position[0] - h, position[1] - b),
                    (position[0] - h, position[1] + b),
                    (position[0], position[1] + a),
                    (position[0] + h, position[1] + b),
                    (position[0] + h, position[1] - b)]

        pygame.draw.polygon(surface, color, points, width)
        
    def draw_border_hex(self, surface, color, width, position, edge):  # borders for hexes
        #     0
        #  1 / \ 5
        #   |   | 
        #  2 \ / 4
        #     3
        a = self.hex_size # bok 
        h = self.proportions * a 
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

    def draw_border_map(self, surface, hex_list, color, width): # granice miedzy prowincjami
        i = 0
        j = 0
        for i, j in hex_list:
            w = math.sqrt(3) * self.hex_size
            h = 2 * self.hex_size

            x_offset = w * i
            y_offset = 1.5 * self.hex_size * j

            if j % 2 == 1:
                x_offset += w / 2

            position = (self.start_draw_pos[0] + x_offset, self.start_draw_pos[1] + y_offset)
            if j % 2 == 0: # if my beloved
                if[i - 1, j - 1] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 0)
                if[i - 1, j] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 1)
                if[i - 1, j + 1] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 2)
                if[i, j + 1] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 3)
                if[i + 1, j] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 4)
                if[i, j - 1] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 5)
            else:
                if[i, j - 1] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 0)
                if[i - 1, j] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 1)
                if[i, j + 1] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 2)
                if[i + 1, j + 1] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 3)
                if[i + 1, j] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 4)
                if[i + 1, j - 1] not in hex_list:
                    self.draw_border_hex( surface, color, width, position, 5)

    def draw_province_border_hex(self, surface, color, width, position, edge, percent):
        a = self.hex_size
        h = self.proportions * a
        b = a / 2

        points = [
            (position[0], position[1]-a),      # 0
            (position[0]-h, position[1]-b),    # 1
            (position[0]-h, position[1]+b),    # 2
            (position[0], position[1]+a),      # 3
            (position[0]+h, position[1]+b),    # 4
            (position[0]+h, position[1]-b)     # 5
        ]

        def lerp(p1, p2, t):
            return (
                p1[0] + (p2[0] - p1[0]) * t,
                p1[1] + (p2[1] - p1[1]) * t
            )

        i0, i1 = edge
        prev_i = (i0 - 1) % 6
        next_i = (i1 + 1) % 6

        subpoints = [
            points[i0],
            points[i1],
            lerp(points[i1], points[next_i], percent),
            lerp(points[i0], points[prev_i], percent),
        ]

        pygame.draw.polygon(surface, color, subpoints, width)


    def draw_player_border(self, surface, player_hex_list, province_number, color, width, size):
        hex_list = player_hex_list[province_number]
        # print(player_hex_list, province_number)

        # self.game_controler.get_player_hexes()

        for [i, j] in hex_list:
            w = math.sqrt(3) * self.hex_size
            h = 2 * self.hex_size

            x_offset = w * i
            y_offset = 1.5 * self.hex_size * j

            if j % 2 == 1:
                x_offset += w / 2
            
            position = (self.start_draw_pos[0] + x_offset, self.start_draw_pos[1] + y_offset)
            player_hex_set = set(tuple(h) for province in player_hex_list for h in province)

            if j % 2 == 0: # if my beloved
                if(i - 1, j - 1) not in player_hex_set:
                    # self.draw_border_hex( surface, color, width, position, 0)
                    self.draw_province_border_hex(surface, color, width, position, [0, 1], size)
                if(i - 1, j) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [1, 2], size)
                if(i - 1, j + 1) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [2, 3], size)
                if(i, j + 1) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [3, 4], size)
                if(i + 1, j) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [4, 5], size)
                if(i, j - 1) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [5, 0], size)
            else:
                if(i, j - 1) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [0, 1], size)
                if(i - 1, j) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [1, 2], size)
                if(i, j + 1) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [2, 3], size)
                if(i + 1, j + 1) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [3, 4], size)
                if(i + 1, j) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [4, 5], size)
                if(i + 1, j - 1) not in player_hex_set:
                    self.draw_province_border_hex(surface, color, width, position, [5, 0], size)

    def draw_building(self, surface, buildingID, hex_list):
        
        position = hex_list[2]
        symbol = GameController.get_building_symbol(self, buildingID)

        font = pygame.freetype.Font(r"fonts/Noto_Emoji/NotoEmoji-VariableFont_wght.ttf", 24 )

        w = math.sqrt(3) * self.hex_size
        h = 2 * self.hex_size

        x_offset = w * position[0]
        y_offset = 1.5 * self.hex_size * position[1]

        if position[1] % 2 == 1:
            x_offset += w / 2
        
        pos_X = self.start_draw_pos[0] + x_offset
        pos_Y = self.start_draw_pos[1] + y_offset

        font.render_to(surface, (pos_X  - self.hex_size * 0.5, pos_Y - self.hex_size * 0.5 ), symbol, (0, 0, 0))

    def draw_squad(self, surface, symbol, font_index, count, hex_list, squad_number):
        w = math.sqrt(3) * self.hex_size
        h = 2 * self.hex_size

        count = str(count)

        position = hex_list[squad_number - 1]
        font_size = int(3/4 * self.hex_size)

        x_offset = w * position[0]
        y_offset = 1.5 * self.hex_size * position[1]

        if position[1] % 2 == 1:
            x_offset += w / 2
        
        pos_X = self.start_draw_pos[0] + x_offset
        pos_Y = self.start_draw_pos[1] + y_offset

        text_font = pygame.font.SysFont(self.font, font_size, True)

        font = pygame.freetype.Font(r"fonts/Noto_Emoji/NotoEmoji-VariableFont_wght.ttf", 16 )

        text_text = text_font.render(count, True, "Black", None)
        text_text_rect = text_text.get_rect()

        font.render_to(surface, (pos_X  - self.hex_size * 0.4, pos_Y - self.hex_size * 0.2 - self.hex_size/3), symbol, (0, 0, 0))

        text_text_rect.center = (pos_X  - self.hex_size * 0.05, pos_Y + self.hex_size * 0.05 + self.hex_size/3)
        surface.blit(text_text, text_text_rect)

    def draw_army(self, surface, symbol_one, font_index_one, count_one, symbol_two, font_index_two, count_two, hex_list):        
        self.draw_squad(surface, symbol_one, font_index_one, count_one, hex_list, 1)
        self.draw_squad(surface, symbol_two, font_index_two, count_two, hex_list, 2)

    def draw_full_map(self, surface, color, width): # cala mapa 
        i = 0
        j = 0
        for i in range(self.hex_number_x):
            for j in range(self.hex_number_y):
                w = math.sqrt(3) * self.hex_size
                h = 2 * self.hex_size

                x_offset = w * i
                y_offset = 1.5 * self.hex_size * j

                if j % 2 == 1:
                    x_offset += w / 2
                
                self.draw_hex( surface, color, width, (self.start_draw_pos[0] + x_offset, self.start_draw_pos[1] + y_offset))


    def draw_map(self, surface, hex_list, color, width):  #mapa z listy
        i,j = (0, 0)

        for i,j in hex_list: 
            w = math.sqrt(3) * self.hex_size
            h = 2 * self.hex_size

            x_offset = w * i
            y_offset = 1.5 * self.hex_size * j

            if j % 2 == 1:
                x_offset += w / 2
            
            self.draw_hex( surface, color, width, (self.start_draw_pos[0] + x_offset, self.start_draw_pos[1] + y_offset))
            # self.draw_province_border_hex(surface, "red", width, (self.start_draw_pos[0] + x_offset, self.start_draw_pos[1] + y_offset), [1, 2], 1/3)

    def draw_glow(self, surface):
        # print(self.all_provinces)
        # print(self.glow)
        for i in self.all_provinces:
            # print(i)
            if(self.glow == i):
                province_hexes = self.game_controler.get_province_hex_list(i)
                self.draw_border_map(surface, province_hexes, "yellow", 4)



    def draw_province(self, surface, province_id):
        # province_hexes = province["hexList"]
        province_hexes = self.game_controler.get_province_hex_list(province_id)
        
        # print(province_hexes)

        # self.error = True
        # terrain_id = province["terrain_ID"]
        terrain_id = self.game_controler.get_province_terrain(province_id)

        color = self.resource_manager.get_terrain_by_id(terrain_id).color

        self.draw_map(surface, province_hexes, color, 0)
        # if(self.glow == province_id):
        #     # print(color)
        #     self.draw_map(surface, province_hexes, self.glow_color, 0)
            
        self.draw_border_map(surface, province_hexes, "black", int(self.hex_size/8))

        


    def draw_player_stuff(self, surface, player_provinces, color):
        for i in range(len(player_provinces)):
            self.draw_player_border(surface, player_provinces, i, color, 0, 1/4)

    def pixel_to_hex(self, mouse_pos):
        mx, my = mouse_pos

        mx -= self.start_draw_pos[0]
        my -= self.start_draw_pos[1]

        w = math.sqrt(3) * self.hex_size
        row_height = 1.5 * self.hex_size 

        j = int(round(my / row_height))

        if j % 2 == 1:
            mx -= w / 2

        i = int(round(mx / w))

        return [i, j]



    def draw_game(self, surface):
        pygame.draw.polygon(self.viewSurface, self.waterColor, [[self.startX, self.startY], [self.startX, self.viewSize[1]], [self.viewSize[0], self.viewSize[1]], [self.viewSize[0], self.startY]], 0)
        
        self.draw_full_map(surface, self.waterColor, 0)

        all_provinces = self.game_controler.get_player_provinces(1)
        all_provinces += self.game_controler.get_player_provinces(2)

        for i in all_provinces:
            self.draw_province(surface, i)

            squad_one_id = self.game_controler.get_army_squad_unit_type(i, 1)
            squad_two_id = self.game_controler.get_army_squad_unit_type(i, 2)

            # print(squad_one_id, squad_two_id)
            squad_one_symbol = self.game_controler.get_unit_symbol(squad_one_id)
            squad_two_symbol = self.game_controler.get_unit_symbol(squad_two_id)

            squad_one_code = self.game_controler.get_unit_symbol_code(squad_one_id)
            squad_two_code = self.game_controler.get_unit_symbol_code(squad_two_id)    
            
            squad_one_stack = self.game_controler.get_army_squad_stack(i, 1)
            squad_two_stack = self.game_controler.get_army_squad_stack(i, 2)

            
            self.draw_army(surface, squad_one_symbol, squad_one_code, squad_one_stack, squad_two_symbol, squad_two_code, squad_two_stack, self.game_controler.get_province_hex_list(i))

            self.draw_building(surface, self.game_controler.get_province_building(i), self.game_controler.get_province_hex_list(i))


        for i in range (2):
            playerHexes = [self.game_controler.get_player_hexes(i+1)]
            if(i == 1):
                color = (255, 0, 0)
            else:
                color = (127, 0, 255)
            self.draw_player_stuff(surface, playerHexes, color)


        # self.draw_building(self.viewSurface, "l", 0 , test) #<------------------------------------------
        # print(self.game_controler.get_province_building( 0 ))
        # self.draw_army(surface, "U", 0, 13 , "P", 1, 4, test)

    def draw_turn_block(self, surface):
        color = "gray"
        gradient_color = self.GUI_gradient

        font_size = 16
        
        turn_type = self.game_controler.turn.get_phase()

        player_id = self.game_controler.get_current_player_id()

        size = [self.GUIsize[0], 75]
        points = [[self.startX + self.viewSize[0], self.startY], [self.startX + self.viewSize[0] + size[0], self.startY], [self.startX + self.viewSize[0] + size[0], self.startY + size[1]], [self.startX + self.viewSize[0], self.startY + size[1]]]

        turn_timer_size = [size[0]/3, size[1]]
        turn_timer_points = [[points[1][0] - turn_timer_size[0], points[1][1]], points[1], points[2], [points[1][0] - turn_timer_size[0], points[3][1]]]

        pygame.draw.polygon(surface, gradient_color, points, 0)
        
        # pygame.draw.polygon(surface, "red", turn_timer_points, 0)
        points_place = [turn_timer_points[0], turn_timer_points[1], [turn_timer_points[1][0], turn_timer_points[1][1] + 1/3 * turn_timer_size[1]], [turn_timer_points[0][0], turn_timer_points[0][1] + 1/3 * turn_timer_size[1]]]
        points_gold = [[turn_timer_points[0][0], turn_timer_points[0][1] + turn_timer_size[1] * 1/3], [turn_timer_points[1][0], turn_timer_points[1][1] + turn_timer_size[1] * 1/3], [turn_timer_points[1][0], turn_timer_points[1][1] + 2/3 * turn_timer_size[1]], [turn_timer_points[0][0], turn_timer_points[0][1] + 2/3 * turn_timer_size[1]] ]
        points_attack = [[turn_timer_points[0][0], turn_timer_points[0][1]  + turn_timer_size[1] * 2/3], [turn_timer_points[1][0], turn_timer_points[1][1] + turn_timer_size[1] * 2/3], [turn_timer_points[1][0], turn_timer_points[1][1] +  turn_timer_size[1]], [turn_timer_points[0][0], turn_timer_points[0][1] + turn_timer_size[1]] ]
        

        pygame.draw.polygon(surface, color, points_place)
        pygame.draw.polygon(surface, gradient_color, points_gold)
        pygame.draw.polygon(surface, color, points_attack)
        
        text_font = pygame.font.SysFont(self.font, font_size + 28, True ) 

        #coin = 0
        coin = self.game_controler.get_player_gold( player_id )
        nick = self.game_controler.get_player_nick( player_id )
        text = str(nick)

        text_player = text_font.render(text, True, "Black")
        text_player_rect = text_player.get_rect(midleft = (points[0][0], (points[0][1] + points[3][1])/2))
        surface.blit(text_player, text_player_rect)

        text_font = pygame.font.SysFont(self.font, font_size, True )

        text_place = text_font.render("Placing", True, "Black")
        text_place_rect = text_place.get_rect(midleft = (points_place[0][0], (points_place[0][1] + points_place[3][1]) / 2))
        surface.blit(text_place, text_place_rect)

        text_gold = text_font.render("Gold: " + str(coin), True, "Black")
        text_gold_rect = text_gold.get_rect(midleft = (points_gold[0][0], (points_gold[0][1] + points_gold[3][1]) / 2))
        surface.blit(text_gold, text_gold_rect)

        text_attack = text_font.render("Attacking", True, "Black")
        text_attack_rect = text_attack.get_rect(midleft = (points_attack[0][0], (points_attack[0][1] + points_attack[3][1]) / 2))
        surface.blit(text_attack, text_attack_rect)

        text_font = pygame.font.SysFont("Wingdings3", font_size + 10, True )

        arrow_points = [0, 0]
        if(turn_type == 0):
            arrow_points = (points_place[0][0], (points_place[0][1] + points_place[3][1]) / 2)
        elif(turn_type == 1):
            arrow_points = (points_attack[0][0], (points_attack[0][1] + points_attack[3][1]) / 2)
        else: 
            arrow_points = (points_gold[0][0], (points_gold[0][1] + points_gold[3][1]) / 2)

        text_attack = text_font.render("a", True, "white")
        text_attack_rect = text_attack.get_rect(midright = arrow_points)
        surface.blit(text_attack, text_attack_rect)

        
    def draw_null_block(self, surface):
        font_size = 28

        scale = 2/3
        size = [self.GUIsize[0], 50]
        size = [size[0] * scale, size[1] * scale]
        
        gradient_color = self.GUI_gradient

        x = self.startX + self.viewSize[0] + 1/2 * self.GUIsize[0]
        y = self.startY + self.viewSize[1] + self.GUIsize[1] - size[1] - 50

        rect = pygame.Rect(x, y, size[0], size[1])
        rect.center = (x, y)


        pygame.draw.rect(surface, gradient_color, rect)

        text_font = pygame.font.SysFont(self.font, font_size, True )

        text = text_font.render("Cancel", True, "Black")

        text_rect = text.get_rect(center = (x, y))

        surface.blit(text, text_rect)

        self.null_block_rect = rect
    
    def draw_table(self, surface, center):
        scale = 0.8

        font_size = 26

        font_color = "gray"

        name_font_size = 32
        size = [self.GUIsize[0], 50]
        size = [size[0] * scale, size[1] * scale]

        line_size = 150

        name_position = [center[0], center[1] - line_size - 75]


        
        if(self.clicked == None):
            return 
        

        showed_object = self.clicked

        if( showed_object["type"] == 'battle' ):
            attack = showed_object["attack"]
            text_font = pygame.font.SysFont(self.font, name_font_size, True )

            text_player = text_font.render("Wynik", True, "Black")
            text_player_rect = text_player.get_rect(center = name_position )
            surface.blit(text_player, text_player_rect)

            symbol_size = font_size + 16
            
            text_font = pygame.font.SysFont(self.font, font_size, True )
            positions = (self.viewSize[0] + 15, center[1] - 0.75 * line_size)

            shift = 0.3

            D_Mod = text_font.render("Atakujący: ", True, font_color)
            D_Mod_rect = text_player.get_rect(midleft = positions )
            surface.blit(D_Mod, D_Mod_rect)

            D_Mod_Value = str( attack[0] )
            D_Mod_Value_text = text_font.render(D_Mod_Value, True, font_color)
            D_Mod_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(D_Mod_Value_text, D_Mod_Value_rect)

            positions = (positions[0], positions[1] + shift * line_size)

            Income = text_font.render("Obrońca:", True, font_color)
            Income_rect = text_player.get_rect(midleft = positions )
            surface.blit(Income, Income_rect)

            Income_Value = str( attack[1] )
            Income_Value_text = text_font.render(Income_Value, True, font_color)
            Income_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(Income_Value_text, Income_Value_rect)

        if( showed_object["type"] == 'unit' ):
            unit_id = showed_object["id"]

            # print(unit_id)
            offset = 25

            # print(self.clicked["id"])

            symbol = self.game_controler.get_unit_symbol(unit_id)

            font_index = self.game_controler.get_unit_symbol_code( unit_id )
            # font_index = 0

            font_view_size = font_size + 16

            name = self.game_controler.get_unit_name( unit_id )

            text_font = pygame.font.SysFont(self.font, name_font_size, True )

            text_player = text_font.render(name, True, "Black")
            text_player_rect = text_player.get_rect(center = name_position )
            surface.blit(text_player, text_player_rect)

            #pygame.draw.line(surface, self.GUI_gradient, [center[0] + offset, center[1] - line_size], [center[0] + offset, center[1] + line_size], 5)

            font = pygame.freetype.Font(r"fonts/Noto_Emoji/NotoEmoji-VariableFont_wght.ttf", 32 )
            font.render_to(surface, (name_position[0], name_position[1] + 1.5 * font_size ), symbol, (0, 0, 0))

            text_font = pygame.font.SysFont(self.font, font_size, True )

            positions = (self.viewSize[0] + 15, center[1] - 0.75 * line_size)

            shift = 0.5
            A_Dice = text_font.render("Attack Dice", True, font_color)
            A_Dice_rect = text_player.get_rect(midleft = positions )
            surface.blit(A_Dice, A_Dice_rect)

            A_Dice_Value = self.game_controler.get_unit_attack_dice( unit_id )
            A_Dice_Value = str(A_Dice_Value)
            A_Dice_Value_text = text_font.render(A_Dice_Value, True, font_color)
            A_Dice_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(A_Dice_Value_text, A_Dice_Value_rect)

            positions = (positions[0], positions[1] + shift * line_size)

            D_Dice = text_font.render("Defence Dice", True, font_color)
            D_Dice_rect = text_player.get_rect(midleft = positions )
            surface.blit(D_Dice, D_Dice_rect)

            D_Dice_Value = self.game_controler.get_unit_defence_dice( unit_id )
            D_Dice_Value = str(D_Dice_Value)
            D_Dice_Value_text = text_font.render(D_Dice_Value, True, font_color)
            D_Dice_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(D_Dice_Value_text, D_Dice_Value_rect)

            positions = (positions[0], positions[1] + shift * line_size)

            M_Stack = text_font.render("Max Stack", True, font_color)
            M_Stack_rect = text_player.get_rect(midleft = positions )
            surface.blit(M_Stack, M_Stack_rect)

            M_Stack_Value = self.game_controler.get_unit_max_stack( unit_id )
            M_Stack_Value = str(M_Stack_Value)
            M_Stack_Value_text = text_font.render(M_Stack_Value, True, font_color)
            M_Stack_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(M_Stack_Value_text, M_Stack_Value_rect)

            positions = (positions[0], positions[1] + shift * line_size)

            U_Price = text_font.render("Unit Price", True, font_color)
            U_Price_rect = text_player.get_rect(midleft = positions )
            surface.blit(U_Price, U_Price_rect)

            U_Price_Value = self.game_controler.get_unit_price( unit_id )
            U_Price_Value = str(U_Price_Value)
            U_Price_Value_text = text_font.render(U_Price_Value, True, font_color)
            U_Price_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(U_Price_Value_text, U_Price_Value_rect)




        if( showed_object["type"] == 'province'):
            province_id = showed_object["id"]

            terrain_id = self.game_controler.get_province_terrain(province_id)
            building_id = self.game_controler.get_province_building(province_id)

            name = self.game_controler.get_terrain_name(terrain_id)

            text_font = pygame.font.SysFont(self.font, name_font_size, True )

            text_player = text_font.render(name, True, "Black")
            text_player_rect = text_player.get_rect(center = name_position )
            surface.blit(text_player, text_player_rect)


            # print(color)
            color = self.resource_manager.get_terrain_by_id( terrain_id ).color
            # print(color)
   

            # view_symbol_color = self.resource_manager.get_terrain_by_id(terrain_id).color
            view_symbol_color = color
            view_symbol_border = "black"

            symbol_size = font_size + 16
            pygame.draw.circle(surface, view_symbol_color, (name_position[0], name_position[1] + 1.5 * font_size ), symbol_size/2, 0)
            pygame.draw.circle(surface, view_symbol_border, (name_position[0], name_position[1] + 1.5 * font_size ), symbol_size/2, 6)
            
            text_font = pygame.font.SysFont(self.font, font_size, True )
            positions = (self.viewSize[0] + 15, center[1] - 0.75 * line_size)

            shift = 0.3
            D_Mod = text_font.render("Defence Modifier", True, font_color)
            D_Mod_rect = text_player.get_rect(midleft = positions )
            surface.blit(D_Mod, D_Mod_rect)

            D_Mod_Value = self.game_controler.get_terrain_defence_modifier( terrain_id )
            D_Mod_Value = str(D_Mod_Value)
            D_Mod_Value_text = text_font.render(D_Mod_Value, True, font_color)
            D_Mod_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(D_Mod_Value_text, D_Mod_Value_rect)

            positions = (positions[0], positions[1] + shift * line_size)

            Income = text_font.render("Income", True, font_color)
            Income_rect = text_player.get_rect(midleft = positions )
            surface.blit(Income, Income_rect)

            Income_Value = self.game_controler.get_terrain_income( terrain_id)
            Income_Value = str(Income_Value)
            Income_Value_text = text_font.render(Income_Value, True, font_color)
            Income_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(Income_Value_text, Income_Value_rect)

            positions = (positions[0], positions[1] + shift * line_size)

            name = self.game_controler.get_building_name( building_id )

            text_font = pygame.font.SysFont(self.font, name_font_size, True )

            text_player = text_font.render(name, True, "Black")
            text_player_rect = text_player.get_rect(center = (center[0], positions[1] ) )
            surface.blit(text_player, text_player_rect)

            positions = (positions[0], positions[1] + 0.9 * shift * line_size)
            
            # print(self.game_controler.get_building_symbol( building_id))
            
            font_view_size = font_size + 16
            symbol = self.game_controler.get_building_symbol( building_id) 

            font = pygame.freetype.Font(r"fonts/Noto_Emoji/NotoEmoji-VariableFont_wght.ttf", 32 )
            font.render_to(surface, (center[0] - 15, positions[1] - 15 ), symbol, (0, 0, 0))
            
            text_font = pygame.font.SysFont(self.font, font_size, True )
            positions = (positions[0], positions[1] + 1.1 * shift * line_size)

            D_Mod_Building = text_font.render("Defence Modifier", True, font_color)
            D_Mod_Building_rect = text_player.get_rect(midleft = positions )
            surface.blit(D_Mod_Building, D_Mod_Building_rect)

            D_Mod_Building_Value = self.game_controler.get_building_defence( building_id )
            D_Mod_Building_Value = str(D_Mod_Building_Value)
            D_Mod_Building_Value_text = text_font.render(D_Mod_Building_Value, True, font_color)
            D_Mod_Building_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(D_Mod_Building_Value_text, D_Mod_Building_Value_rect)

            positions = (positions[0], positions[1] + shift * line_size)

            Income_Building = text_font.render("Income", True, font_color)
            Income_Building_rect = text_player.get_rect(midleft = positions )
            surface.blit(Income_Building, Income_Building_rect)

            Income_Building_Value = self.game_controler.get_building_income( building_id )
            Income_Building_Value = str(Income_Building_Value)
            Income_Building_Value_text = text_font.render(Income_Building_Value, True, font_color)
            Income_Building_Value_rect = text_player.get_rect(midleft = (positions[0] + 215, positions[1]) )
            surface.blit(Income_Building_Value_text, Income_Building_Value_rect)


        



    def draw_next_turn(self, surface):

        font_size = 32

        size = [self.GUIsize[0], 50]
        gradient_color = self.GUI_gradient

        x = self.startX + self.viewSize[0]
        y = self.startY + self.viewSize[1] + self.GUIsize[1] - size[1]

        rect = pygame.Rect(x, y, size[0], size[1])

        pygame.draw.rect(surface, gradient_color, rect)

        text_font = pygame.font.SysFont(self.font, font_size, True )

        text = text_font.render("Next Turn =>", True, "Black")

        text_rect = text.get_rect(center=rect.center)

        surface.blit(text, text_rect)

        self.next_turn_rect = rect

    def draw_side(self, surface):
        color = self.GUI_color
        gradient_color = self.GUI_gradient
        font_size = 64

        points = [[self.startX + self.viewSize[0], self.startY], [self.startX + self.viewSize[0] + self.GUIsize[0], self.startY], [self.startX + self.viewSize[0] + self.GUIsize[0], self.startY + self.viewSize[1] + self.GUIsize[1]], [self.startX + self.viewSize[0], self.startY + self.viewSize[1] + self.GUIsize[1]]]


        size = (abs(points[0][0] - points[1][0]), abs(points[0][1] - points[2][1]))

        center = [points[0][0] + 0.5 * size[0], points[0][1] + 0.5 * size[1]]

        pygame.draw.polygon(surface, color, points, 0)

        self.draw_turn_block(surface)
        self.draw_next_turn(surface) 
        self.draw_null_block(surface)
        self.draw_table(surface, center)


    def get_clicked_unit(self, mouse_pos, unit_number):

        points = [
            [self.startX, self.startY + self.viewSize[1] + self.GUIsize[1]],
            [self.startX, self.startY + self.viewSize[1]],
            [self.startX + self.viewSize[0], self.startY + self.viewSize[1]],
            [self.startX + self.viewSize[0], self.startY + self.viewSize[1] + self.GUIsize[1]]
        ]

        size = (
            abs(points[0][0] - points[3][0]),
            abs(points[0][1] - points[1][1])
        )

        font_size = 64

        for i in range(1, unit_number + 1):

            position = (
                points[0][0] + i * size[0] / (unit_number + 1),
                points[0][1] - size[1] / 2
            )

            rect = pygame.Rect(0, 0, font_size, font_size)
            rect.center = position

            if rect.collidepoint(mouse_pos):
                return i - 1

        return None
    
    def next_turn_clicked(self, mouse_pos): 
        if self.next_turn_rect.collidepoint(mouse_pos):
            return True
        
        return False
    
    def null_block_clicked(self, mouse_pos): 
        if self.null_block_rect.collidepoint(mouse_pos):
            return True
        
        return False
    

    def get_clicked_province(self, mouse_pos):
        clicked_hex = self.pixel_to_hex(mouse_pos)
        # print(clicked_hex)
        
        all_provinces = self.game_controler.get_player_provinces(1)
        all_provinces += self.game_controler.get_player_provinces(2)

        for i in range(len(all_provinces)):
            province_hex_list = self.game_controler.get_province_hex_list(i)

            if( clicked_hex in province_hex_list):
                return i
            
        return None

    def draw_bottom(self, surface):
        color = self.GUI_color
        gradient_color = self.GUI_gradient
        font_size = 64

        points = [[self.startX, self.startY + self.viewSize[1] + self.GUIsize[1]], [self.startX, self.startY + self.viewSize[1]], [self.startX + self.viewSize[0], self.startY + self.viewSize[1]], [self.startX + self.viewSize[0], self.startY + self.viewSize[1] + self.GUIsize[1]]]


        size = (abs(points[0][0] - points[3][0]), abs(points[0][1] - points[1][1]))

        pygame.draw.polygon(surface, color, points, 0)

        unit_types = self.resource_manager.get_unit_types()

        unit_number = 0
        for i in unit_types:
            unit_number += 1

        for i in range (0, unit_number):            
            symbol = self.game_controler.get_unit_symbol(i)
            font = pygame.freetype.Font(r"fonts/Noto_Emoji/NotoEmoji-VariableFont_wght.ttf", 48 )

            position = ((points[0][0] + (i + 1) * size[0]/(unit_number + 1)-10,  points[0][1] - size[1]/2-20))
            font.render_to(surface, position, symbol, (0, 0, 0))

    def draw_GUI(self, surface):
        self.draw_bottom(surface)
        self.draw_side(surface)

    def get_clicked_object(self, mouse_pos):

        if self.next_turn_rect.collidepoint(mouse_pos):
            return {
                "type": "next_turn"
            }
        
        if self.null_block_rect.collidepoint(mouse_pos):
            return {
                "type": None
            }

        unit_types = self.resource_manager.get_unit_types()
        unit_number = 0
        for i in unit_types:
            unit_number += 1

        unit_id = self.get_clicked_unit(mouse_pos, unit_number)

        if unit_id is not None:
            return {
                "type": "unit",
                "id": unit_id
            }

        province = self.get_clicked_province(mouse_pos)

        if province is not None:
            return {
                "type": "province",
                "id": province,
                "object": province
            }

        return None

    def show_end( self, text ):
        bg_color=(30, 30, 30)
        text_color=(255, 255, 255)
        font_size=50

        surface = self.viewSurface
        # Wypełnij tło jednym kolorem
        surface.fill(bg_color)

        # Utwórz font
        font = pygame.font.SysFont(None, font_size)

        # Renderuj tekst
        rendered_text = font.render(text, True, text_color)

        # Wyśrodkuj tekst
        text_rect = rendered_text.get_rect(center=((self.viewSize[0] + self.GUIsize[0]) // 2, (self.viewSize[1] + self.GUIsize[1]) // 2))

        # Narysuj tekst
        surface.blit(rendered_text, text_rect)

        # Odśwież ekran
        pygame.display.update()

        surface = self.gameWindow
        # Wypełnij tło jednym kolorem
        surface.fill(bg_color)

        # Utwórz font
        font = pygame.font.SysFont(None, font_size)

        # Renderuj tekst
        rendered_text = font.render(text, True, text_color)

        # Wyśrodkuj tekst
        text_rect = rendered_text.get_rect(center=(500 // 2, 500 // 2))

        # Narysuj tekst
        surface.blit(rendered_text, text_rect)

        # Odśwież ekran
        pygame.display.update()

    def runGame(self):
        background = pygame.Surface(self.screenSize, pygame.SRCALPHA) 
        running = True

        self.draw_game(self.viewSurface)
        self.draw_glow(self.viewSurface)
        self.draw_GUI(self.gameWindow)

        while running:

            self.viewSurface.blit(background, (self.startX, self.startY))
            self.gameWindow.blit(self.viewSurface, (0,0))

            # draw GUI directly on gameWindow
            # self.draw_bottom(self.gameWindow)

            # print(self.game_controler.get_player_hexes(2))

            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False

                if self.win:
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = self.get_clicked_object(event.pos)
                    

                    if clicked is not None:

                        self.clicked = clicked
                        self.glow = None

                        if clicked["type"] == "unit":
                            self.selected_unit_type = self.clicked["id"]

                            # print("Unit:", self.clicked["id"])

                        elif clicked["type"] == "province":

                            unit_type = self.selected_unit_type
                            province_from = self.province_clicked_1
                            province_to = self.clicked["id"]

                            if self.game_controler.turn.get_phase() == ATTACK_PHASE:
                            
                                if self.province_clicked_1 == None:
                                    self.province_clicked_1 = self.clicked["id"]
                                else:
                                    result = self.game_controler.attack( province_from , province_to )

                                    if( result != False ):
                                        self.clicked["type"] = 'battle'
                                        self.clicked["attack"] = result

                                    self.province_clicked_1 = province_to

                            elif self.game_controler.turn.get_phase() == BUYING_PHASE:
                                
                                if unit_type != None:
                                    result = self.game_controler.buy_unit( unit_type, province_to )
                                    print( unit_type, province_to, result )

                            elif self.game_controler.turn.get_phase() == MOVEMENT_PHASE:

                                if self.province_clicked_1 == None:
                                    self.province_clicked_1 = self.clicked["id"]
                                else:
                                    #self.game_controler.move( province_from, 1, province_to, 1 )

                                    # print( "move:", province_from, province_to )
                                    self.province_clicked_1 = province_to

                            self.glow = self.clicked["id"]
                            # print(clicked["object"])
                            print("Province:", clicked["id"])

                        elif clicked["type"] == "next_turn":
                            self.game_controler.next_phase()
                            # print("NEXT TURN")
                            self.province_clicked_1 = None
                            self.selected_unit_type = None
                        
                        elif clicked["type"] == None:
                            # print("Null")
                            pass

                    self.draw_game(self.viewSurface)
                    self.draw_glow(self.viewSurface)
                    self.draw_GUI(self.gameWindow)

                    self.win = self.game_controler.check_win()
                    self.win = False
                    if self.win:
                        player_id = self.game_controler.get_current_player_id()
                        player_nick = self.game_controler.player_list[ player_id ].nick
                        self.show_end( "Winner:  Player " + str(player_nick) )
            
            scaled = pygame.transform.smoothscale(self.viewSurface, self.viewSize)
            self.gameWindow.blit(scaled, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            
            if( self.error == True):
                break
            
        pygame.quit()

    # 1) wyswietlanie jednostek - ok
    # 2) wczytujemy pierwsze 3 rzeczy - budtnek, odział 1, odział 2 - ok
    # 3) przestaw to na klasę - ok
    # 4) border hexes - ok
    # 5) przerzuc sie na reseource mangaer jak bedzie commitniety


pygame.init()

gameWindow = None
# gameWindow = pygame.display.set_mode((2000, 1000))

game = GameWindowClass( gameWindow , 0, 0, 1, 24, 20, 15)
game.runGame()
