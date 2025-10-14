import pygame
import json
import math
import random
import sys
import os
from random import choice, randint
from sys import exit

# --- config ---
with open("config.json", "r") as f:
    config = json.load(f)

values_dict = config["values"]
optionals_dict = config.get("optionals", {})


mu_dim_grass = values_dict["Grass_frict"]
mu_dim_sand = values_dict["Sand_frict"]
mu_dim_ice = values_dict["Ice_frict"]
mu_dim_asphalt = values_dict["Asphalt_frict"]

surfaces = {
    "Grass": {"mu": mu_dim_grass},
    "Sand": {"mu": mu_dim_sand},
    "Ice": {"mu": mu_dim_ice},
    "Asphalt": {"mu": mu_dim_asphalt}
}
 
Wind_strenght=values_dict["Wind_strenght"]

PIXELS_PER_METER = 25
AIR_DENSITY=1.22
PLAYER_AREA=1.5

def display_score(current_time):
   score_font=pygame.font.Font(None, 50)
   score_surface=score_font.render(f"Score:{int(current_time)}",False, (228,10,8))
   score_rect=score_surface.get_rect(center=(100,50)) 
   screen.blit(score_surface,score_rect)

def display_wind_indicator(wind_system):
    if not optionals_dict.get("Wind", False) or not wind_system.active:
        return
    
    # Usa la velocità del vento globale
    avg_vel_x = wind_system.vel_x
    avg_vel_y = wind_system.vel_y
    
    # Posizione dell'indicatore (in alto a destra)
    center_x, center_y = 900, 50
    
    # Disegna cerchio di sfondo
    pygame.draw.circle(screen, (255, 255, 255, 128), (center_x, center_y), 35, 2)
    
    # Calcola lunghezza e angolo della freccia
    magnitude = math.sqrt(avg_vel_x**2 + avg_vel_y**2)
    if magnitude > 0.1:
        # Scala la freccia (max 25 pixel)
        arrow_length = min(magnitude * 5, 25)
        angle = math.atan2(avg_vel_y, avg_vel_x)
        
        # Punto finale della freccia
        end_x = center_x + arrow_length * math.cos(angle)
        end_y = center_y + arrow_length * math.sin(angle)
        
        # Colore basato sull'intensità (da verde a rosso)
        intensity = min(magnitude / 5.0, 1.0)
        color = (int(255 * intensity), int(255 * (1 - intensity)), 0)
        
        # Disegna la linea principale
        pygame.draw.line(screen, color, (center_x, center_y), (end_x, end_y), 3)
        
        # Disegna la punta della freccia
        arrow_size = 8
        arrow_angle = 0.5
        left_x = end_x - arrow_size * math.cos(angle - arrow_angle)
        left_y = end_y - arrow_size * math.sin(angle - arrow_angle)
        right_x = end_x - arrow_size * math.cos(angle + arrow_angle)
        right_y = end_y - arrow_size * math.sin(angle + arrow_angle)
        
        pygame.draw.polygon(screen, color, [(end_x, end_y), (left_x, left_y), (right_x, right_y)])
        
        # Mostra intensità numerica
        font = pygame.font.Font(None, 20)
        text = font.render(f"{magnitude:.1f}", False, color)
        text_rect = text.get_rect(center=(center_x, center_y + 45))
        screen.blit(text, text_rect)
    else:
        # Nessun vento - disegna un punto
        pygame.draw.circle(screen, (100, 100, 100), (center_x, center_y), 3)

class WindSystem:
    def __init__(self):
        self.active = optionals_dict.get("Wind", True)
        self.duration = 5.0
        self.time_elapsed = 0.0
        
        # Velocità del vento globale
        self.start_x = random.uniform(-Wind_strenght, Wind_strenght)
        self.start_y = random.uniform(-Wind_strenght, Wind_strenght)
        self.end_x = random.uniform(-Wind_strenght, Wind_strenght)
        self.end_y = random.uniform(-Wind_strenght, Wind_strenght)
        self.vel_x = self.start_x
        self.vel_y = self.start_y
    
    def update(self, dt):
        if not self.active:
            self.vel_x = 0
            self.vel_y = 0
            return
        
        self.time_elapsed += dt
        t = min(self.time_elapsed / self.duration, 1.0)
        sin_t = 0.5 - 0.5 * math.cos(math.pi * t)
        
        self.vel_x = self.start_x + (self.end_x - self.start_x) * sin_t
        self.vel_y = self.start_y + (self.end_y - self.start_y) * sin_t
        
        if t >= 1.0:
            self.start_x = self.vel_x
            self.start_y = self.vel_y
            self.end_x = random.uniform(-Wind_strenght, Wind_strenght)
            self.end_y = random.uniform(-Wind_strenght, Wind_strenght)
            self.time_elapsed = 0.0
    
    def apply_to_player(self, player, dt):
        if not self.active:
            return
        
        wind_force_x = self.vel_x * 10
        wind_force_y = self.vel_y * 10
        
        acc_x = wind_force_x / player.mass
        acc_y = wind_force_y / player.mass
        
        player.vel_x += acc_x * dt * PIXELS_PER_METER
        player.vel_y += acc_y * dt * PIXELS_PER_METER

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        PLAYER_SIZE = (128, 128)
        walk1 = pygame.image.load("images/player/walk1.png").convert_alpha()
        walk2 = pygame.image.load("images/player/walk2.png").convert_alpha()
        walk3 = pygame.image.load("images/player/walk3.png").convert_alpha()
        self.jump_frame = pygame.image.load("images/player/jump.png").convert_alpha()
        self.stand_frame = pygame.image.load("images/player/walk2.png").convert_alpha()
        walk1 = pygame.transform.scale(walk1, PLAYER_SIZE)
        walk2 = pygame.transform.scale(walk2, PLAYER_SIZE)
        walk3 = pygame.transform.scale(walk3, PLAYER_SIZE)
        self.jump_frame  = pygame.transform.scale(self.jump_frame , PLAYER_SIZE)
        self.stand_frame = pygame.transform.scale(self.stand_frame, PLAYER_SIZE)
        self.walk_frames = [walk1, walk2, walk3]
        self.index = 0
        self.image = self.walk_frames[self.index]

        self.rect = self.image.get_rect(midbottom=(80, 450))
        self.mask = pygame.mask.from_surface(self.image)
        self.mass=values_dict["Dino_mass"]
        self.area=PLAYER_AREA
        self.vel_x=0.0
        self.vel_y=0.0
        self.on_ground=True
        self.ground_y=450

        self.max_input_force=600.0
        self.jump_velocity_initial = -math.sqrt(2 * values_dict["Gravity"] * 10.0) * PIXELS_PER_METER
    
    def gravity_force(self):
        return self.mass*values_dict["Gravity"]*2
    
    def friction_force(self,surface_name):
       if not self.on_ground or abs(self.vel_x)<0.1:
           return 0.0
       mu_k=surfaces[surface_name]["mu"]
       normal_force=self.mass*values_dict["Gravity"]
       friction_force=mu_k*normal_force
       return -friction_force if self.vel_x>0 else friction_force
    
    def air_resistance_force(self): 
        if not optionals_dict["Air resistance"]:
            return 0.0, 0.0
        vel_x_ms=self.vel_x/PIXELS_PER_METER
        vel_y_ms=self.vel_y/PIXELS_PER_METER
        drag_force_x=-0.5*AIR_DENSITY*values_dict["Air_coeff"]*self.area*vel_x_ms*abs(vel_x_ms)
        drag_force_y=-0.5*AIR_DENSITY*values_dict["Air_coeff"]*self.area*vel_y_ms*abs(vel_y_ms)
        return drag_force_x, drag_force_y
    
    def input_force(self):
        keys = pygame.key.get_pressed()
        force_input = 0.0
        
        if keys[pygame.K_LEFT]:
            force_input -= self.max_input_force
        if keys[pygame.K_RIGHT]:
            force_input += self.max_input_force
            
        return force_input
    
    def update_physics(self,dt,current_surface_name):
        #X
        force_input=self.input_force()
        force_friction=self.friction_force(current_surface_name)
        force_drag_x,force_drag_y=self.air_resistance_force()
        total_force_x=force_input+force_friction+force_drag_x
        acc_x=total_force_x/self.mass
        self.vel_x+=acc_x*dt* PIXELS_PER_METER
        max_speed_pixels=15.0*PIXELS_PER_METER
        self.vel_x=max(-max_speed_pixels,min(max_speed_pixels,self.vel_x))
        self.rect.x+=self.vel_x*dt
        #Y
        keys=pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y=self.jump_velocity_initial
            self.on_ground=False
        force_gravity=self.gravity_force()
        total_force_y=force_gravity+force_drag_y
        acc_y=total_force_y/self.mass
        self.vel_y+=acc_y*dt*PIXELS_PER_METER
        self.rect.y+=self.vel_y*dt
        if self.rect.bottom>=self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0.0
            self.on_ground = True
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0.0
        if self.rect.right > 1000:
            self.rect.right = 1000
            self.vel_x = 0.0

    def animate(self):
        keys = pygame.key.get_pressed()
        if self.on_ground:
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.index += 0.1
                if self.index >= len(self.walk_frames):
                    self.index = 0
                self.image = self.walk_frames[int(self.index)]
            else:
                self.image = self.stand_frame
        else:
            self.image = self.jump_frame
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt, current_surface_name):
        self.update_physics(dt,current_surface_name)
        self.animate()

class Backgrounds(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.grass_floor = pygame.image.load("images/backgrounds/grass_floor.png").convert_alpha()
        self.grass_sky = pygame.image.load("images/backgrounds/grass_sky.png").convert_alpha()
        self.ice_floor = pygame.image.load("images/backgrounds/ice_floor.png").convert_alpha()
        self.ice_sky = pygame.image.load("images/backgrounds/ice_sky.png").convert_alpha()
        self.asphalt_floor = pygame.image.load("images/backgrounds/asphalt_floor.png").convert_alpha()
        self.asphalt_sky = pygame.image.load("images/backgrounds/asphalt_sky.png").convert_alpha()
        self.sand_floor = pygame.image.load("images/backgrounds/sand_floor.png").convert_alpha()
        self.sand_sky = pygame.image.load("images/backgrounds/sand_sky.png").convert_alpha()

        self.grass_floor = pygame.transform.scale(self.grass_floor, (1000, 150))
        self.grass_sky = pygame.transform.scale(self.grass_sky, (1000, 450))
        self.ice_floor = pygame.transform.scale(self.ice_floor, (1000, 150))
        self.ice_sky = pygame.transform.scale(self.ice_sky, (1000, 450))
        self.asphalt_floor = pygame.transform.scale(self.asphalt_floor, (1000, 150))
        self.asphalt_sky = pygame.transform.scale(self.asphalt_sky, (1000, 450))
        self.sand_floor = pygame.transform.scale(self.sand_floor, (1000, 150))
        self.sand_sky = pygame.transform.scale(self.sand_sky, (1000, 450))

        self.surfaces = {
            "Grass": {"floor": self.grass_floor, "sky": self.grass_sky},
            "Sand": {"floor": self.sand_floor, "sky": self.sand_sky},
            "Ice": {"floor": self.ice_floor, "sky": self.ice_sky},
            "Asphalt": {"floor": self.asphalt_floor, "sky": self.asphalt_sky}
        }

        self.current_surface_name = "Grass"
        self.floor_image = self.grass_floor
        self.sky_image = self.grass_sky
        self.last_surface_change = pygame.time.get_ticks()
        self.next_change_time = randint(25000, 32000)

    def update_surface(self,obstacles_group=None):
     if optionals_dict["Surfaces"]==True:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_surface_change >= self.next_change_time:
            new_surface = choice(list(self.surfaces.keys()))
            self.current_surface_name = new_surface
            self.floor_image = self.surfaces[new_surface]["floor"]
            self.sky_image = self.surfaces[new_surface]["sky"]
            self.last_surface_change = current_time
            self.next_change_time = randint(25000, 32000)
            if obstacles_group:
                obstacles_group.empty()
     else:
        self.floor_image = self.surfaces["Grass"]["floor"]
        self.sky_image = self.surfaces["Grass"]["sky"]

class Obstacles(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        self.type = type
        self.set_sky_index = 0
        self.speed = 0

        FLOOR_SIZE=(96,96)
        cactus = pygame.image.load("images/obstacles/floor/cactus.png").convert_alpha()
        iceman = pygame.image.load("images/obstacles/floor/iceman.png").convert_alpha()
        tree = pygame.image.load("images/obstacles/floor/tree.png").convert_alpha()
        car = pygame.image.load("images/obstacles/floor/car.png").convert_alpha()
        
        self.grass_open=pygame.image.load("images/obstacles/sky/grass_open.png").convert_alpha()
        self.grass_close=pygame.image.load("images/obstacles/sky/grass_close.png").convert_alpha()
        self.sand_open=pygame.image.load("images/obstacles/sky/sand_open.png").convert_alpha()
        self.sand_close=pygame.image.load("images/obstacles/sky/sand_close.png").convert_alpha()
        self.asphalt_open=pygame.image.load("images/obstacles/sky/asphalt_open.png").convert_alpha()
        self.asphalt_close=pygame.image.load("images/obstacles/sky/asphalt_close.png").convert_alpha()
        self.ice_open=pygame.image.load("images/obstacles/sky/ice_open.png").convert_alpha()
        self.ice_close=pygame.image.load("images/obstacles/sky/ice_close.png").convert_alpha()

        self.grass_open=pygame.transform.scale(self.grass_open, FLOOR_SIZE)
        self.grass_close=pygame.transform.scale(self.grass_close, FLOOR_SIZE)
        self.sand_open=pygame.transform.scale(self.sand_open, FLOOR_SIZE)
        self.sand_close=pygame.transform.scale(self.sand_close, FLOOR_SIZE)
        self.asphalt_open=pygame.transform.scale(self.asphalt_open, FLOOR_SIZE)
        self.asphalt_close=pygame.transform.scale(self.asphalt_close, FLOOR_SIZE)
        self.ice_open=pygame.transform.scale(self.ice_open, (112,64))
        self.ice_close=pygame.transform.scale(self.ice_close,(112,64))

        cactus = pygame.transform.scale(cactus, FLOOR_SIZE)
        iceman = pygame.transform.scale(iceman, FLOOR_SIZE)
        tree = pygame.transform.scale(tree, FLOOR_SIZE)
        car = pygame.transform.scale(car, FLOOR_SIZE)

        self.set_obst_floor={"Grass":tree,"Sand":cactus,"Ice":iceman,"Asphalt":car}
        self.set_obst_sky={"Grass":[self.grass_open,self.grass_close],"Sand":[self.sand_open,self.sand_close],"Asphalt":[self.asphalt_open,self.asphalt_close],"Ice":[self.ice_open,self.ice_close]}

        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.mask = None

    def set_obstacles(self,current_surface_name,type, current_time):
        if type=="floor":
          self.image = self.set_obst_floor[current_surface_name]
          self.rect = self.image.get_rect(midbottom=(randint(1100,1400), 450))
          self.mask = pygame.mask.from_surface(self.image)
          if current_time>=0 and current_time<=50:
           self.speed = randint(6,7)
          elif current_time>=51 and current_time<=100:
           self.speed = randint(8,9)
          elif current_time>=101 and current_time<=150:
           self.speed = randint(9,10)
          elif current_time>=151:
           self.speed = randint(11,12)
        if type=="sky":
          self.image=self.set_obst_sky[current_surface_name][int(self.set_sky_index)]
          self.rect = self.image.get_rect(midbottom=(randint(1100,1400), 300))
          self.mask = pygame.mask.from_surface(self.image)
          if current_time>=0 and current_time<=50:
           self.speed = randint(7,8)
          elif current_time>=51 and current_time<=100:
           self.speed = randint(8,9)
          elif current_time>=101 and current_time<=150:
           self.speed = randint(10,11)
          elif current_time>=151:
           self.speed = randint(12,13)
    
    def animate_sky(self,current_surface_name):
     if current_surface_name in self.set_obst_sky and self.type=="sky":
        self.set_sky_index += 0.05
        if self.set_sky_index >= len(self.set_obst_sky[current_surface_name]):
            self.set_sky_index = 0
        self.image = self.set_obst_sky[current_surface_name][int(self.set_sky_index)]
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, current_surface_name, dt=None):
     if self.type=="sky":
         self.animate_sky(current_surface_name)
     self.rect.x -= self.speed
     if self.rect.right < 0:
            self.kill()

class Wind(pygame.sprite.Sprite):
    def __init__(self, wind_system, x_start=1000, y_range=(50, 400)):
        super().__init__()

        WIND_SIZE = (48, 48)
        wind1 = pygame.image.load("images/wind/wind1.png").convert_alpha()
        wind2 = pygame.image.load("images/wind/wind2.png").convert_alpha()
        wind1 = pygame.transform.scale(wind1, WIND_SIZE)
        wind2 = pygame.transform.scale(wind2, WIND_SIZE)
        self.wind_frames = [wind1, wind2]

        self.index = 0
        self.image = self.wind_frames[self.index]

        self.rect = self.image.get_rect(midbottom=(x_start, random.uniform(*y_range)))
        
        # Riferimento al sistema di vento globale
        self.wind_system = wind_system

    def animate(self):
      if optionals_dict["Wind"]==True:
        self.index += 0.1
        if self.index >= len(self.wind_frames):
            self.index = 0
        self.image = self.wind_frames[int(self.index)]

    def update(self, dt):
      if optionals_dict["Wind"]==True:
        self.animate()

        # Muovi secondo la velocità del vento globale
        self.rect.x += self.wind_system.vel_x * PIXELS_PER_METER * dt
        self.rect.y += self.wind_system.vel_y * PIXELS_PER_METER * dt
 
        # Se esce dallo schermo, elimina lo sprite
        if (self.rect.bottom >= 450 or self.rect.top < 0 or 
            self.rect.right < 0 or self.rect.left > 1000):
            self.kill()
  

class Trampolines(pygame.sprite.Sprite):
     def __init__(self):
        super().__init__()
        TRAMPOLINE_SIZE = (80, 80)
        trampoline = pygame.image.load("images/trampoline/trampoline.png").convert_alpha()
        trampoline = pygame.transform.scale(trampoline, TRAMPOLINE_SIZE)
        self.image=trampoline
        self.rect=self.image.get_rect(midbottom=(randint(1100,1400), 460))
        self.speed = 0
     def set_trampoline(self, current_time):
         if current_time>=0 and current_time<=50:
           self.speed = randint(6,7)
         elif current_time>=51 and current_time<=100:
           self.speed = randint(8,9)
         elif current_time>=101 and current_time<=150:
           self.speed = randint(9,10)
         elif current_time>=151:
           self.speed = randint(11,12)
         
     def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()




# ------------------ setup pygame ------------------
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Dino Runner")
icon = pygame.image.load("images/player/walk2.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

player = Player()
player_group = pygame.sprite.Group(player)
background = Backgrounds()

# Sistema di vento globale
wind_system = WindSystem()
wind_group = pygame.sprite.Group()

obstacles_group = pygame.sprite.Group()

def create_obstacle():
    type = choice(["floor", "sky"])
    obst = Obstacles(type)
    obst.set_obstacles(background.current_surface_name, type, current_time)
    return obst

trampoline_group=pygame.sprite.Group()

def create_trampoline():
    trampoline = Trampolines()
    trampoline.set_trampoline(current_time)
    return trampoline

# Timer ostacoli
OBSTACLE_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_TIMER, randint(2000, 2200))

TRAMPOLINE_TIMER=pygame.USEREVENT + 2
pygame.time.set_timer(TRAMPOLINE_TIMER, randint(8000, 15000))

running = True
game_active=True

while running:
    dt = clock.tick(60) / 1000.0
    current_time=pygame.time.get_ticks()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == OBSTACLE_TIMER:
            obstacles_group.add(create_obstacle())
        if event.type == TRAMPOLINE_TIMER and optionals_dict["Trampolines"]==True:
            trampoline_group.add(create_trampoline())
    if game_active:
        background.update_surface(obstacles_group)

        # Aggiorna il sistema di vento globale
        wind_system.update(dt)
        wind_system.apply_to_player(player, dt)

        player_group.update(dt, background.current_surface_name)
        
        if optionals_dict["Wind"]==True:
            MIN_WIND = 10
            MAX_WIND = 15

            current_wind_count = len(wind_group.sprites())

            if current_wind_count < MIN_WIND:
                for _ in range(MIN_WIND - current_wind_count):
                    wind_group.add(Wind(
                        wind_system,
                        x_start=random.uniform(0, 1000),
                        y_range=(50, 400)
                    ))
            elif current_wind_count > MAX_WIND:
                for wind in list(wind_group.sprites())[:current_wind_count - MAX_WIND]:
                    wind.kill()
        
        wind_group.update(dt)
        obstacles_group.update(background.current_surface_name)
        trampoline_group.update()

        screen.blit(background.sky_image, (0, 0))
        screen.blit(background.floor_image, (0, 450))
        player_group.draw(screen)
        obstacles_group.draw(screen)
        wind_group.draw(screen)
        trampoline_group.draw(screen)
        display_score(current_time)
        display_wind_indicator(wind_system)
        trampoline_collisions = pygame.sprite.spritecollide(player, trampoline_group, False, pygame.sprite.collide_mask)
        keys = pygame.key.get_pressed()

        trampoline_collisions = pygame.sprite.spritecollide(player, trampoline_group, False, pygame.sprite.collide_mask)
        if trampoline_collisions and player.on_ground and not keys[pygame.K_DOWN]:
            cc=values_dict["Coll_coeff"]
            player.vel_y = cc*-abs(player.vel_y)
            if abs(player.vel_y) < 10: 
                player.vel_y = -abs(player.jump_velocity_initial) * cc
            player.on_ground = False
            for trampoline in trampoline_collisions:
                trampoline.kill()
        if pygame.sprite.spritecollide(player, obstacles_group, False, pygame.sprite.collide_mask):
            game_active=False
    else:
     # Schermata intro
        screen.fill("#CBEA23")
        font_big = pygame.font.Font("font/Super_Joyful.ttf", 70)
        title = font_big.render("GAME OVER", False, "#4DC51D")
        game_over = pygame.image.load("images/player/sad.png").convert_alpha()
        game_over  = pygame.transform.scale(game_over , (256,256))
        restart = font_big.render("Press R to play again", False, "#4DC51D")
        menu = font_big.render("Press M to go back to the menu", False, "#4DC51D")
        quit = font_big.render("Press Q to quit the game", False, "#4DC51D")
        screen.blit(title, title.get_rect(center=(500,50)))
        screen.blit(game_over, game_over.get_rect(center=(500,250)))
        screen.blit(restart, restart.get_rect(center=(500, 400)))
        screen.blit(menu, menu.get_rect(center=(500, 475)))
        screen.blit(quit, quit.get_rect(center=(500, 550)))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            pygame.quit()
            python = sys.executable
            os.execl(python, python, "gui_game.py")
        if keys[pygame.K_r]:
           python = sys.executable
           os.execl(python, python, *sys.argv)
        if keys[pygame.K_q]:
           pygame.quit()
           exit()
        
    pygame.display.update()

pygame.quit()