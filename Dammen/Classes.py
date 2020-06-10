import pygame


class damsteen:
    radius = 0
    rand = 0

    def __init__(self, positie_x, positie_y, team):
        self.positie = [positie_y, positie_x]
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
    w1 = damsteen(0, 1, 'wit')
    z1 = damsteen(7, 6, 'zwart')

    lst = [w1, z1]
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


def checkIfFriendly(board, beurt, x, y):
    if board[y][x] == 0:
        return False
    elif board[y][x].team == beurt:
        return True
    else:
        return False


def damZetten(board, stuk, y, x):
    positie = stuk.positie
    if stuk.team:
        if positie[0] + 1 == y:
            if positie[1] + 1 == x or positie[1] - 1 == x:
                return True
    else:
        if positie[0] - 1 == y:
            if positie[1] + 1 == x or positie[1] - 1 == x:
                return True
    return False


def damPakken(board, stuk, x, y):
    all_moves = []
    team = stuk.team

    if board[y + 1][x - 1] == 0:
        pass
    elif board[y + 1][x - 1].team != team and board[y + 2][x - 2] == 0:
        all_moves.append([y + 2, x - 2])



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

    beurt = True

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

                while True:
                    old_x = pos[0] // breedte
                    old_y = pos[1] // hoogte
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        break

                    if event.type == pygame.MOUSEBUTTONUP:
                        new_pos = pygame.mouse.get_pos()
                        new_x = new_pos[0] // breedte
                        new_y = new_pos[1] // hoogte
                        friendly = checkIfFriendly(board, beurt, old_x, old_y)

                        if friendly:
                            if damZetten(board, board[old_y][old_x], new_x, new_y):
                                print('jep')
                                board[old_y][old_x].begin_x = new_x
                                board[old_y][old_x].begin_y = new_y

                                board[new_y][new_x], board[old_y][old_x] = board[old_y][old_x], 0

                                break


        clock.tick(10)
        draw_board(board, scherm, breedte, hoogte)

    # Update screen with what we drew
        pygame.display.flip()



inner_loop()
