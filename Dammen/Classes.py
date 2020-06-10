import pygame


class damsteen:
    def __init__(self, positie_x, positie_y, team):
        self.positie_x = positie_x
        self.positie_y = positie_y
        if team == 'wit' or team == 'Wit':
            self.team = True
        else:
            self.team = False
        self.king = False

    def promoveren(self):
        self.king = True


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
        posities.append([i.positie_x, i.positie_y])

    for i in range(0, len(posities)):
        if lst[i].team:
            spelbord[int(posities[i][0])][int(posities[i][1])] = 1
        else:
            spelbord[int(posities[i][0])][int(posities[i][1])] = 2


stukken(board)



def draw_board(board, scherm, lengte_vakje, hoogte_vakje, radius, rand):
    zwart = (0, 0, 0)
    zwart_rand = (128, 128, 128)
    wit_achtergrond = (150, 150, 150)
    wit_stuk = (250, 250, 250)
    goud = (255, 215, 0)

    kleur = 1

    for i in range(0, 8):
        for j in range(0, 8):
            if kleur == 1:
                kleur_van_vakje = wit_achtergrond
                kleur = 0
            else:
                kleur_van_vakje = zwart
                kleur = 1


            vakje = pygame.draw.rect(scherm, kleur_van_vakje, [lengte_vakje * j, hoogte_vakje * i, lengte_vakje, hoogte_vakje])
            plaats_vakje = vakje.center
            if board[i][j] == 1:
                pygame.draw.circle(scherm, wit_stuk, plaats_vakje, radius)
            if board[i][j] == 2:
                pygame.draw.circle(scherm, zwart, plaats_vakje, radius)
                pygame.draw.circle(scherm, zwart_rand, plaats_vakje, radius, rand)
        if kleur == 1:
            kleur = 0
        else:
            kleur = 1


def inner_loop():
    pygame.init()
    afmetingen = [900, 900]
    breedte = afmetingen[0] // 8
    hoogte = afmetingen[1] // 8
    scherm = pygame.display.set_mode(afmetingen)

    pygame.display.set_caption("Checkers")

    clock = pygame.time.Clock()

    white = [1, 3]
    black = [2, 4]

    game_over = 0
    while game_over == 0:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            mouse_matrix_pos = mouse_pos[0] // breedte, mouse_pos[1] // hoogte

            clock = pygame.time.Clock()
            clock.tick(10)
            draw_board(board, scherm, breedte, hoogte, afmetingen[0] // 20, afmetingen[1] // 200)
            pygame.display.flip()
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                old_x = (pos[0] // breedte)
                old_y = (pos[1] // hoogte)

                event = pygame.event.wait()
                if event.type == pygame.MOUSEBUTTONUP:
                    new_pos = pygame.mouse.get_pos()
                    new_x = (new_pos[0] // breedte)
                    new_y = (new_pos[1] // hoogte)
                    print(old_x, old_y, new_x, new_y)


inner_loop()
