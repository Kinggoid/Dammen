import pygame


class damsteen:
    radius = 0
    rand = 0

    def __init__(self, begin_x, begin_y, team):
        self.begin_x = begin_x
        self.begin_y = begin_y
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
    w1 = damsteen('0', '1', 'wit')
    z1 = damsteen('7', '6', 'zwart')

    lst = [w1, z1]
    posities = []

    for i in lst:
        posities.append([i.begin_x, i.begin_y])

    for i in range(0, len(posities)):
        if lst[i].team:
            spelbord[int(posities[i][0])][int(posities[i][1])] = lst[i]
        else:
            spelbord[int(posities[i][0])][int(posities[i][1])] = lst[i]



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


def zetten(board, stuk, x, y):
    all_moves = []
    if stuk.team:
        if board[y + 1][x + 1] == 0:
            all_moves.append([y+1, x + 1])
        if board[y + 1][x - 1] == 0:
            all_moves.append([y + 1, x - 1])

    else:
        if board[y - 1][x + 1] == 0:
            all_moves.append([y - 1, x + 1])
        if board[y - 1][x - 1] == 0:
            all_moves.append([y - 1, x - 1])
    return all_moves


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
            draw_board(board, scherm, breedte, hoogte)
            pygame.display.flip()
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                print('hoi')
                pos = pygame.mouse.get_pos()
                old_x = pos[0] // breedte
                old_y = pos[1] // hoogte

                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        break

                    if event.type == pygame.MOUSEBUTTONUP:
                        new_pos = pygame.mouse.get_pos()
                        new_x = new_pos[0] // breedte
                        new_y = new_pos[1] // hoogte
                        friendly = checkIfFriendly(board, beurt, old_x, old_y)

                        if friendly:

                            moves = zetten(board, board[old_y][old_x], old_x, old_y)
                            print(moves)

                            if [new_y, new_x] in moves:
                                board[new_y][new_x], board[old_y][old_x] = board[old_y][old_x], 0

                            break


    clock.tick(10)
    draw_board(board, scherm, breedte, hoogte)

    # Update screen with what we drew
    pygame.display.flip()



inner_loop()
