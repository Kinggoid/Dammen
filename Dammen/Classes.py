import pygame


class Damsteen:
    radius = 0
    rand = 0

    def __init__(self, positie_x, positie_y, team):
        self.positie = [positie_x, positie_y]
        if team == 'wit' or team == 'Wit':
            self.team = True
        else:
            self.team = False
        self.king = False  # Iedereen begint als een man (man = normale damsteen en koning = gepromoveerde damsteen)

    def promoveren(self):  # Als je een damsteen wilt promoveren
        self.king = True

    def nieuwe_positie(self, x, y):  # Als je een damsteen een nieuwe positie wil geven
        self.positie = [x, y]

    def draw_dam(self, scherm, plaats_vakje):  # Zo ziet de man eruit
        zwart = (0, 0, 0)
        zwart_rand = (128, 128, 128)
        wit_stuk = (250, 250, 250)

        if self.team:
            pygame.draw.circle(scherm, wit_stuk, plaats_vakje, self.radius)
        else:
            pygame.draw.circle(scherm, zwart, plaats_vakje, self.radius)
        pygame.draw.circle(scherm, zwart_rand, plaats_vakje, self.radius, self.rand)

    def draw_king(self, scherm, plaats_vakje):  # Dit is hoe mijn koningen eruit zien
        zwart = (0, 0, 0)
        zwart_rand = (128, 128, 128)
        wit_stuk = (250, 250, 250)
        goud = (255, 215, 0)

        if self.team:
            pygame.draw.circle(scherm, wit_stuk, plaats_vakje, self.radius)
        else:
            pygame.draw.circle(scherm, zwart, plaats_vakje, self.radius)
        pygame.draw.circle(scherm, zwart_rand, plaats_vakje, self.radius, self.rand)
        pygame.draw.circle(scherm, goud, plaats_vakje, int(self.radius // 3))
        pygame.draw.circle(scherm, goud, plaats_vakje, int(self.radius // 1.5), int(self.rand // 1.5))


def setup():  # Maakt het bord
    spelbord = []
    for row in range(8):
        spelbord.append([0]*8)
    return spelbord


def stukken(spelbord):  # Maakt alle damstukken aan en zet ze in het bord
    w1 = Damsteen(1, 0, 'wit')
    w2 = Damsteen(3, 0, 'wit')
    w3 = Damsteen(5, 0, 'wit')
    w4 = Damsteen(7, 0, 'wit')
    w5 = Damsteen(0, 1, 'wit')
    w6 = Damsteen(2, 1, 'wit')
    w7 = Damsteen(4, 1, 'wit')
    w8 = Damsteen(6, 1, 'wit')
    w9 = Damsteen(1, 2, 'wit')
    w10 = Damsteen(3, 2, 'wit')
    w11 = Damsteen(5, 2, 'wit')
    w12 = Damsteen(7, 2, 'wit')

    z1 = Damsteen(0, 7, 'zwart')
    z2 = Damsteen(2, 7, 'zwart')
    z3 = Damsteen(4, 7, 'zwart')
    z4 = Damsteen(6, 7, 'zwart')
    z5 = Damsteen(1, 6, 'zwart')
    z6 = Damsteen(3, 6, 'zwart')
    z7 = Damsteen(5, 6, 'zwart')
    z8 = Damsteen(7, 6, 'zwart')
    z9 = Damsteen(0, 5, 'zwart')
    z10 = Damsteen(2, 5, 'zwart')
    z11 = Damsteen(4, 5, 'zwart')
    z12 = Damsteen(6, 5, 'zwart')

    alle_stenen = [w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, z1, z2, z3, z4, z5, z6, z7, z8, z9, z10, z11, z12]
    posities = []

    for steen in alle_stenen:  # Pakt van elke steen zijn positie
        posities.append(steen.positie)

    for i in range(0, len(posities)):  # Zet alle stenen op het bord
        spelbord[posities[i][1]][posities[i][0]] = alle_stenen[i]
    return alle_stenen


def draw_board(board, scherm, lengte_vakje, hoogte_vakje):  # Hier tekenen we het bord
    zwart = (0, 0, 0)
    wit = (220, 220, 220)

    for i in range(0, 8):
        for j in range(0, 8):
            if (i + j) % 2 == 0:  # Formule om te kijken of we een zwart of een wit vakje willen
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
    if len(board) >= y + 1:
        if len(board[y]) >= x + 1:
            if board[y][x] == 0:
                return True
    return False


def opDiagonaal(stuk, x, y):
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


def watKanJeZetten(stukken, beurt):
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
                if opDiagonaal(i, rechts_opzij, een_vooruit):
                    alle_zetten.append([rechts_opzij, een_vooruit])
            if 0 <= links_opzij <= 7:
                if opDiagonaal(i, links_opzij, een_vooruit):
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
        if i.king:
            return True
        positie = i.positie
        een_vooruit = positie[1] + vooruit
        links_opzij = positie[0] - 1
        rechts_opzij = positie[0] + 1

        if 0 <= een_vooruit <= 7:
            if 0 <= rechts_opzij <= 7:
                if board[een_vooruit][links_opzij] == 0 and opDiagonaal(i, rechts_opzij, een_vooruit):
                    return True
            if 0 <= links_opzij <= 7:
                if board[een_vooruit][rechts_opzij] == 0 and opDiagonaal(i, links_opzij, een_vooruit):
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

    alle_mogelijke_posities = []
    niet_springen = []
    wel_springen = [stuk]

    for i in [-1, 1]:
        for j in [-1, 1]:
            een_diagonaal = []
            x = stuk.positie[0]
            y = stuk.positie[1]
            stukken = 0
            while True:
                x += i
                y += j
                if 0 <= x <= 7 and 0 <= y <= 7:
                    vak = board[y][x]
                    if vak != 0:
                        if vak.team == team:
                            break
                        else:
                            stukken += 1
                            if stukken == 2:
                                een_diagonaal.remove(een_diagonaal[-1])
                                break
                            een_diagonaal.append([y, x])
                    else:
                        een_diagonaal.append([y, x])
                else:
                    break
            alle_mogelijke_posities.append(een_diagonaal)

    for diagonaal in alle_mogelijke_posities:
        sprong_mogelijk = 0
        diagonal = []
        for positie in diagonaal:
            vak = board[positie[0]][positie[1]]
            if vak != 0:
                sprong_mogelijk += 1
            if sprong_mogelijk == 0:
                niet_springen.append(positie)
            elif sprong_mogelijk == 1:
                diagonal.append(positie)
            else:
                break
        if diagonal and len(diagonal) > 1:
            wel_springen.append(diagonal)

    if len(wel_springen) > 1:
        return wel_springen
    else:
        return niet_springen


def diagonaalKoningSpringen(board, posities):
    stuk = posities[0]
    mogelijke_posities = [stuk, [posities[1][0]]]
    coordinaten = []
    for i in stuk.positie:
        coordinaten.append(i)

    y = board[posities[1][0][0]][posities[1][0][1]]
    board[posities[1][0][0]][posities[1][0][1]] = 0
    for i in range(1, len(posities[1])):
        board[posities[1][i][0]][posities[1][i][1]] = stuk
        stuk.positie[0] = posities[1][i][1]
        stuk.positie[1] = posities[1][i][0]

        x = koningStappen(board, stuk)
        if type(x[0]) != list:
            mogelijke_posities[1].append(posities[1][i])
        board[posities[1][i][0]][posities[1][i][1]] = 0

    stuk.positie = coordinaten
    board[posities[1][0][0]][posities[1][0][1]] = y

    if len(mogelijke_posities[1]) == 1:
        return posities
    return mogelijke_posities


def innerLoop():
    pygame.init()  # Begin de game
    board = setup()  # Zet het bord op
    pieces = stukken(board)  # Zet de stukken erop
    aantal_witte_stukken = 12
    aantal_zwarte_stukken = 12

    alleen_sprong = False  # Als een stuk na een sprong nog een keer moet springen gaat deze aan
    stuk_dat_moet_springen = 0  # Naam spreekt voor zich

    afmetingen = [700, 700]  # Hoe groot het scherm is
    breedte = afmetingen[0] // 8
    hoogte = afmetingen[1] // 8
    scherm = pygame.display.set_mode(afmetingen)

    pygame.display.set_caption("Dammen")

    clock = pygame.time.Clock()

    Damsteen.radius = afmetingen[0] // 20
    Damsteen.rand = afmetingen[1] // 150

    beurt = True  # Als beurt True is dan is wit aan de beurt

    game_over = 0
    while game_over == 0:
        for event in pygame.event.get():
            clock = pygame.time.Clock()

            if event.type == pygame.QUIT or einde(aantal_witte_stukken, aantal_zwarte_stukken):  # Als je wilt stoppen of als één kleur geen stukken meer over heeft
                game_over = True
                break

            if not watKanJeZetten(pieces, beurt):  # Als je stukken niet meer kunnen lopen
                if not watKanJeSpringen(board, pieces, beurt):  # En niks kunnen slaan
                    if beurt:
                        print('Zwart wint')
                    else:
                        print('Wit wint')
                    game_over = True
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:  # Als je ergens op klikt
                pos = pygame.mouse.get_pos()
                oud_x = pos[0] // breedte
                oud_y = pos[1] // hoogte
                begin_positie = board[oud_y][oud_x]  # begin_positie is de plek op het bord waar je op hebt geklikt

                if begin_positie == 0:  # Als je een leeg vak selecteerd breken we meteen af
                    break

                if stuk_dat_moet_springen != 0 and stuk_dat_moet_springen != begin_positie:  # Als we een steen hebben die moet springen
                    break

                if beurt % 2 == begin_positie.team:  # Als de gekozen damsteen de goede kleur is
                    while True:
                        event = pygame.event.wait()

                        if event.type == pygame.QUIT:
                            break

                        if event.type == pygame.MOUSEBUTTONUP:  # Hier laten we onze muis los
                            new_pos = pygame.mouse.get_pos()
                            new_x = new_pos[0] // breedte
                            new_y = new_pos[1] // hoogte

                            if not checkIfFriendly(board, new_x, new_y):  # Als het gekozen nieuwe vak al bezet is. Kan je daar niks plaatsen
                                break

                            if begin_positie.king:  # Als de damsteen een koning is
                                zetten = koningStappen(board, begin_positie)  # Dit zijn de zetten die je kan doen
                                if type(zetten[0]) != list:  # Als je een stuk kan pakken, is deze True
                                    zetten_voor_sprongen = diagonaalKoningSpringen(board, zetten)  # Checkt of nog iemand kan pakken
                                    if [new_y, new_x] in zetten_voor_sprongen[1]:
                                        begin_positie.nieuwe_positie(new_x, new_y)

                                        gesprongen_stuk = zetten_voor_sprongen[1][0]
                                        pieces.remove(board[gesprongen_stuk[0]][gesprongen_stuk[1]])

                                        board[new_y][new_x], board[oud_y][oud_x], board[gesprongen_stuk[0]][gesprongen_stuk[1]] = begin_positie, 0, 0  # Update het bord goed

                                        if begin_positie.team:
                                            aantal_zwarte_stukken -= 1
                                        else:
                                            aantal_witte_stukken -= 1

                                        if len(zetten_voor_sprongen[1]) != len(zetten[1]):  # Als we nog een keer een stuk kunnen pakken
                                            alleen_sprong = True
                                            stuk_dat_moet_springen = zetten_voor_sprongen[0]
                                        else:  # Anders draaien we de beurt om
                                            beurt = draaiDeBeurt(beurt)
                                        break
                                elif not alleen_sprong:  # Anders kan je je koning gewoon ergens naar verplaatsen
                                    if [new_y, new_x] in zetten:
                                        begin_positie.nieuwe_positie = new_x, new_y

                                        board[new_y][new_x], board[oud_y][oud_x] = begin_positie, 0
                                        beurt = draaiDeBeurt(beurt)
                                        break

                            else:
                                if not KanJeSpringen(board, pieces, beurt) and opDiagonaal(begin_positie, new_x, new_y):
                                    begin_positie.nieuwe_positie(new_x, new_y)

                                    board[new_y][new_x], board[oud_y][oud_x] = begin_positie, 0

                                    promoveer(begin_positie, alleen_sprong)

                                    beurt = draaiDeBeurt(beurt)
                                elif damPakken(board, begin_positie, new_x, new_y):
                                    pieces.remove(board[(new_y + begin_positie.positie[1]) // 2][(new_x + begin_positie.positie[0]) // 2])
                                    board[(new_y + begin_positie.positie[1]) // 2][(new_x + begin_positie.positie[0]) // 2] = 0

                                    begin_positie.nieuwe_positie(new_x, new_y)

                                    board[new_y][new_x], board[oud_y][oud_x] = begin_positie, 0

                                    if begin_positie.team:
                                        aantal_zwarte_stukken -= 1
                                    else:
                                        aantal_witte_stukken -= 1

                                    if nogEenKeerSpringen(board, begin_positie, False):
                                        alleen_sprong = True
                                        stuk_dat_moet_springen = begin_positie
                                        break

                                    alleen_sprong = False
                                    stuk_dat_moet_springen = 0
                                    promoveer(begin_positie, alleen_sprong)
                                    beurt = draaiDeBeurt(beurt)
                                break

            clock.tick(10)
            draw_board(board, scherm, breedte, hoogte)

            # Update screen with what we drew
            pygame.display.flip()



innerLoop()