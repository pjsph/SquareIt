import pygame

window_surface = None

tileSize = None
gameSize = None

links = []

squares = []


def init():
    global window_surface
    pygame.init()
    pygame.display.set_caption("SquareIt!")
    window_surface = pygame.display.set_mode((700, 700))
    window_surface.fill((255, 255, 255))


def set_game_rules(tilesize, gamesize):
    global tileSize
    global gameSize
    tileSize = tilesize
    gameSize = gamesize


def set_test_variables(set_links):
    global links
    links = set_links

def fill_variables():
    global gameSize
    global tileSize

    # Creation des points en fonction de la taille gameSize
    for x in range(0, gameSize[0]):
        for y in range(0, gameSize[1]):
            pygame.draw.circle(window_surface, (0, 0, 0), [tileSize * (x + 1), tileSize * (y + 1)], 5)

    # Initialisation du tableau squares
    for i in range(0, (gameSize[0] - 1) * (gameSize[1] - 1)):
        squares.append((0, 0, 0, 0))

    # Creation des liens en fonction des points du tableau links
    for link in links:
        pygame.draw.line(
            window_surface,
            (0, 0, 0),
            [tileSize * (link[0] % gameSize[0] + 1), tileSize * (link[0] // gameSize[0] + 1)],
            [tileSize * (link[1] % gameSize[0] + 1), tileSize * (link[1] // gameSize[0] + 1)]
        )

    # Remplissage du tableau squares par rapport au tableau links
    for link in links:
        is_horizontal = True if (link[0] % gameSize[0] - link[1] % gameSize[0]) != 0 else False
        if is_horizontal:
            point = min(link[0], link[1])
            square = (gameSize[0] - 1) * (point // gameSize[0]) + point % gameSize[0]
            print(square)
            if square < (gameSize[0] - 1) * (gameSize[1] - 1):
                squares[square] = (1, squares[square][1], squares[square][2], squares[square][3])

            if square - (gameSize[0] - 1) >= 0:
                squares[square - (gameSize[0] - 1)] = (squares[square - (gameSize[0] - 1)][0], squares[square - (gameSize[0] - 1)][1], 1, squares[square - (gameSize[0] - 1)][3])

        elif not is_horizontal:
            point = min(link[0], link[1])
            square = (gameSize[0] - 1) * (point // gameSize[0]) + point % gameSize[0]

            if gameSize[0] - point % gameSize[0] > 1:
                squares[square] = (squares[square][0], squares[square][1], squares[square][2], 1)

            if gameSize[0] - point % gameSize[0] < gameSize[0]:
                squares[square - 1] = (squares[square - 1][0], 1, squares[square - 1][2], squares[square - 1][3])

def add_link(link):
    links.append(link)

    # Creation des liens en fonction des points du tableau links
    pygame.draw.line(
        window_surface,
        (0, 0, 0),
        [tileSize * (link[0] % gameSize[0] + 1), tileSize * (link[0] // gameSize[0] + 1)],
        [tileSize * (link[1] % gameSize[0] + 1), tileSize * (link[1] // gameSize[0] + 1)]
    )

    # Remplissage du tableau squares par rapport au tableau links
    is_horizontal = True if (link[0] % gameSize[0] - link[1] % gameSize[0]) != 0 else False
    if is_horizontal:
        point = min(link[0], link[1])
        square = (gameSize[0] - 1) * (point // gameSize[0]) + point % gameSize[0]
        print(square)
        if square < (gameSize[0] - 1) * (gameSize[1] - 1):
            squares[square] = (1, squares[square][1], squares[square][2], squares[square][3])

        if square - (gameSize[0] - 1) >= 0:
            squares[square - (gameSize[0] - 1)] = (squares[square - (gameSize[0] - 1)][0], squares[square - (gameSize[0] - 1)][1], 1, squares[square - (gameSize[0] - 1)][3])

    elif not is_horizontal:
        point = min(link[0], link[1])
        square = (gameSize[0] - 1) * (point // gameSize[0]) + point % gameSize[0]

        if gameSize[0] - point % gameSize[0] > 1:
            squares[square] = (squares[square][0], squares[square][1], squares[square][2], 1)

        if gameSize[0] - point % gameSize[0] < gameSize[0]:
            squares[square - 1] = (squares[square - 1][0], 1, squares[square - 1][2], squares[square - 1][3])

def init_game():
    # Creation des points en fonction de la taille gameSize
    for x in range(0, gameSize[0]):
        for y in range(0, gameSize[1]):
            pygame.draw.circle(window_surface, (0, 0, 0), [tileSize * (x + 1), tileSize * (y + 1)], 5)

    # Initialisation du tableau squares
    for i in range(0, (gameSize[0] - 1) * (gameSize[1] - 1)):
        squares.append((0, 0, 0, 0))

def output():

    # Test des carrÃƒÆ’Ã‚Â©s
    for i in range(0, len(squares)):
        square = squares[i]
        count = square[0] + square[1] + square[2] + square[3]
        print("Le carrÃƒÆ’Ã‚Â© " + str(i) + " a " + str(count) + " cotes remplis")


def main():
    init()
    set_game_rules(50, [6, 4])
    init_game()
    pygame.display.flip()

    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False

            if event.type == pygame.MOUSEMOTION:
                x = event.pos[0]
                y = event.pos[1]

                if tileSize-5<=x<=gameSize[0]*tileSize+5 :
                    X=x//tileSize+1
                    if X*tileSize-5<=x<=X*tileSize+5 :
                        point = X-1+gameSize[0]*(y//tileSize-1)
                        link = (point, point + gameSize[0])
                        if not links.__contains__(link):
                            add_link(link)

            pygame.display.update()

    pygame.quit()
if __name__ == '__main__':
    main()
