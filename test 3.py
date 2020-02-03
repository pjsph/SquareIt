import pygame
from pygame.locals import *
pygame.init()

black = (0,0,0)
white = (255,255,255)
grey = (242,242,242)
grey_p = (218,218,218)
nuit=(127,127,127)

#definir la taille de la fenetre + charger les images
fen=pygame.display.set_mode((960,540))
main=pygame.image.load("main.png").convert()
logo_p=pygame.image.load("logo_p.jpg").convert()
logo_p_n=pygame.image.load("logo_p_n.jpg").convert()
logo_p_n.set_colorkey(nuit)
arrow=pygame.image.load("arrow.png").convert()
arrow_n=pygame.image.load("arrow_night.png").convert()
arrow_n.set_colorkey(black)
moon=pygame.image.load("moon.png").convert()
moon.set_colorkey(white)
moonlight=pygame.image.load("moonlight.jpg").convert()
moonlight.set_colorkey(white)
sound=pygame.image.load("sound.png").convert()
sound.set_colorkey(white)
soundoff=pygame.image.load("soundoff.png").convert()
soundoff.set_colorkey(white)

#montrer les parametres
show=0
shownight=0

#cacher lune et son
hide_moon=0
hide_sound=0

#desactiver le son
soundclicked=0

#mode nuit
nighton=0



continuer=1

#-----------------------------Boucle Jouer--------------------------------------
while continuer==1:

    #pour fermer la fenetre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer=0



        def menu():

            #Square it
            pygame.draw.rect(main,white, (0, 0, 960, 540))
            font_obj = pygame.font.Font("freesansbold.ttf", 32)
            text_surface_obj = font_obj.render("Square it", True, black, white)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (480, 72)
            main.blit(text_surface_obj, text_rect_obj)

            #La pipopipette officielle
            font_obj = pygame.font.Font("freesansbold.ttf", 10)
            text_surface_obj = font_obj.render("La pipopipette officielle", False, black, white)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (480, 111)
            main.blit(text_surface_obj, text_rect_obj)

            #ligne de séparation
            pygame.draw.line(main, black, (276, 131), (684, 131), 2)

            #bouton mode
            pygame.draw.rect(main,black, (413, 222, 113, 22))
            pygame.draw.rect(main,white, (415, 223, 111, 20))
            pygame.draw.rect(main,black, (525, 222, 22, 22))
            pygame.draw.rect(main,grey, (526, 223, 20, 20))
            #triangle de selection
            pygame.draw.polygon(main, black, ((530, 230), (540, 230), (535, 235)))
            #texte
            font_obj = pygame.font.Font("freesansbold.ttf", 12)
            text_surface_obj = font_obj.render("mode 1 vs 1", True, black, white)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (466, 233)
            main.blit(text_surface_obj, text_rect_obj)

            #bouton taille de grille
            pygame.draw.rect(main,black, (413, 283, 113, 22))
            pygame.draw.rect(main,white, (415, 284, 111, 20))
            pygame.draw.rect(main,black, (525, 283, 22, 22))
            pygame.draw.rect(main,grey, (526, 284, 20, 20))
            #triangle de selection
            pygame.draw.polygon(main, black, ((530, 290), (540, 290), (535, 295)))
            #texte
            font_obj = pygame.font.Font("freesansbold.ttf", 12)
            text_surface_obj = font_obj.render("taille 4*6", True, black, white)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (455, 295)
            main.blit(text_surface_obj, text_rect_obj)

            #bouton jouer
            pygame.draw.rect(main,black, (413, 390, 134, 37))
            pygame.draw.rect(main,white, (417, 394, 126, 29))
            #texte "jouer"
            font_obj = pygame.font.Font("freesansbold.ttf", 22)
            text_surface_obj = font_obj.render("Jouer", True, black, white)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (480, 410)
            main.blit(text_surface_obj, text_rect_obj)

        menu()

        def menu_nuit():

            #Square it
            pygame.draw.rect(main,nuit, (0, 0, 960, 540))
            font_obj = pygame.font.Font("freesansbold.ttf", 32)
            text_surface_obj = font_obj.render("Square it", True, white, nuit)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (480, 72)
            main.blit(text_surface_obj, text_rect_obj)

            #La pipopipette officielle
            font_obj = pygame.font.Font("freesansbold.ttf", 10)
            text_surface_obj = font_obj.render("La pipopipette officielle", False, white, nuit)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (480, 111)
            main.blit(text_surface_obj, text_rect_obj)

            #ligne de séparation
            pygame.draw.line(main, white, (276, 131), (684, 131), 2)

            #bouton mode
            pygame.draw.rect(main,black, (413, 222, 113, 22))
            pygame.draw.rect(main,white, (415, 223, 111, 20))
            pygame.draw.rect(main,black, (525, 222, 22, 22))
            pygame.draw.rect(main,grey, (526, 223, 20, 20))
            #triangle de selection
            pygame.draw.polygon(main, black, ((530, 230), (540, 230), (535, 235)))
            #texte
            font_obj = pygame.font.Font("freesansbold.ttf", 12)
            text_surface_obj = font_obj.render("mode 1 vs 1", True, black, white)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (466, 233)
            main.blit(text_surface_obj, text_rect_obj)

            #bouton taille de grille
            pygame.draw.rect(main,black, (413, 283, 113, 22))
            pygame.draw.rect(main,white, (415, 284, 111, 20))
            pygame.draw.rect(main,black, (525, 283, 22, 22))
            pygame.draw.rect(main,grey, (526, 284, 20, 20))
            #triangle de selection
            pygame.draw.polygon(main, black, ((530, 290), (540, 290), (535, 295)))
            #texte
            font_obj = pygame.font.Font("freesansbold.ttf", 12)
            text_surface_obj = font_obj.render("taille 4*6", True, black, white)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (455, 295)
            main.blit(text_surface_obj, text_rect_obj)

            #bouton jouer
            pygame.draw.rect(main,white, (413, 390, 134, 37))
            pygame.draw.rect(main,nuit, (417, 394, 126, 29))
            #texte "jouer"
            font_obj = pygame.font.Font("freesansbold.ttf", 22)
            text_surface_obj = font_obj.render("Jouer", True, white, nuit)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (480, 410)
            main.blit(text_surface_obj, text_rect_obj)

        def parametre():
            #fond + carre central
            pygame.draw.rect(main,white, (0, 0, 960, 540))
            pygame.draw.rect(main,grey_p, (340, 130, 281, 281))
        def parametre_nuit():
            #fond + carre central
            pygame.draw.rect(main,nuit, (0, 0, 960, 540))
            pygame.draw.rect(main,grey_p, (340, 130, 281, 281))

        #détecter clic sur :
        #paramètre
        if event.type == MOUSEBUTTONUP and event.button==1 and event.pos[0] > 41 and event.pos[0] < 69 and event.pos[1] < 69 and event.pos[1] > 41:
            show=1
        #retour
        if event.type == MOUSEBUTTONUP and event.button==1 and event.pos[0] > 40 and event.pos[0] < 70 and event.pos[1] < 110 and event.pos[1] > 80:
            show=0

        if show==1:
            parametre()
            #mode nuit/jour
            if event.type == MOUSEBUTTONUP and event.button==1 and event.pos[0] > 400 and event.pos[0] < 460 and event.pos[1] < 250 and event.pos[1] > 190:
                nighton=1
                hide_moon=1
            if event.type == MOUSEBUTTONUP and event.button==1 and event.pos[0] > 500 and event.pos[0] < 560 and event.pos[1] < 250 and event.pos[1] > 190:
                nighton=0
                hide_moon=0
            #mode silencieux/son
            if event.type == MOUSEBUTTONUP and event.button==1 and event.pos[0] > 400 and event.pos[0] < 460 and event.pos[1] < 360 and event.pos[1] > 300:
                soundclicked=1
                hide_sound=1
            if event.type == MOUSEBUTTONUP and event.button==1 and event.pos[0] > 500 and event.pos[0] < 560 and event.pos[1] < 365 and event.pos[1] > 305:
                soundclicked=0
                hide_sound=0

        if show==0:
            menu()
            #clic sur le bouton jouer (event.pos[0]= abcisse)
            if event.type == MOUSEBUTTONUP and event.button==1 and event.pos[0] > 394 and event.pos[0] < 526 and event.pos[1] < 428 and event.pos[1] > 390:
                print("Jouer !")

        #clic sur bouton paramètre en mode nuit
        if event.type == MOUSEBUTTONUP and event.button==1 and event.pos[0] > 41 and event.pos[0] < 69 and event.pos[1] < 69 and event.pos[1] > 41 and nighton==1:
            shownight=0

        if event.type == MOUSEBUTTONUP and event.button==1 and event.pos[0] > 40 and event.pos[0] < 70 and event.pos[1] < 110 and event.pos[1] > 80 and nighton==1:
            shownight=1

        if nighton==1 and shownight==1:
            menu_nuit()

        #passer du clic sur la lune au mode nuit
        if nighton==1 and shownight==0:
            parametre_nuit()


        #coller les images
        fen.blit(main,(0,0))
        if show==0:
            if nighton==0:
                fen.blit(logo_p,(40,40))
            if nighton==1:
                fen.blit(logo_p_n,(40,40))
        if show==1:
            if hide_sound==0:
                fen.blit(sound,(400,300))
            if hide_moon==0:
                fen.blit(moon,(400,190))
            if soundclicked==1:
                fen.blit(soundoff,(500,305))
            if nighton==1:
                fen.blit(moonlight,(500,190))
                fen.blit(arrow_n,(40,80))
            if nighton==0:
                fen.blit(arrow,(40,80))


        pygame.display.update()