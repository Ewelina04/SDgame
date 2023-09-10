# -*- coding: utf-8 -*-


# python C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\main_sc.py

from psychopy import visual, event, core
import pandas as pd
#import filterlib as flt
#import blink as blk



class FltRealTime(object):
    def __init__(self, flt_type='4A'):
        self.prev_x = np.zeros((8, 5))
        self.prev_y = np.zeros((8, 5))
        self.prev_x2 = np.zeros((8, 5))
        self.prev_y2 = np.zeros((8, 5))

        self.flt_type = flt_type

    def filterIIR(self, data, nrk):
        # b = 0.0
        # a = 0.0
        # b2 = 0.0
        # a2 = 0.0

        b = np.array([1, 1, 1, 1, 1])
        a = np.array([1, 1, 1, 1, 1])

        b2 = np.array([1, 1, 1, 1, 1])
        a2 = np.array([1, 1, 1, 1, 1])

        j = 5 - 1
        while j > 0:
            self.prev_x[nrk, j] = self.prev_x[nrk, j - 1]
            self.prev_y[nrk, j] = self.prev_y[nrk, j - 1]
            self.prev_x2[nrk, j] = self.prev_x2[nrk, j - 1]
            self.prev_y2[nrk, j] = self.prev_y2[nrk, j - 1]
            j -= 1

        self.prev_x[nrk, 0] = data

        # 1-50Hz
        if ('1' in self.flt_type):
            b = np.array([
                0.2001387256580675,
                0,
                -0.4002774513161350,
                0,
                0.2001387256580675
                ])
            a = np.array([
                1,
                -2.355934631131582,
                1.941257088655214,
                -0.7847063755334187,
                0.1999076052968340
                ])
        # 7-13Hz
        if ('2' in self.flt_type):
            b = np.array([
                0.005129268366104263,
                0,
                -0.01025853673220853,
                0,
                0.005129268366104263
                ])
            a = np.array([
                1, -3.678895469764040,
                5.179700413522124,
                -3.305801890016702,
                0.8079495914209149
                ])

        # 15-50Hz
        if ('3' in self.flt_type):
            b = np.array([
                0.1173510367246093,
                0,
                -0.2347020734492186,
                0,
                0.1173510367246093
                ])
            a = np.array([
                1,
                -2.137430180172061,
                2.038578008108517,
                -1.070144399200925,
                0.2946365275879138
                ])

        # 5-50Hz
        if ('4' in self.flt_type):
            b = np.array([
                0.1750876436721012,
                0,
                -0.3501752873442023,
                0,
                0.1750876436721012
                ])
            a = np.array([
                1,
                -2.299055356038497,
                1.967497759984450,
                -0.8748055564494800,
                0.2196539839136946
                ])

        # none
        if ('5' in self.flt_type):
            b = np.array([1, 1, 1, 1, 1])
            a = np.array([1, 1, 1, 1, 1])

        # 50 Hz
        if ('A' in self.flt_type):
            b2 = np.array([
                0.96508099,
                -1.19328255,
                2.29902305,
                -1.19328255,
                0.96508099
                ])
            a2 = np.array([
                1,
                -1.21449347931898,
                2.29780334191380,
                -1.17207162934772,
                0.931381682126902
                ])

        # 60 Hz
        if ('B' in self.flt_type):
            b2 = np.array([
                0.9650809863447347,
                -0.2424683201757643,
                1.945391494128786,
                -0.2424683201757643,
                0.9650809863447347
                ])
            a2 = np.array([
                1,
                -0.2467782611297853,
                1.944171784691352,
                -0.2381583792217435,
                0.9313816821269039
                ])

        # none
        if ('C' in self.flt_type):
            b2 = np.array([1, 1, 1, 1, 1])
            a2 = np.array([1, 1, 1, 1, 1])

        filtered = self.filter_data(b2, a2, b, a, nrk)
        return filtered

    def filter_data(self, b2, a2, b, a, nrk):
        wynik = 0.0
        for j in range(5):
            wynik += b2[j] * self.prev_x[nrk, j]
            if j > 0:
                wynik -= a2[j] * self.prev_y[nrk, j]
        self.prev_y[nrk, 0] = wynik
        self.prev_x2[nrk, 0] = wynik
        wynik = 0.0
        for j in range(5):
            wynik += b[j] * self.prev_x2[nrk, j]
            if j > 0:
                wynik -= a[j] * self.prev_y2[nrk, j]
        self.prev_y2[nrk, 0] = wynik
        return wynik



class BlinkRealTime(object):

    def __init__(self):
        self.blinks_num = 0
        self.new_blink = False
        self.zero_crossed = True
        self.prev_val = 0.0
        self.visual = np.array([])

    def blink_detect(self, value, thr):
        self.visual = np.append(self.visual, [0.0])

        # if there is no new blink detected then this is False
        self.new_blink = False

        if value < thr and self.prev_val >= thr \
                and self.zero_crossed is True:
            if (len(self.visual) > 2):
                # blink detected at this function call
                self.new_blink = True
                self.blinks_num += 1
                self.visual[-2] = thr
                self.visual[-1] = -thr
                self.zero_crossed = False

        if self.prev_val > 0.0 and value <= 0.0:
            self.zero_crossed = True

        self.prev_val = value

#from pyOpenBCI import OpenBCIGanglion

import pygame
from pygame.locals import *
import random
import datetime
import time
import multiprocessing as mp




def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()


####################################################
    SYMULACJA_SYGNALU = True #False
####################################################
    mac_adress = 'f0:a6:74:94:b3:4d'
####################################################

    clock = pg.time.Clock()
    frt = FltRealTime()
    brt = BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv(r'C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\dane_do_symulacji\data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":

    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')



#stałe
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 450
ROAD_HEIGHT = 250
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 25
scooby_POS_X = 100
scooby_POS_Y = ROAD_HEIGHT - 16
zombie_POS_Y = ROAD_HEIGHT - 20
ghost_POS_X = (scooby_POS_X- 80)
ghost_POS_Y = ROAD_HEIGHT - 46
snack_POS_X = (scooby_POS_X + 441)
snack_POS_Y = ROAD_HEIGHT - 212

pygame.init()
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scooby Doo Game')
clock = pygame.time.Clock()


scooby_list = []
scooby_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics\scoobyjump.png")) #0
scooby_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics\scoobyrun1.png")) #1
scooby_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics\scoobyrun2.png")) #2
scooby_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics\scoobyjump.png")) #3
run_indx = 1

road1 = pygame.image.load(r'C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/ziemia.png')
road2 = pygame.image.load(r'C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/ziemia.png')

ghost_list = []
ghost_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/ghost.png")) #0
ghost_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/ghost.png")) #1

snack_list = []
snack_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/snack.png")) #0
snack_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/snack.png")) #1

zombie_list = []
zombie_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/grave3.png")) #0
zombie_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/hand.png")) #1
zombie_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/grave.png")) #2
zombie_list.append(pygame.image.load(r"C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/grave2.png")) #3

background = pygame.image.load(r'C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\graphics/tlo.jpg')

road1_pos_x = 0
road2_pos_x = 600

pygame.mixer.init()
pygame.mixer.music.load(r'C:\Users\User\Downloads\KogMilion\ScoobyDoo-master\scooby doo.mp3')
pygame.mixer.music.play()

speed_was_up = True
clear_game = True
game_on = False
lost_game = True
scooby_jump = False
jump_height = 7
points = 0

frames_since_zombie = 0
gen_zombie_time = 50


font = pygame.font.SysFont("Times New Roman", 18)
points_font = pygame.font.SysFont('Times New Roman', 18)
startScreen = font.render('NACIŚNIJ SPACJĘ ABY ZACZĄĆ', True, WHITE, BLACK)
startScreenRect = startScreen.get_rect()
startScreenRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)


gaming = True
while gaming:

    if blink.value == 1:
        if scooby_jump == False:
            game_on = True
            scooby_jump = True
            blink.value = 0
        if lost_game == True:
            time.sleep(1)
            clear_game = True
            lost_game = False
            blink.value = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_program.set()
                pygame.quit()
                quit()
                gaming = False

            if event.key == pygame.K_SPACE and scooby_jump == False:
                game_on = True
                scooby_jump = True
            if lost_game == True and event.key == pygame.K_SPACE:
                time.sleep(1)
                clear_game = True
                lost_game = False
                pygame.mixer.music.unpause()


    if clear_game == True:
        FPS = 25
        zombie_pos_x = []
        curr_zombie = []
        speed = 10
        points = 0
        clear_game = False

    gameDisplay.fill(BLACK)
    gameDisplay.blit(background,(0,0))
    gameDisplay.blit(road1, (road1_pos_x, ROAD_HEIGHT))
    if game_on == False:
        gameDisplay.blit(startScreen, startScreenRect)

    if game_on == True and lost_game == True:
        gameDisplay.blit(startScreen, startScreenRect)
        lostScreen = font.render('LICZBA SCOOBY CHRUPEK: ' + str(points), True, WHITE, BLACK)
        lostScreenRect = lostScreen.get_rect()
        lostScreenRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2-25)
        gameDisplay.blit(lostScreen, lostScreenRect)


    if speed_was_up == False and points%5 == 0:
        FPS += 3
        speed_was_up = True
    if points%5 == 1:
        speed_was_up = False

    if game_on == True:
        pointsDisplay = points_font.render('SCOOBY-CHRUPKI: ' + str(points), True, WHITE, BLACK)
        pointsRect = pointsDisplay.get_rect()
        pointsRect.center = (SCREEN_WIDTH-105, 10)
        gameDisplay.blit(pointsDisplay, pointsRect)


    if game_on == True and scooby_jump == False and lost_game == False:
        if run_indx <= 3:
            scooby = gameDisplay.blit(scooby_list[1], (scooby_POS_X, scooby_POS_Y))
            ghost = gameDisplay.blit(ghost_list[0], (ghost_POS_X, ghost_POS_Y))
            snack = gameDisplay.blit(snack_list[0], (snack_POS_X, snack_POS_Y))
            run_indx += 1
        elif run_indx < 6:
            scooby = gameDisplay.blit(scooby_list[2], (scooby_POS_X, scooby_POS_Y))
            ghost = gameDisplay.blit(ghost_list[1], (ghost_POS_X, ghost_POS_Y))
            snack = gameDisplay.blit(snack_list[1], (snack_POS_X, snack_POS_Y))
            run_indx += 1
        else:
            scooby = gameDisplay.blit(scooby_list[2], (scooby_POS_X, scooby_POS_Y))
            ghost = gameDisplay.blit(ghost_list[1], (ghost_POS_X, ghost_POS_Y))
            snack = gameDisplay.blit(snack_list[1], (snack_POS_X, snack_POS_Y))
            run_indx = 1
    elif game_on == False:
        scooby = gameDisplay.blit(scooby_list[0], (scooby_POS_X, scooby_POS_Y))
        ghost = gameDisplay.blit(ghost_list[0], (ghost_POS_X, ghost_POS_Y))
        snack = gameDisplay.blit(snack_list[0], (snack_POS_X, snack_POS_Y))

    if game_on == True and scooby_jump == True:
        if jump_height >= -7:
            going_up = 1
            if jump_height < 0:
                going_up = -1
            scooby_POS_Y -= (jump_height ** 2) * 0.8 * going_up
            ghost = gameDisplay.blit(ghost_list[1], (ghost_POS_X, ghost_POS_Y))
            snack = gameDisplay.blit(snack_list[1], (snack_POS_X, snack_POS_Y))
            jump_height -= 1
        else:
            scooby_jump = False
            jump_height = 7
        scooby = gameDisplay.blit(scooby_list[0], (scooby_POS_X, scooby_POS_Y))


    if game_on == True:
        frames_since_zombie += 1
        road1_pos_x -= speed
        if road1_pos_x <= -SCREEN_WIDTH:
            gameDisplay.blit(road2, (road2_pos_x, ROAD_HEIGHT))
            road2_pos_x -= speed
            if road2_pos_x == 0:
                road2_pos_x = 600
                road1_pos_x = 0

    if frames_since_zombie == gen_zombie_time:
        gen_zombie_time = random.randint(30, 50)
        gen_zombie_img = random.randint(0, 3)
        frames_since_zombie = 0
        curr_zombie.append([gen_zombie_img, SCREEN_WIDTH])

    for i in range(len(curr_zombie)):
        if curr_zombie[i][0] == 0 or curr_zombie[i][0] == 3:
            lower = 12
        else: lower = 0
        zombie = gameDisplay.blit(zombie_list[curr_zombie[i][0]], (curr_zombie[i][1], zombie_POS_Y+lower))
        curr_zombie[i][1] -= speed

        if curr_zombie[i][1] == 0:
            points += 1

        if scooby.colliderect(zombie):
            speed = 0
            if lost_game == False:
                pygame.mixer.music.pause()
            lost_game = True
            scooby = gameDisplay.blit(scooby_list[2], (scooby_POS_X, scooby_POS_Y))


    pygame.display.update()
    clock.tick(FPS)

proc_blink_det.join()
