import pygame
from threading import Thread
import time

import ctypes
myappid = 'jbpj.squareit.0-1'  # Aider windows pour changer le logo dans la barre des taches
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

window_surface = None

tileSize = None
gameSize = None

links = []

squares = []

waiting_task = None
waiting = False

time_font = None
index_font = None

in_game = False

players = [["Joueur 1", (234, 60, 83, 124), 0], ["Joueur 2", (137, 207, 240, 124), 0]]


def init():
    """
    Initialiser le programme (pygame, etc.)
    """
    global window_surface
    global time_font
    global index_font
    pygame.init()
    pygame.display.set_caption("SquareIt!")
    icon = pygame.image.load("img\\logo.png")
    pygame.display.set_icon(icon)
    window_surface = pygame.display.set_mode((700, 700))
    window_surface.fill((255, 255, 255))
    time_font = pygame.font.SysFont("arial", 30)
    index_font = pygame.font.SysFont("arial", 12)


def init_game():
    """
    Permet d'initialiser les variables du jeu
    """
    global squares
    global links

    # Clear
    window_surface.fill((255, 255, 255))

    # Creation des points en fonction de la taille gameSize
    for x in range(0, gameSize[0]):
        for y in range(0, gameSize[1]):
            pygame.draw.circle(window_surface, (0, 0, 0), [tileSize * (x + 1), tileSize * (y + 1)], 5)

    # Initialisation du tableau squares
    if len(squares) != 0:
        squares = []
    for i in range(0, (gameSize[0] - 1) * (gameSize[1] - 1)):
        squares.append((0, 0, 0, 0))

    # (Re)initialisation du tableau links
    if len(links) != 0:
        links = []


def set_game_rules(tilesize, gamesize):
    """
    Definir la taille du jeu
    """
    global tileSize
    global gameSize
    tileSize = tilesize
    gameSize = gamesize


def timeout():
    """
    Fonction appelee lorsque le compte a rebours du joueur est termine
    """
    if len(players) == 2:  # Pour l'instant à 2 joueurs
        for player in players:
            if player != get_player_turn():
                add_point(player, 999)  # Pour que l'autre joueur gagne
                end_game()


def cancel_wait():
    """
    Fonction appelee pour arreter le compte a rebours present
    """
    global waiting_task
    global waiting
    if waiting_task is not None and waiting is not False:
        waiting = False
        waiting_task.join()
        waiting_task = None
    pygame.draw.rect(window_surface, (255, 255, 255), (600, 100, 100, 100))


def run(seconds, callback):
    """
    Fonction appelee lorsque le compte a rebours est lance, boucle du timer
    """
    global waiting
    global waiting_task
    ms = int(round(time.time() * 1000))
    ms -= 1000  # Pour que l'ecran se mette a jour tout de suite et pas apres une seconde
    seconds += 1  # Pour que ca parte de 20 a l'affichage et que ca finisse a 1
    while waiting:
        if ms <= int(round(time.time() * 1000)) - 1000:
            ms = int(round(time.time() * 1000))

            # Boucle mise a jour toutes les secondes
            seconds -= 1
            pygame.draw.rect(window_surface, (255, 255, 255), (400, 100, 210, 40))
            window_surface.blit(time_font.render("Temps restant : " + str(seconds), True, (0, 0, 0)), (400, 100))

            if seconds == 0:
                waiting = False
                waiting_task = None
                if callback is not None and callable(callback):
                    callback()
                return


def wait(seconds, callback):
    """
    Permet de lancer le compte a rebours
    """
    global waiting_task
    global waiting
    cancel_wait()
    waiting_task = Thread(target=run, args=[seconds, callback])
    waiting = True
    waiting_task.start()


def add_point(player, points=1):
    """
    Ajoute un (ou plusieurs) point(s) au joueur specifie. Ils seront utilises pour determiner le vainqueur
    """
    global players
    player_index = players.index(player)
    if len(players[player_index]) != 3:
        players[player_index].append(0)

    players[player_index][2] += points


def draw_square(square):
    """
    Permet de dessiner un carre si ses 4 cotes sont pleins, puis ajoute un point au joueur et redouble son tour
    """
    point = gameSize[0] * (square // (gameSize[0] - 1)) + (square % (gameSize[0] - 1))
    sumn = 0
    for value in squares[square]:
        sumn += value
    if sumn == 4:
        """pygame.draw.rect(window_surface, get_player_turn()[1], (
        (point % gameSize[0] + 1) * tileSize, (point // gameSize[0] + 1) * tileSize, tileSize, tileSize))"""
        s = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
        s.fill(get_player_turn()[1])
        window_surface.blit(s, ((point % gameSize[0] + 1) * tileSize, (point // gameSize[0] + 1) * tileSize))
        text = get_player_turn()[0].split(" ")
        initials = ""
        for word in text:
            initials += word[:1]
        text = index_font.render(initials, True, (0, 0, 0))
        size = index_font.size(get_player_turn()[0][-1:])
        window_surface.blit(text,
                            (int(round((point % gameSize[0] + 1) * tileSize + tileSize * 0.5 - size[0] / 2)),
                             int(round((point // gameSize[0] + 1) * tileSize + tileSize * 0.5 - size[1] / 2))))

        # Redessiner les points pour eviter les bugs d'affichage
        points = [point, point + 1, point + gameSize[0], point + 1 + gameSize[0]]
        for point in points:
            pygame.draw.circle(window_surface, (0, 0, 0),
                               [tileSize * (point % gameSize[0] + 1), tileSize * (point // gameSize[0] + 1)], 5)
        draw_link((points[0], points[1]))
        draw_link((points[0], points[2]))
        draw_link((points[1], points[3]))
        draw_link((points[2], points[3]))

        add_point(get_player_turn())
        check_end_game()
        set_player_turn(get_player_turn())


def add_link(link):
    """
    Permet d'ajouter un lien (cote d'un carre) dans le tableau qui les enregistre, et le dessine
    Appelee quand un joueur clique
    """
    links.append(link)

    # Creation des liens en fonction des points du tableau links
    draw_link(link, get_player_turn()[1])

    # Remplissage du tableau squares par rapport au tableau links
    is_horizontal = True if (link[0] % gameSize[0] - link[1] % gameSize[0]) != 0 else False
    if is_horizontal:
        point = min(link[0], link[1])
        square = (gameSize[0] - 1) * (point // gameSize[0]) + point % gameSize[0]
        print(square)
        if square < (gameSize[0] - 1) * (gameSize[1] - 1):
            squares[square] = (1, squares[square][1], squares[square][2], squares[square][3])
            draw_square(square)

        if square - (gameSize[0] - 1) >= 0:
            squares[square - (gameSize[0] - 1)] = (
            squares[square - (gameSize[0] - 1)][0], squares[square - (gameSize[0] - 1)][1], 1,
            squares[square - (gameSize[0] - 1)][3])
            draw_square(square - (gameSize[0] - 1))

    elif not is_horizontal:
        point = min(link[0], link[1])
        square = (gameSize[0] - 1) * (point // gameSize[0]) + point % gameSize[0]

        if gameSize[0] - point % gameSize[0] > 1:
            squares[square] = (squares[square][0], squares[square][1], squares[square][2], 1)
            draw_square(square)

        if gameSize[0] - point % gameSize[0] < gameSize[0]:
            squares[square - 1] = (squares[square - 1][0], 1, squares[square - 1][2], squares[square - 1][3])
            draw_square(square - 1)


def draw_link(link, color=(0, 0, 0)):
    """
    Permet de dessiner un lien avec une couleur, sans l'enregistrer
    Appelee lorsque le joueur passe la souris sur un lien, et qu'il doit etre affiche puis supprime
    """
    pygame.draw.line(
        window_surface,
        color,
        [tileSize * (link[0] % gameSize[0] + 1), tileSize * (link[0] // gameSize[0] + 1)],
        [tileSize * (link[1] % gameSize[0] + 1), tileSize * (link[1] // gameSize[0] + 1)]
    )

    # Redessiner les points pour eviter les bugs d'affichage
    for point in link:
        pygame.draw.circle(window_surface, (0, 0, 0),
                           [tileSize * (point % gameSize[0] + 1), tileSize * (point // gameSize[0] + 1)], 5)


def undraw_link(link):
    """
    Permet de supprimer un lien
    Appelee lorsque le joueur enleve la souris d'un lien, et qu'il doit se desafficher
    """
    # Creation d'un lien de même couleur que le fond
    pygame.draw.line(
        window_surface,
        (255, 255, 255),
        [tileSize * (link[0] % gameSize[0] + 1), tileSize * (link[0] // gameSize[0] + 1)],
        [tileSize * (link[1] % gameSize[0] + 1), tileSize * (link[1] // gameSize[0] + 1)]
    )

    # Redessiner les points pour eviter les bugs d'affichage
    for point in link:
        pygame.draw.circle(window_surface, (0, 0, 0),
                           [tileSize * (point % gameSize[0] + 1), tileSize * (point // gameSize[0] + 1)], 5)


"""
Variable qui stocke l'index du dernier joueur qui a joue (index du tableau players)
L'index du joueur actuel est last_player_index + 1
"""
last_player_index = players.__len__() - 2  # Initialisation pour que le joueur actuel soit le dernier, et donc qu'au
                                           # démarrage (avec le end_turn()), ce soit le premier


def get_player_turn():
    """
    Retourne l'index du joueur actuel
    """
    return players[(last_player_index + 1) % players.__len__()]


def set_player_turn(player):
    """
    Permet de fixer le tour actuel a celui du joueur passe en parametre
    Utilisee pour redoubler le tour d'un joueur apres qu'il ait rempli un carre
    """
    global last_player_index
    index = players.index(player)
    last_player_index = (players.__len__() - 1 if index - 2 == -1 else
                         (players.__len__() - 2 if index - 2 == -2 else index - 2))


def end_turn():
    """
    Permet de terminer le tour du joueur actuel, et de passer au suivant (relance le timer)
    """
    global last_player_index
    if not in_game:
        return
    size = time_font.size(get_player_turn()[0])
    pygame.draw.rect(window_surface, (255, 255, 255), (400, 50, size[0], size[1]))
    last_player_index = (last_player_index + 1) % players.__len__()
    window_surface.blit(time_font.render(get_player_turn()[0], True, get_player_turn()[1]), (400, 50))
    wait(20, timeout)


def end_game():
    """
    Permet de finir le jeu : determine le gagnant et affiche l'ecran de fin
    """
    global waiting
    global waiting_task
    global in_game
    max_point = 0
    winner = None
    for player in players:
        if player[2] > max_point:
            max_point = player[2]
            winner = player

    if winner is not None:
        window_surface.fill((255, 255, 255))
        size = time_font.size(winner[0] + " gagne !")
        window_surface.blit(time_font.render(winner[0] + " gagne !", True, winner[1]),
                            (int(round(window_surface.get_width() * 0.5 - size[0] / 2)),
                             int(round(window_surface.get_height() * 0.5 - size[1] / 2))))
        size = time_font.size("Cliquez pour recommencer")
        window_surface.blit(time_font.render("Cliquez pour recommencer", True, (0, 0, 0)),
                            (int(round(window_surface.get_width() * 0.5 - size[0] / 2)),
                             int(round(window_surface.get_height() * 0.5 + 50 - size[1] / 2))))
        in_game = False
        cancel_wait()


def check_end_game():
    """
    Permet de verifier si le jeu est termine : on regarde si tous les carres ont ete remplis
    La fonction end_game() est appelee si le jeu est termine
    """
    squared = 0
    for square in squares:
        if square[0] + square[1] + square[2] + square[3] == 4:
            squared += 1

    if squared == (gameSize[0] - 1) * (gameSize[1] - 1):
        end_game()


"""
Tableau qui stocke les liens affiches parce que le joueur passe la souris dessus, et qui devront etre supprimes
des qu'il enlevera sa souris
"""
to_undraw = []

init()


def main():
    """
    Fonction principale
    Contient la boucle du jeu
    """
    global in_game
    # Initialisation des regles du jeu
    set_game_rules(50, [6, 4])
    init_game()
    pygame.display.flip()

    launched = True

    in_game = True

    # Lancement du premier tour
    wait(20, timeout)
    end_turn()

    # Boucle du jeu
    while launched:
        for event in pygame.event.get():
            # Fermer le jeu
            if event.type == pygame.QUIT:
                launched = False

            # Lorsque la souris bouge
            if event.type == pygame.MOUSEMOTION:
                x = event.pos[0]
                y = event.pos[1]
                if in_game:
                    # On efface les liens a effacer
                    if to_undraw.__sizeof__() > 0:
                        for to_undraw_link in to_undraw:
                            to_undraw.remove(to_undraw_link)
                            undraw_link(to_undraw_link)

                    # Si la souris est dans l'aire de jeu (entre les points situes aux extremites + 5px de chaque cote)
                    if tileSize - 5 <= x <= gameSize[0] * tileSize + 5 and tileSize - 5 <= y <= gameSize[1] * tileSize + 5:
                        X = x // tileSize
                        Y = y // tileSize

                        # Si la souris est entre deux points l'un au dessus de l'autre (10px de large)
                        if X * tileSize <= x <= X * tileSize + 5 or (X + 1) * tileSize - 5 <= x <= (X + 1) * tileSize:
                            # On recupere le numero du point en haut
                            point = (X - 1 if X * tileSize <= x <= X * tileSize + 5 else X) + gameSize[0] * (y // tileSize - 1)
                            # On le lie a celui en dessous
                            link = (point, point + gameSize[0])
                            # S'il n'est pas deja enregistre, et que les points sont dans l'aire de jeu,
                            # on dessine le lien et on l'ajoute au tableau pour le supprimer plus tard
                            if not links.__contains__(link) and 0 <= point and point + gameSize[0] <= gameSize[0] * gameSize[1] - 1:
                                to_undraw.append(link)
                                draw_link(link, get_player_turn()[1])
                        # Si la souris est entre deux points l'un a la suite de l'autre (10px de hauteur)
                        elif Y * tileSize <= y <= Y * tileSize + 5 or (Y + 1) * tileSize - 5 <= y <= (Y + 1) * tileSize:
                            # On recupere le numero du point de gauche
                            point = X - 1 + gameSize[0] * (Y - 1 if Y * tileSize <= y <= Y * tileSize + 5 else Y)
                            # On le lie a celui a sa droite
                            link = (point, point + 1)
                            # S'il n'est pas deja enregistre, et que les points sont dans l'aire de jeu,
                            # on dessine le lien et on l'ajoute au tableau pour le supprimer plus tard
                            if not links.__contains__(link) and 0 <= point and point + 1 <= gameSize[0] * gameSize[1] - 1:
                                to_undraw.append(link)
                                draw_link(link, get_player_turn()[1])

            # Lorsqu'il y a un clique
            elif event.type == pygame.MOUSEBUTTONUP:
                # Ici, si le jeu est termine (ecran de fin), on relance la partie
                if not in_game:
                    main()
                    return

                # On teste si la souris est bien dans l'aire de jeu
                if tileSize - 5 <= x <= gameSize[0] * tileSize + 5 and tileSize - 5 <= y <= gameSize[1] * tileSize + 5:
                    X = x // tileSize
                    Y = y // tileSize
                    # Si la souris est entre deux points l'un au dessus de l'autre (10px de large)
                    if X * tileSize <= x <= X * tileSize + 5 or (X + 1) * tileSize - 5 <= x <= (X + 1) * tileSize:
                        # On recupere le numero du point en haut
                        point = (X - 1 if X * tileSize <= x <= X * tileSize + 5 else X) + gameSize[0] * (y // tileSize - 1)
                        # On le lie a celui en dessous
                        link = (point, point + gameSize[0])
                        # S'il n'est pas deja enregistre, et que les points sont dans l'aire de jeu,
                        # on dessine le lien et on l'enregistre dans le tableau squares
                        # On l'enleve des elements a desafficher
                        if not links.__contains__(link) and 0 <= point and point + gameSize[0] <= gameSize[0] * gameSize[1] - 1:
                            add_link(link)
                            end_turn()
                            if to_undraw.__contains__(link):
                                to_undraw.remove(link)

                    # Si la souris est entre deux points l'un a la suite de l'autre (10px de hauteur)
                    elif Y * tileSize <= y <= Y * tileSize + 5 or (Y + 1) * tileSize - 5 <= y <= (Y + 1) * tileSize:
                        # On recupere le numero du point de gauche
                        point = X - 1 + gameSize[0] * (Y - 1 if Y * tileSize <= y <= Y * tileSize + 5 else Y)
                        # On le lie a celui a sa droite
                        link = (point, point + 1)
                        # S'il n'est pas deja enregistre, et que les points sont dans l'aire de jeu,
                        # on dessine le lien et on l'enregistre dans le tableau squares
                        # On l'enleve des elements a desafficher
                        if not links.__contains__(link) and 0 <= point and point + 1 <= gameSize[0] * gameSize[1] - 1:
                            add_link(link)
                            end_turn()
                            if to_undraw.__contains__(link):
                                to_undraw.remove(link)

        pygame.display.update()

    cancel_wait()
    pygame.quit()


if __name__ == '__main__':
    main()
