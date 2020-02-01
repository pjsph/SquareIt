import pygame

window_surface = None

tileSize = None
gameSize = None

links = None

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
            if square < (gameSize[0] - 1) * (gameSize[1] - 1):
                squares[square] = (1, squares[square][1], squares[square][2], squares[square][3])

            if square - 3 >= 0:
                squares[square - 3] = (squares[square - 3][0], squares[square - 3][1], 1, squares[square - 3][3])

        elif not is_horizontal:
            point = min(link[0], link[1])
            square = (gameSize[0] - 1) * (point // gameSize[0]) + point % gameSize[0]

            if gameSize[0] - point % gameSize[0] > 1:
                squares[square] = (squares[square][0], squares[square][1], squares[square][2], 1)

            if gameSize[0] - point % gameSize[0] < 4:
                squares[square - 1] = (squares[square - 1][0], 1, squares[square - 1][2], squares[square - 1][3])


def output():

    # Test des carrés
    for i in range(0, len(squares)):
        square = squares[i]
        count = square[0] + square[1] + square[2] + square[3]
        print("Le carré " + str(i) + " a " + str(count) + " cotés remplis")


def main():
    init()
    set_game_rules(50, [4, 4])
    set_test_variables([(0, 1), (0, 4), (3, 7), (9, 10), (14, 15), (9, 13)])
    fill_variables()
    output()

    pygame.display.flip()

    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False


if __name__ == '__main__':
    main()
