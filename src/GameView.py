import pygame
import sys
import math
import json 
#importy
from game.resourceManager import ResourceManager
from game.game_controller import GameController


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

        # wczytywanie bazy danych
        self.resource_manager = ResourceManager()
        self.resource_manager.load_definitions()
        self.game_controler = GameController(self.resource_manager)
        
            
        # statystyki hexow
        self.scale = 1
        hexScale = 1 # <--------------------------------------------------------------
        hex_unscaled_number_x = int(self.origin_X_hex_number * hexScale) #30
        hex_unscaled_number_y = int(self.origin_Y_hex_number * hexScale) #20
        hex_unscaled_size = hex_size / hexScale
        self.proportions = math.sqrt(3) / 2

        self.waterColor = GameController.get_terrain_color(self, 0)

        self.glow = None
        self.glow_color = [150, 150, 150, 10]

        self.unit_number = 3


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
    
        self.gameSize = (self.viewSize[0] + self.GUIsize[0], self.viewSize[1] + self.GUIsize[1])

        self.gameWindow = pygame.display.set_mode((self.viewSize[0] + self.GUIsize[0], self.viewSize[1] + self.GUIsize[1]))
        self.viewSurface = pygame.Surface(self.viewSize, pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("IOIOIOIO")
        


        

        with open("scenario_one.json") as f:
            scenario_data = json.load(f)

        self.provinces = scenario_data["provinces"]
        # print(self.provinces)

    
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
        font_index = GameController.get_building_symbol_code(self, buildingID)
        symbol = GameController.get_building_symbol(self, buildingID)

        #symbol = '\u028F'
        size = int(3/2 * self.hex_size)
        # symbol = "h"
        # symbol = "‡"


        if( font_index == 0):
            font = pygame.font.SysFont("webdings", size)  
        elif(font_index == 1):
            font = pygame.font.SysFont("wingdings", size)  
        elif(font_index == 2):
            font = pygame.font.SysFont("wingdings2", size)  
        else:
            font = pygame.font.SysFont("wingdings3", size)  

        #font = pygame.font.SysFont("Segoe UI Symbol", size)
        # font = pygame.font.SysFont("freesansbold", int(3/2 * self.hex_size)) 
        text = font.render(symbol, True, "Black", None)
        textRect = text.get_rect()


        w = math.sqrt(3) * self.hex_size
        h = 2 * self.hex_size

        x_offset = w * position[0]
        y_offset = 1.5 * self.hex_size * position[1]

        if position[1] % 2 == 1:
            x_offset += w / 2
        
        pos_X = self.start_draw_pos[0] + x_offset
        pos_Y = self.start_draw_pos[1] + y_offset

        textRect.center = (pos_X, pos_Y)
        textRect.center = (pos_X  - self.hex_size * 0.05, pos_Y + self.hex_size * 0.05)
        surface.blit(text, textRect)

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

        text_font = pygame.font.SysFont("times new roman", font_size, True)

        if(font_index == 0):
            font = pygame.font.SysFont("webdings", font_size)  
        elif(font_index == 1):
            font = pygame.font.SysFont("wingdings", font_size)  
        elif(font_index == 2):
            font = pygame.font.SysFont("wingdings2", font_size)  
        else:
            font = pygame.font.SysFont("wingdings3", font_size)  

        text_symbol = font.render(symbol, True, "Black", None)
        text_symbol_rect = text_symbol.get_rect()

        text_text = text_font.render(count, True, "Black", None)
        text_text_rect = text_text.get_rect()

        #textRect.center = (pos_X, pos_Y)
        text_symbol_rect.center = (pos_X  - self.hex_size * 0.05, pos_Y + self.hex_size * 0.05 - self.hex_size/3)
        surface.blit(text_symbol, text_symbol_rect) 
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


    def draw_province(self, surface, province):
        province_hexes = province["hexList"]
        terrain_id = province["terrain_ID"]

        color = self.resource_manager.get_terrain_by_id(terrain_id).color

        self.draw_map(surface, province_hexes, color, 0)
        if(self.glow == province):
            # print(color)
            self.draw_map(surface, province_hexes, self.glow_color, 0)
            
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


    def get_clicked_province(self, mouse_pos):
        clicked_hex = self.pixel_to_hex(mouse_pos)

        for province in self.provinces:
            if clicked_hex in province["hexList"]:
                return province

        return None

    def draw_game(self, surface):
        pygame.draw.polygon(self.viewSurface, self.waterColor, [[self.startX, self.startY], [self.startX, self.viewSize[1]], [self.viewSize[0], self.viewSize[1]], [self.viewSize[0], self.startY]], 0)
        
        self.draw_full_map(surface, self.waterColor, 0)
        #tworzy prowincje
        for province in self.provinces:
            self.draw_province(surface, province)



        test = [[0,0],[1,0],[1,1], [0,1]]
        test2 = [[2,2],[2,1], [2,3], [3,2], [1, 2]]
        test3 = [[0,2], [0,3], [0,4], [1,4], [1, 3]]

        # zagladnij do game controlera o informacje jakie sa hexy (mapa)
        # z mapy biore liste prowincje
        # z kazdej prowincji biore liste hexow
        # i lista hexow to jest np test2

        player_provinces = [test, test2, test3]

        self.draw_player_stuff(surface, player_provinces, (255, 0, 0, 255))
        

        # self.draw_building(self.viewSurface, "l", 0 , test)
        # print(GameController.get_province_building(self, 0))
        self.draw_army(surface, "U", 0, 13 , "P", 1, 4, test)

    def draw_turn_block(self, surface):
        gradient_color = [109, 110, 112]

        size = [self.GUIsize[0], 75]
        points = [[self.startX + self.viewSize[0], self.startY], [self.startX + self.viewSize[0] + size[0], self.startY], [self.startX + self.viewSize[0] + size[0], self.startY + size[1]], [self.startX + self.viewSize[0], self.startY + size[1]]]

        pygame.draw.polygon(surface, gradient_color, points, 0)

    
    def draw_next_turn(self, surface):

        font_size = 32

        size = [self.GUIsize[0], 50]
        gradient_color = [109, 110, 112]

        x = self.startX + self.viewSize[0]
        y = self.startY + self.viewSize[1] + self.GUIsize[1] - size[1]

        rect = pygame.Rect(x, y, size[0], size[1])

        pygame.draw.rect(surface, gradient_color, rect)

        text_font = pygame.font.SysFont(
            "times new roman",
            font_size,
            True
        )

        text = text_font.render(
            "Next Turn =>",
            True,
            "Black"
        )

        text_rect = text.get_rect(center=rect.center)

        surface.blit(text, text_rect)

        self.next_turn_rect = rect

    def draw_side(self, surface):
        color = [72, 74, 79]
        gradient_color = [109, 110, 112]
        font_size = 64

        points = [[self.startX + self.viewSize[0], self.startY], [self.startX + self.viewSize[0] + self.GUIsize[0], self.startY], [self.startX + self.viewSize[0] + self.GUIsize[0], self.startY + self.viewSize[1] + self.GUIsize[1]], [self.startX + self.viewSize[0], self.startY + self.viewSize[1] + self.GUIsize[1]]]


        size = (abs(points[0][0] - points[1][0]), abs(points[0][1] - points[2][1]))

        center = [points[0][0] + 0.5 * size[0], points[0][1] + 0.5 * size[1]]

        pygame.draw.polygon(surface, color, points, 0)

        self.draw_turn_block(surface)
        self.draw_next_turn(surface)


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

    def draw_bottom(self, surface):
        color = [72, 74, 79]
        gradient_color = [109, 110, 112]
        font_size = 64

        points = [[self.startX, self.startY + self.viewSize[1] + self.GUIsize[1]], [self.startX, self.startY + self.viewSize[1]], [self.startX + self.viewSize[0], self.startY + self.viewSize[1]], [self.startX + self.viewSize[0], self.startY + self.viewSize[1] + self.GUIsize[1]]]


        size = (abs(points[0][0] - points[3][0]), abs(points[0][1] - points[1][1]))

        pygame.draw.polygon(surface, color, points, 0)

        for i in range (1, self.unit_number + 1):
            # font_index = GameController.get_unit_symbol_code(self.game_controler, i)
            font_index = 0
            # symbol = 
            symbol = "U"

            if(font_index == 0):
                font = pygame.font.SysFont("webdings", font_size)  
            elif(font_index == 1):
                font = pygame.font.SysFont("wingdings", font_size)  
            elif(font_index == 2):
                font = pygame.font.SysFont("wingdings2", font_size)  
            else:
                font = pygame.font.SysFont("wingdings3", font_size)  

            text_symbol = font.render(symbol, True, "Black", None)
            text_symbol_rect = text_symbol.get_rect()


            position = ((points[0][0] + i* size[0]/(self.unit_number + 1),  points[0][1] - size[1]/2))

            text_symbol_rect.center = position
            pygame.draw.rect(surface, gradient_color, text_symbol_rect, 0)
            surface.blit(text_symbol, text_symbol_rect)

    def draw_GUI(self, surface):
        self.draw_bottom(surface)
        self.draw_side(surface)

    def runGame(self):
        background = pygame.Surface(self.screenSize, pygame.SRCALPHA) 


        running = True

        while running:

            unit_number = 3

            self.viewSurface.blit(background, (self.startX, self.startY))
            self.gameWindow.blit(self.viewSurface, (0,0))

            # draw GUI directly on gameWindow
            # self.draw_bottom(self.gameWindow)

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    province = self.get_clicked_province(event.pos)
                
                    clicked = self.get_clicked_unit(pygame.mouse.get_pos(), self.unit_number)

                    if clicked is not None:
                        print("kliknięto unit:", clicked)
                    if (province is not None):
                        print("Province ID =", province["ID"])
                        self.glow = province
                    if self.next_turn_clicked(event.pos):
                        print("NEXT TURN")
                    

            self.draw_game(self.viewSurface)
            self.draw_GUI(self.gameWindow)
            
            scaled = pygame.transform.smoothscale(self.viewSurface, self.viewSize)
            self.gameWindow.blit(scaled, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            
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


# lista wszystkich getow