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
    a1 = damsteen('0', '1', 'wit')

    lst = [a1]
    posities = []

    for i in lst:
        posities.append([i.positie_x, i.positie_y])

    for i in range(0, len(posities)):
        if lst[i].team:
            spelbord[int(posities[i][0])][int(posities[i][1])] = 1
        else:
            spelbord[int(posities[i][0])][int(posities[i][1])] = 2


stukken(board)



def draw_board(board, scherm, lengte_vakje, hoogte_vakje, radius, border):
    zwart_achtergrond = (0, 0, 0)
    wit_stuk = (250, 250, 250)
    wit_achtergrond = (150, 150, 150)
    zwart_stuk = (128, 128, 128)
    goud = (255, 215, 0)

    for i in range(0, 8):
        for j in range(0, 8):
            if (i + j) % 2 == 0:
                kleur_van_vakje = wit_achtergrond
            else:
                kleur_van_vakje = zwart_achtergrond

            vakje = pygame.draw.rect(scherm, kleur_van_vakje, [lengte_vakje * j, hoogte_vakje * i, lengte_vakje, hoogte_vakje])


def inner_loop():
    pygame.init()
    afmetingen = [600, 600]
    scherm = pygame.display.set_mode(afmetingen)

    pygame.display.set_caption("Checkers")

    clock = pygame.time.Clock()

    game_over = 0
    while game_over == 0:
        for event in pygame.event.get():
            print('lol')
            clock = pygame.time.Clock()
            clock.tick(10)
            draw_board(board, scherm, afmetingen[0] // 8, afmetingen[1] // 8, afmetingen[0] // 20, afmetingen[1] // 200)
            pygame.display.flip()
            if event.type == pygame.QUIT:
                game_over = True


inner_loop()
