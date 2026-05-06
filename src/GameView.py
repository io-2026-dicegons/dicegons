import pygame
import sys
import math
import json 
#importy

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

        
            
        # statystyki hexow
        self.scale = 2
        hexScale = 1/2
        hex_unscaled_number_x = int(self.origin_X_hex_number * hexScale) #30
        hex_unscaled_number_y = int(self.origin_Y_hex_number * hexScale) #20
        hex_unscaled_size = 16 / hexScale
        self.proportions = math.sqrt(3) / 2

        self.waterColor = [38, 64, 171]

        # sandColor = [195, 172, 126]

        # tutaj jest system od skalowania mapy bo bez tego to strasznie spixelizowane bylo
        self.hex_number_x = hex_unscaled_number_x 
        self.hex_number_y = hex_unscaled_number_y 
        # self.hex_size = hex_unscaled_size * self.scale # <------------------------------------------------------------------

        self.viewSize = (hex_unscaled_number_x * 2 * self.proportions * hex_unscaled_size + hex_unscaled_size, 3/2 * hex_unscaled_number_y * hex_unscaled_size + 1/2*hex_unscaled_size)
        self.screenSize = (self.hex_number_x * 2 * self.proportions * self.hex_size + self.hex_size, 3/2 * self.hex_number_y * self.hex_size + 1/2*self.hex_size)
        #self.screenSize = (1000, 1000)

        self.start_draw_pos = (self.startX + self.proportions*self.hex_size , self.startY+ self.hex_size)

        #pygamestuff
        self.gameWindow = pygame.display.set_mode(self.viewSize)
        self.viewSurface = pygame.Surface(self.screenSize)

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("IOIOIOIO")

        # wczytywanie bazy danych
        with open("scenario_one.json") as f:
            scenario_data = json.load(f)

        self.provinces = scenario_data["provinces"]

        with open("terrain_types.json") as f:
            terrain_data = json.load(f)

        self.terrain = terrain_data["terrain_types"]

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
        

    def draw_border_hex(self, surface, color, width, position, edge):  
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

    def draw_border_map(self, surface, hex_list, color, width): #granice miedzy prowincjami
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

    def draw_building(self, surface, symbol, font_index, hex_list):
        
        position = hex_list[2]

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

        if( font_index == 0):
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

        color = self.terrain[terrain_id]["color"]

        self.draw_map(surface, province_hexes, color, 0)
        self.draw_border_map(surface, province_hexes, "black", 2)
        
    def draw_player_stuff(self, surface, player_provinces, color):
        for i in range(len(player_provinces)):
            self.draw_player_border(surface, player_provinces, i, color, 0, 1/4)




    #pygame stuff v2


    def runGame(self):
        background = pygame.Surface(self.screenSize, pygame.SRCALPHA) 
        background.fill("grey") 

        running = True
        while running:
            
            self.viewSurface.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # rysuje cala mape poza jako wode 
            self.draw_full_map(self.viewSurface, self.waterColor, 0)

            #tworzy prowincje
            for province in self.provinces:
                self.draw_province(self.viewSurface, province)



            test = [[0,0],[1,0],[1,1], [0,1]]
            test2 = [[2,2],[2,1], [2,3], [3,2], [1, 2]]
            test3 = [[0,2], [0,3], [0,4], [1,4], [1, 3], [1, 5]]

            player_provinces = [test, test2, test3]

            self.draw_player_stuff(self.viewSurface, player_provinces, "red")

            test4 = [[[3,0], [4,0], [4,1], [4,2], [2, 0], [3,1]]]
            self.draw_player_stuff(self.viewSurface, test4, "green")

            self.draw_building(self.viewSurface, "0", 3 , test)
            self.draw_army(self.viewSurface, "U", 0, 13 , "P", 1, 4, test)
    

            
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

game = GameWindowClass( gameWindow , 0, 0, 1, 16, 30, 20)
game.runGame()
