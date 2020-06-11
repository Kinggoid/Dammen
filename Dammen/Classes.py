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

    def draw_dam(self, scherm, plaats_vakje):
        zwart = (0, 0, 0)
        zwart_rand = (128, 128, 128)
        wit_stuk = (250, 250, 250)

        if self.team:
            pygame.draw.circle(scherm, wit_stuk, plaats_vakje, self.radius)
            pygame.draw.circle(scherm, zwart_rand, plaats_vakje, self.radius, self.rand)
        else:
            pygame.draw.circle(scherm, zwart, plaats_vakje, self.radius)
            pygame.draw.circle(scherm, zwart_rand, plaats_vakje, self.radius, self.rand)

    def draw_king(self, scherm, plaats_vakje):
        zwart = (0, 0, 0)
        zwart_rand = (128, 128, 128)
        wit_stuk = (250, 250, 250)
        goud = (255, 215, 0)

        if self.team:
            pygame.draw.circle(scherm, wit_stuk, plaats_vakje, self.radius)
            pygame.draw.circle(scherm, goud, plaats_vakje, int(self.radius // 3))
            pygame.draw.circle(scherm, goud, plaats_vakje, int(self.radius // 1.5), int(self.rand // 1.5))
            pygame.draw.circle(scherm, zwart_rand, plaats_vakje, self.radius, self.rand)
        else:
            pygame.draw.circle(scherm, zwart, plaats_vakje, self.radius)
            pygame.draw.circle(scherm, zwart_rand, plaats_vakje, self.radius, self.rand)
            pygame.draw.circle(scherm, goud, plaats_vakje, int(self.radius // 3))
            pygame.draw.circle(scherm, goud, plaats_vakje, int(self.radius // 1.5), int(self.rand // 1.5))


def setup():
    totaalbord = []
    for row in range(8):
        totaalbord.append([0]*8)
    return totaalbord


def stukken(spelbord):
    w1 = damsteen(1, 0, 'wit')
    w2 = damsteen(0, 1, 'wit')
    z1 = damsteen(6, 7, 'zwart')
    z2 = damsteen(4, 7, 'zwart')

    lst = [w1, z1, z2, w2]
    posities = []

    for i in lst:
        posities.append(i.positie)

    for i in range(0, len(posities)):
        if lst[i].team:
            spelbord[int(posities[i][1])][int(posities[i][0])] = lst[i]
        else:
            spelbord[int(posities[i][1])][int(posities[i][0])] = lst[i]
    return lst



def draw_board(board, scherm, lengte_vakje, hoogte_vakje):
    zwart = (0, 0, 0)
    wit = (220, 220, 220)

    for i in range(0, 8):
        for j in range(0, 8):
            if (i + j) % 2 == 0:
                kleur_van_vakje = wit
            else:
                kleur_van_vakje = zwart

            vakje = pygame.draw.rect(scherm, kleur_van_vakje, [lengte_vakje * j, hoogte_vakje * i, lengte_vakje, hoogte_vakje])
            stuk = board[i][j]
            if stuk != 0:
                if stuk.king:
                    stuk.draw_king(scherm, vakje.center)
                else:
                    stuk.draw_dam(scherm, vakje.center)


def checkIfFriendly(board, x, y):
    if board[y][x] == 0:
        return True
    return False


def damZetten(stuk, x, y):
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

    if 0 <= x <= 7 and 0 <= y <= 7:
        if positie[1] + 2 == y or positie[1] - 2 == y:
            if positie[0] + 2 == x or positie[0] - 2 == x:
                tussen_plek = board[(y + positie[1]) // 2][(x + positie[0]) // 2]
                if tussen_plek != 0:
                    if tussen_plek.team != team:
                        return True
    return False


def nogEenKeerSpringen(board, stuk, wil_je_een_lijst):
    positie = stuk.positie
    x_sprongen = ['positie[0] + 2', 'positie[0] - 2']
    y_sprongen = ['positie[1] + 2', 'positie[1] - 2']

    alle_sprongen = []

    for i in x_sprongen:
        for j in y_sprongen:
            x = eval(i)
            y = eval(j)
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == 0 and damPakken(board, stuk, x, y):
                    if wil_je_een_lijst:
                        alle_sprongen.append([x, y])
                    else:
                        return True
    if wil_je_een_lijst:
        return alle_sprongen
    return False


def draaiDeBeurt(beurt):
    if beurt:
        return False
    else:
        return True


def einde(wit, zwart):
    if wit == 0 or zwart == 0:
        if wit == 0:
            print('Zwart wint')
        else:
            print('Wit wint')
        return True
    else:
        return False


def juisteStukken(stukken, beurt):
    juiste_kleur_stukken = []

    for i in stukken:
        if i.team == beurt:
            juiste_kleur_stukken.append(i)
    return juiste_kleur_stukken


def watKanJeZetten(board, stukken, beurt):
    juiste_kleur_stukken = juisteStukken(stukken, beurt)
    alle_zetten = []

    team = juiste_kleur_stukken[0].team
    if team:
        vooruit = 1
    else:
        vooruit = -1

    for i in juiste_kleur_stukken:
        positie = i.positie
        een_vooruit = positie[1] + vooruit
        links_opzij = positie[0] - 1
        rechts_opzij = positie[0] + 1

        if 0 <= een_vooruit <= 7:
            if 0 <= rechts_opzij <= 7:
                if damZetten(i, rechts_opzij, een_vooruit):
                    alle_zetten.append([rechts_opzij, een_vooruit])
            if 0 <= links_opzij <= 7:
                if damZetten(i, links_opzij, een_vooruit):
                    alle_zetten.append([links_opzij, een_vooruit])
    return alle_zetten


def watKanJeSpringen(board, stukken, beurt):
    juiste_kleur_stukken = juisteStukken(stukken, beurt)
    alle_zetten = []

    for stuk in juiste_kleur_stukken:
        sprongen = nogEenKeerSpringen(board, stuk, True)
        for sprong in sprongen:
            alle_zetten.append(sprong)
    return alle_zetten


def KanJeZetten(board, stukken, beurt):
    juiste_kleur_stukken = juisteStukken(stukken, beurt)

    team = juiste_kleur_stukken[0].team
    if team:
        vooruit = 1
    else:
        vooruit = -1

    for i in juiste_kleur_stukken:
        positie = i.positie
        een_vooruit = positie[1] + vooruit
        links_opzij = positie[0] - 1
        rechts_opzij = positie[0] + 1

        if 0 <= een_vooruit <= 7:
            if 0 <= rechts_opzij <= 7:
                if board[een_vooruit][links_opzij] == 0 and damZetten(i, rechts_opzij, een_vooruit):
                    return True
            if 0 <= links_opzij <= 7:
                if board[een_vooruit][rechts_opzij] == 0 and damZetten(i, links_opzij, een_vooruit):
                    return True
    return False


def KanJeSpringen(board, stukken, beurt):
    juiste_kleur_stukken = juisteStukken(stukken, beurt)

    for stuk in juiste_kleur_stukken:
        sprongen = nogEenKeerSpringen(board, stuk, False)
        if sprongen:
            return True
    return False


def promoveer(stuk, springen):
    positie = stuk.positie
    if stuk.team:
        if positie[1] == 7 and not springen:
            stuk.promoveren()
    else:
        if positie[1] == 0 and not springen:
            stuk.promoveren()


def koningStappen(board, stuk):
    team = stuk.team
    x = stuk.positie[0]
    y = stuk.positie[1]

    alle_mogelijke_posities = []

    directions = [range(y + 1, 8), range(y + 1, 8), range(y - 1, -1, -1), range(y - 1, -1, -1)]
    directions_x = [range(x + 1, 8), range(x - 1, -1, -1), range(x + 1, 8), range(x - 1, -1, -1)]

    for i in directions:
        for j in i:
            if board:
                pass


    return alle_mogelijke_posities




def innerLoop():
    pygame.init()
    board = setup()
    pieces = stukken(board)
    aantal_witte_stukken = 2
    aantal_zwarte_stukken = 2

    alleen_sprong = False
    stuk_dat_moet_springen = 0

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

            clock = pygame.time.Clock()

            if event.type == pygame.QUIT:
                game_over = True

            if einde(aantal_witte_stukken, aantal_zwarte_stukken):
                game_over = True
                break

            if not watKanJeZetten(board, pieces, beurt):
                if not watKanJeSpringen(board, pieces, beurt):
                    if beurt:
                        print('Zwart wint')
                    else:
                        print('Wit wint')
                    game_over = True
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                print('hoi')
                pos = pygame.mouse.get_pos()
                old_x = pos[0] // breedte
                old_y = pos[1] // hoogte
                welkVak = board[old_y][old_x]

                if welkVak == 0:
                    break

                if stuk_dat_moet_springen != 0:
                    if stuk_dat_moet_springen != welkVak:
                        break

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

                            if not alleen_sprong:
                                if KanJeSpringen(board, pieces, beurt):
                                    alleen_sprong = True

                            if friendly:
                                if not alleen_sprong and damZetten(welkVak, new_x, new_y):
                                    welkVak.positie[0] = new_x
                                    welkVak.positie[1] = new_y

                                    board[new_y][new_x], board[old_y][old_x] = welkVak, 0

                                    promoveer(welkVak, alleen_sprong)

                                    beurt = draaiDeBeurt(beurt)
                                    break
                                elif damPakken(board, welkVak, new_x, new_y):
                                    board[(new_y + welkVak.positie[1]) // 2][(new_x + welkVak.positie[0]) // 2] = 0

                                    welkVak.positie[0] = new_x
                                    welkVak.positie[1] = new_y

                                    board[new_y][new_x], board[old_y][old_x] = welkVak, 0

                                    if welkVak.team:
                                        aantal_zwarte_stukken -= 1
                                    else:
                                        aantal_witte_stukken -= 1

                                    if nogEenKeerSpringen(board, welkVak, False):
                                        alleen_sprong = True
                                        stuk_dat_moet_springen = welkVak
                                        break

                                    alleen_sprong = False
                                    stuk_dat_moet_springen = 0
                                    promoveer(welkVak, alleen_sprong)
                                    beurt = draaiDeBeurt(beurt)
                                    break

            clock.tick(10)
            draw_board(board, scherm, breedte, hoogte)

            # Update screen with what we drew
            pygame.display.flip()



innerLoop()