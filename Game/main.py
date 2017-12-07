import pygame, sys, random
from math import atan2, degrees, sin, cos, sqrt
from pygame.locals import *

pygame.init()

res = [1280, 720]
screen = pygame.display.set_mode(res)

clock = pygame.time.Clock()

time = 0
speed = 0
planetx = -100
planety = -100
t = 0.1

font = pygame.font.SysFont('Calibri', 25)
score = 0
lvl = 1

class Missile:
    pass
class Rocket:
    pass
class Ennemi:
    pass
liste_missile = []
liste_rocket = []
liste_ennemi = []

def pythagore(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return sqrt(dx * dx + dy * dy)

def blit_center(image, pos):
    screen.blit(image, [pos[0] - image.get_width() / 2, pos[1] - image.get_height()/2])

vert = [0, 255, 0]

ship = pygame.image.load('assets/ship.png').convert_alpha()
blast = pygame.image.load('assets/blast.png').convert_alpha()
rocketimg = pygame.image.load('assets/rocket.png').convert_alpha()
background_800x600 = pygame.image.load('assets/background_800x600.png').convert_alpha()
background_1280x720 = pygame.image.load('assets/background_1280x720.png').convert_alpha()
planete = pygame.image.load('assets/planet.png').convert_alpha()
fire = pygame.image.load('assets/particles/fire.png')
pixel = pygame.image.load('assets/particles/pixel.png')
fire_yellow = pygame.image.load('assets/particles/fire_yellow.png')

compteur_ennemis = 0
compteur_rkt = 0
fini = 0
while fini == 0:
    time += 1
    position_souris = pygame.mouse.get_pos()
    mouse_x = position_souris[0]
    mouse_y = position_souris[1]
    image_score = font.render("Score: " + str(score), True, [255,255,255])
    image_lvl = font.render("Level: " + str(lvl), True, [255,255,255])
    image_vitesse = font.render(str(speed * 20) + "%", True, [255,255,255])
    if score >= 100:
        lvl += 1
        score = 0
    compteur_ennemis += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fini = 1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(liste_missile) >= 10:
                print ("reloading")
            else:
                le_missile = Missile()
                le_missile.x = res[0]/2
                le_missile.y = res[1]/2
                le_missile.angle = atan2(mouse_y - res[1]/2, mouse_x - res[0]/2)
                liste_missile.append(le_missile)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if len(liste_rocket) >= 1:
                    del liste_rocket[0]
                else:
                    rocket = Rocket()
                    rocket.x = res[0]/2
                    rocket.y = res[1]/2
                    liste_rocket.append(rocket)

    if time >= 60*10:
        t += 0.2
        time = 0
    if compteur_ennemis >= 60/t:
        compteur_ennemis = 0
        ennemi = Ennemi()
        liste_ennemi.append(ennemi)
        ramdomizer = random.randrange(4)
        if ramdomizer == 0:
            ennemi.x = res[0] + 20
            ennemi.y = random.randrange(res[1])
        else:
            if ramdomizer == 1:
                ennemi.x = -20
                ennemi.y = random.randrange(res[1])
            else:
                if ramdomizer == 2:
                    ennemi.x = random.randrange(res[0])
                    ennemi.y = -20
                else:
                    if ramdomizer == 3:
                        ennemi.x = random.randrange(res[0])
                        ennemi.y = res[1] + 20

    # supprimer les missles trop loin
    if len(liste_missile) > 0 and liste_missile[0].x >= res[0]:
        del liste_missile[0]
    if len(liste_missile) > 0 and liste_missile[0].y >= res[1]:
        del liste_missile[0]
    if len(liste_missile) > 0 and liste_missile[0].x <= 0:
        del liste_missile[0]
    if len(liste_missile) > 0 and liste_missile[0].y <= 0:
        del liste_missile[0]

    if len(liste_rocket) > 0 and liste_rocket[0].x >= res[0]:
        del liste_rocket[0]
    if len(liste_rocket) > 0 and liste_rocket[0].y >= res[1]:
        del liste_rocket[0]
    if len(liste_rocket) > 0 and liste_rocket[0].x <= 0:
        del liste_rocket[0]
    if len(liste_rocket) > 0 and liste_rocket[0].y <= 0:
        del liste_rocket[0]


    # bouger le vaisseau
    pressed = pygame.key.get_pressed()

    angle = atan2(mouse_y - res[1]/2, mouse_x - res[0]/2)

    if pressed[pygame.K_w]:
        speed += 0.1
    if speed >= 5:
        speed = 5
    if pressed[pygame.K_s]:
        speed -= 0.1
    if speed <= -5:
        speed = -5
    if speed == 0:
        etat = 0
    elif speed > 0:
        etat = 1
    elif speed < 0:
        etat = 2
    if pressed[pygame.K_SPACE]:
        if etat == 1:
            speed -= 0.1
            if speed <= 0:
                speed = 0
        if etat == 2:
            speed += 0.1
            if speed >= 0:
                speed = 0

    if etat != 0:
        planetx -= cos(angle) * speed/20
        planety -= sin(angle) * speed/20

    #missiles
    i = 0
    while i < len(liste_missile):
        liste_missile[i].x += 12 * cos(liste_missile[i].angle)
        liste_missile[i].y += 12 * sin(liste_missile[i].angle)
        i = i + 1
    #rocket
    j = 0
    while j < len(liste_rocket):
        angle_rocket = atan2(mouse_y - liste_rocket[j].y, mouse_x - liste_rocket[j].x)
        liste_rocket[j].x += 10 * cos(angle_rocket)
        liste_rocket[j].y += 10 * sin(angle_rocket)
        j += 1

    #collisions
    j = 0
    while j < len(liste_missile):
        m = liste_missile[j]
        i = 0
        while i < len(liste_ennemi):
            e = liste_ennemi[i]
            distance = pythagore([m.x, m.y],[e.x, e.y])
            if distance <= 40:
                del liste_ennemi[i]
                del liste_missile[j]
                i -= 1
                score += 1
            i += 1
        j += 1

    j = 0
    while j < len(liste_rocket):
        m = liste_rocket[j]
        i = 0
        while i < len(liste_ennemi):
            e = liste_ennemi[i]
            distance = pythagore([m.x, m.y],[e.x, e.y])
            if distance <= 40:
                del liste_ennemi[i]
                if len(liste_rocket) > 0:
                    del liste_rocket[j]
                i -= 1
                score += 1
            i += 1
        j += 1

    # DESSIN
    if res == [800,600]:
        screen.blit(background_800x600, [0,0])
    else:
        if res == [1280,720]:
            screen.blit(background_1280x720, [0,0])
    screen.blit(planete, [planetx,planety])


    # vaisseau
    ship_rot = pygame.transform.rotozoom(ship, - degrees(angle) + 90, 1)
    blit_center(ship_rot, [res[0]/2, res[1]/2])

    # missiles
    i = 0
    while i < len(liste_missile):
        blit_center(pygame.transform.rotozoom(blast, -degrees(liste_missile[i].angle),1), [liste_missile[i].x, liste_missile[i].y])
        i = i + 1

    # rocket
    j = 0
    while j < len(liste_rocket):
        angle_rocket = atan2(mouse_y - liste_rocket[j].y, mouse_x - liste_rocket[j].x)
        blit_center(pygame.transform.rotozoom(rocketimg, -degrees(angle_rocket),1), [liste_rocket[j].x, liste_rocket[j].y])
        j += 1
    if len(liste_rocket) > 0:
        rkt_time += 1
        n += 45
        pos_smoke = [liste_rocket[0].x - (n + random.randrange(-10,10))*cos(angle_rocket), liste_rocket[0].y - (n + random.randrange(-10,10))*sin(angle_rocket)]
        distance_rkt = pythagore([liste_rocket[0].x,liste_rocket[0].y],[pos_smoke[0],pos_smoke[1]])
        if distance_rkt <= 200:
            blit_center(fire_yellow, [pos_smoke[0] - 20*cos(angle_rocket),pos_smoke[1] - 20*sin(angle_rocket)])
        if distance_rkt <= 150:
            blit_center(fire_yellow, [pos_smoke[0] - 15*cos(angle_rocket) + 10*cos(angle_rocket + 5),pos_smoke[1] - 15*sin(angle_rocket) + 10*sin(angle_rocket + 5)])
            blit_center(fire_yellow, [pos_smoke[0] - 15*cos(angle_rocket) - 10*cos(angle_rocket + 5),pos_smoke[1] - 15*sin(angle_rocket) - 10*sin(angle_rocket + 5)])
        if distance_rkt <= 100:
            blit_center(fire, [pos_smoke[0] - 10*cos(angle_rocket) + 5*cos(angle_rocket + 5),pos_smoke[1] - 10*sin(angle_rocket) + 5*sin(angle_rocket + 5)])
            blit_center(fire, [pos_smoke[0] - 10*cos(angle_rocket) - 5*cos(angle_rocket + 5),pos_smoke[1] - 10*sin(angle_rocket) - 5*sin(angle_rocket + 5)])
        if distance_rkt <= 50:
            blit_center(pixel, [pos_smoke[0],pos_smoke[1]])
        else:
            if distance_rkt >= 200:
                n = 0
    else:
        if len(liste_rocket) <= 0:
            rkt_time = 0
            n = 0
    if rkt_time >= 60*2.5:
        del liste_rocket[0]

    # ennemi
    p = 0
    while p < len(liste_ennemi):

        angle_ennemi = atan2(res[1]/2 - liste_ennemi[p].y,res[0]/2 - liste_ennemi[p].x)
        ennemi_rot = pygame.transform.rotozoom(ship, - degrees(angle_ennemi) + 90, 1)
        liste_ennemi[p].x -= speed * cos(angle)
        liste_ennemi[p].y -= speed * sin(angle)
        liste_ennemi[p].x += cos(angle_ennemi) * 2
        liste_ennemi[p].y += sin(angle_ennemi) * 2
        blit_center(ennemi_rot,[liste_ennemi[p].x, liste_ennemi[p].y])
        p += 1

    screen.blit(image_score, [res[0] - 100, 20])
    screen.blit(image_lvl, [res[0] - 100,45])
    screen.blit(image_vitesse, [res[0] - 100,res[1] - 100])
    pygame.display.flip()

    clock.tick(60)
pygame.quit()