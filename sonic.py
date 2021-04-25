import retro
import pygame
from pygame.locals import *
import cv2
import numpy as np
import imutils
import csv #agregada para generar el csv
import datetime #la usamos solo para generar un nombre de archivo unico

video_size = 700, 700

def key_action():
    #["B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"]
    buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    keys=pygame.key.get_pressed()
    
    #atrapando otras teclas
    if keys[K_b]:
        buttons[0] = 1
    if keys[K_a]:
        buttons[1] = 1
    if keys[K_MODE]:
        buttons[2] = 1
    if keys[K_KP_ENTER]:
        buttons[3] = 1
        
    if keys[K_UP]:
        buttons[4] = 1
    if keys[K_DOWN]:
        buttons[5] = 1
    if keys[K_LEFT]:
        buttons[6] = 1
    if keys[K_RIGHT]:
        buttons[7] = 1
    
    #atrapando otras teclas    
    if keys[K_c]:
        buttons[8] = 1
    if keys[K_y]:
        buttons[9] = 1
    if keys[K_x]:
        buttons[10] = 1
    if keys[K_z]:
        buttons[11] = 1

    return buttons

pygame.init()
env = retro.make('SonicTheHedgehog-Genesis', 'GreenHillZone.Act1')
screen = pygame.display.set_mode(video_size)
env.reset()

done = False
clock = pygame.time.Clock()

unique_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')

#Utilizamos a para crear el archivo si no existe, em caso de existir lo abrimos y lo modificamos
with open('sonic-data-'+ unique_filename +'.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"])
    while not done:
        clock.tick(60) # Alentar un poco, quitar si prefieren entrar en modo ultra instinto
        img = env.render(mode='rgb_array') # Esta porqueria viene rotada, hay que darle forma.
        img = np.flipud(np.rot90(img))# La rotamos
        image_np = imutils.resize(img, width=500) # Le ponenes un  tamano descente
        surf = pygame.surfarray.make_surface(image_np)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        action = key_action()
        ob, rew, done, info = env.step(action)
        pygame.event.pump()## Escucha los eventos
        
        writer.writerow(action) #escribimos en el excel(csv) un nuevo registro.
        #print("Grabamos en el archivo")
        print("Action ", action, "Reward ", rew) 
