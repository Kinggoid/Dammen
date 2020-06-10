import pygame


class damsteen:
    radius = 0
    rand = 0

    def __init__(self, positie_x, positie_y, team):
        self.positie = [positie_x, positie_y]
        if team == 'wit' or team == 'Wit':
            self.team = True
        else:
            self.team = False
        self.king = False

    def promoveren(self):
        self.king = True

    def draw(self, scherm, plaats_vakje):
        zwart = (0, 0, 0)
        zwart_rand = (128, 128, 128)
        wit_stuk = (250, 250, 250)

        if self.team:
            pygame.draw.circle(scherm, wit_stuk, plaats_vakje, self.radius)
        else:
            pygame.draw.circle(scherm, zwart, plaats_vakje, self.radius)
            pygame.draw.circle(scherm, zwart_rand, plaats_vakje, self.radius, self.rand)


def setup():
    totaalbord = []
    for row in range(8):
        totaalbord.append([0]*8)
    return totaalbord


board = setup()



def stukken(spelbord):
    w1 = damsteen(1, 0, 'wit')
    w2 = damsteen(0, 1, 'wit')
    z1 = damsteen(3, 2, 'zwart')
    z2 = damsteen(5, 2, 'zwart')

    lst = [w1, z1, z2, w2]
    posities = []

    for i in lst:
        posities.append(i.positie)

    for i in range(0, len(posities)):
        if lst[i].team:
            spelbord[int(posities[i][1])][int(posities[i][0])] = lst[i]
        else:
            spelbord[int(posities[i][1])][int(posities[i][0])] = lst[i]



def draw_board(board, scherm, lengte_vakje, hoogte_vakje):
    zwart = (0, 0, 0)
    wit_achtergrond = (150, 150, 150)

    for i in range(0, 8):
        for j in range(0, 8):
            if (i + j) % 2 == 0:
                kleur_van_vakje = wit_achtergrond
            else:
                kleur_van_vakje = zwart

            vakje = pygame.draw.rect(scherm, kleur_van_vakje, [lengte_vakje * j, hoogte_vakje * i, lengte_vakje, hoogte_vakje])
            stuk = board[i][j]
            if stuk != 0:
                stuk.draw(scherm, vakje.center)


def checkIfFriendly(board, x, y):
    if board[y][x] == 0:
        return True
    return False


def damZetten(board, stuk, x, y):
    positie = stuk.positie
    if stuk.team:
        if positie[1] + 1 == y:
            if positie[0] + 1 == x or positie[0] - 1 == x:
                return True
    else:
        if positie[1] - 1 == y:
            if positie[0] + 1 == x or positie[0] - 1 == x:
                return True
    return False


def damPakken(board, stuk, x, y):
    positie = stuk.positie
    team = stuk.team

    if positie[1] + 2 == y or positie[1] - 2 == y:
        if positie[0] + 2 == x or positie[0] - 2 == x:
            tussenPlek = board[(y + positie[1]) // 2][(x + positie[0]) // 2]
            if tussenPlek != 0:
                if tussenPlek.team != team:
                    return True
    return False



def inner_loop():
    pygame.init()
    stukken(board)
    afmetingen = [900, 900]
    breedte = afmetingen[0] // 8
    hoogte = afmetingen[1] // 8
    scherm = pygame.display.set_mode(afmetingen)

    pygame.display.set_caption("Checkers")

    clock = pygame.time.Clock()

    damsteen.radius = afmetingen[0] // 20
    damsteen.rand = afmetingen[1] // 150

    beurt = 1

    game_over = 0
    while game_over == 0:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            mouse_matrix_pos = mouse_pos[0] // breedte, mouse_pos[1] // hoogte

            clock = pygame.time.Clock()

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                print('hoi')
                pos = pygame.mouse.get_pos()
                old_x = pos[0] // breedte
                old_y = pos[1] // hoogte
                welkVak = board[old_y][old_x]

                if beurt % 2 == welkVak.team:
                    while True:
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            break

                        if event.type == pygame.MOUSEBUTTONUP:
                            new_pos = pygame.mouse.get_pos()
                            new_x = new_pos[0] // breedte
                            new_y = new_pos[1] // hoogte
                            friendly = checkIfFriendly(board, new_x, new_y)

                            if friendly:
                                if damZetten(board, welkVak, new_x, new_y):
                                    welkVak.positie[0] = new_x
                                    welkVak.positie[1] = new_y

                                    board[new_y][new_x], board[old_y][old_x] = welkVak, 0

                                    beurt += 1
                                    break
                                elif damPakken(board, welkVak, new_x, new_y):
                                    board[(new_y + welkVak.positie[1]) // 2][(new_x + welkVak.positie[0]) // 2] = 0

                                    welkVak.positie[0] = new_x
                                    welkVak.positie[1] = new_y

                                    board[new_y][new_x], board[old_y][old_x] = welkVak, 0

                                    beurt += 1
                                    break

            clock.tick(10)
            draw_board(board, scherm, breedte, hoogte)

            # Update screen with what we drew
            pygame.display.flip()



inner_loop()
