# base_jogo.py
import numpy
import pygame
import math
import time
from utils import *
from random import *
import sys
import neat
import os
import pickle

# --- INICIALIZAÇÃO DE IMAGENS E VARIÁVEIS GLOBAIS ---
GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)
TRACK_MASK = scale_image(pygame.image.load("imgs/track-mask.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

car_width, car_height = GREEN_CAR.get_size()
HALF_WIDTH = car_width / 2
HALF_HEIGHT = car_height / 2
CAR_SIZE = HALF_WIDTH, HALF_HEIGHT

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

pygame.font.init()
MAIN_FONT = pygame.font.SysFont("comicsans", 44)
FPS = 60
FINISH_POSITION = (130, 250)

# --- CLASSES BASE ---
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 1

    def rotate(self, left=False, right=False):
        if left and right:
            pass
        elif left:
            self.angle += self.rotation_vel + choice(range(-1,1))
        elif right:
            self.angle -= self.rotation_vel + choice(range(-1,1))
        self.angle = int(self.angle) % 360
        
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
        
    def move_backwards(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel//2)
        self.move()
    
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal
        
    def collide(self, mask, x=0, y=0):
        rotated_image = pygame.transform.rotate(self.img, self.angle)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        car_mask = pygame.mask.from_surface(rotated_image)
        offset = (int(new_rect.x - x), int(new_rect.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
        
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        x, y = int(self.x + CAR_SIZE[0]), int(self.y + CAR_SIZE[1])
        dx, dy = CAR_SIZE[0], CAR_SIZE[1]
        alfa = (self.angle) * math.pi / 180
        mrot = numpy.array([[math.cos(alfa), -math.sin(alfa)], [math.sin(alfa), math.cos(alfa)]])
        pts = numpy.array([[-dx, -dy], [dx, -dy], [-dx, dy], [dx, dy]])
        npts = numpy.dot(pts, mrot)
        for i in npts:
            if 0 <= i[0]+x < WIDTH and 0 <= i[1]+y < HEIGHT: 
                pygame.draw.circle(win, TRACK_MASK.get_at((int(i[0] + x), int(i[1] + y))), \
                                                          (int(i[0] + x), int(i[1] + y)), 2, 2)

class GameInfo:
    LEVELS = 10
    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0
    def next_level(self):
        self.level += 1
        self.started = False
    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0
    def game_finished(self):
        return self.level > self.LEVELS
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()
    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)