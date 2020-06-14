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

            vakje = pygame.draw.rect(scherm, kleur_van_vakje,
                                     [lengte_vakje * j, hoogte_vakje * i, lengte_vakje, hoogte_vakje])
            stuk = board[i][j]
            if stuk != 0:
                if stuk.king:
                    stuk.draw_king(scherm, vakje.center)
                else:
                    stuk.draw_dam(scherm, vakje.center)


def checkIfFriendly(board, x,
                    y):  # Kijkt of je gekozen vak wel binnen het bord valt en of je een leeg vak hebt geselecteerd
    if len(board) >= y + 1:
        if len(board[y]) >= x + 1:
            if board[y][x] == 0:
                return True
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


def promoveer(stuk):
    positie = stuk.positie
    if stuk.team:
        if positie[1] == 7:
            stuk.promoveren()
    else:
        if positie[1] == 0:
            stuk.promoveren()


def koningStappen(board, stuk):
    """ Hier kijken we van een bepaalde koning of hij iemand kan pakken (dan krijg je het hele diagonaal daarachter mee.
    en anders waar hij met normale stappen naartoe kan gaan."""
    team = stuk.team

    alle_mogelijke_posities = []
    niet_springen = []
    wel_springen = [stuk]

    for i in [-1, 1]:  # Deze forloops gebruik ik om op elk diagonaal te kijken
        for j in [-1, 1]:
            een_diagonaal = []  # Op welke vakken kunnen we landen op dit diagonaal
            x = stuk.positie[0]
            y = stuk.positie[1]
            stukken = 0
            while True:
                x += i
                y += j
                # Elke ronde in de while loop kijken we steeds verder het diagonaal in
                if 0 <= x <= 7 and 0 <= y <= 7:  # Als we nog binnen het bord zitten
                    vak = board[y][x]
                    if vak != 0:
                        if vak.team == team:  # Als we ons eigen team tegenkomen kunnen we niet verder
                            break
                        else:  # Als we één keer een steen van het andere team tegenkomen slaan we deze op. Als we er twee op hetzelfde diagonaal vinden stoppen we met dit diagonaal
                            stukken += 1
                            if stukken == 2:
                                een_diagonaal.remove(een_diagonaal[-1])
                                break
                            een_diagonaal.append([y, x])
                    else:  # Als het een leeg vak is slaan we hem op
                        een_diagonaal.append([y, x])
                else:
                    break
            alle_mogelijke_posities.append(een_diagonaal)  # We slaan elk diagonaal op

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


def stukkenBijhouden(wit, zwart, stuk):
    """Als een stuk wordt gepakt gaat het aantal zwarte of witte stukken omlaag met 1"""
    if stuk.team:
        return [wit, zwart - 1]
    else:
        return [wit - 1, zwart]


def damZetten(board, stuk):
    """ Hier kijken we of een man een ander stuk kan pakken (en waar hij landt) en anders krijgen we een lijst met
    andere mogelijke zetten terug"""
    positie = stuk.positie
    team = stuk.team
    stap_vooruit_posities = []
    sprong_posities = []
    lst = [1, -1]

    for i in lst:  # Met deze for loopjes kijken we in elke (schuine) richting van het stuk
        for j in lst:
            y = positie[1] + i
            x = positie[0] + j
            if 0 <= x <= 7 and 0 <= y <= 7:  # Als het nog binnen het bord zit
                position = board[y][x]
                if position == 0:
                    if team and y > positie[1] or not team and y < positie[1]:  # Witte damstenen moeten schuin naar beneden en zwarte damstenen moeten de andere kant op
                        stap_vooruit_posities.append([y, x])
                elif position.team != team:  # Als er een man van het andere team naast onze man ligt dan kijken we of het vakje daarna leeg is.
                    y2 = y + i
                    x2 = x + j
                    if checkIfFriendly(board, x2, y2):
                        sprong_posities.append([[y, x], [y2, x2]])

    if sprong_posities:  # Als we iets kunnen pakken, krijgen we zoiets: [[positie van de steen die je pakt, positie waar je terecht komt]] terug
        return sprong_posities
    return stap_vooruit_posities  # Anders een lijst met waar ze naartoe kunnen lopen


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

                        kan_je_nog_iets = 0

                        for dam in pieces:  # Hier kijken we of de speler nog zetten heeft. Zo niet, dan wint de ander
                            if dam.team == beurt:
                                mogelijke_zetten = damZetten(board, dam)
                                if dam.king:
                                    if koningStappen(board, dam):
                                        kan_je_nog_iets = 1
                                if mogelijke_zetten:
                                    kan_je_nog_iets = 1
                                    if type(mogelijke_zetten[0][0]) == list:  # Als een normale man kan springen dan gaat 'alleen_sprong' aan
                                        alleen_sprong = True
                                        break

                        if kan_je_nog_iets == 0:
                            if beurt:
                                print('Zwart wint')
                            else:
                                print('Wit wint')
                            game_over = True
                            break

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
                                print(zetten)
                                if type(zetten[0]) != list:  # Als je een stuk kan pakken, is deze True
                                    zetten_voor_sprongen = diagonaalKoningSpringen(board, zetten)  # Checkt of nog iemand kan pakken
                                    if [new_y, new_x] in zetten_voor_sprongen[1]:  # Als onze zet kan veranderen we de nodige dingen om deze te verwerken
                                        begin_positie.nieuwe_positie(new_x, new_y)

                                        gesprongen_stuk = zetten_voor_sprongen[1][0]
                                        pieces.remove(board[gesprongen_stuk[0]][gesprongen_stuk[1]])

                                        board[new_y][new_x], board[oud_y][oud_x], board[gesprongen_stuk[0]][gesprongen_stuk[1]] = begin_positie, 0, 0  # Update het bord goed

                                        aantal_witte_stukken, aantal_zwarte_stukken = stukkenBijhouden(aantal_witte_stukken, aantal_zwarte_stukken, begin_positie)

                                        if len(zetten_voor_sprongen[1]) != len(zetten[1]):  # Als we nog een keer een stuk kunnen pakken
                                            alleen_sprong = True
                                            stuk_dat_moet_springen = zetten_voor_sprongen[0]
                                        else:  # Anders draaien we de beurt om
                                            promoveer(begin_positie)
                                            alleen_sprong = False
                                            stuk_dat_moet_springen = 0
                                            beurt = draaiDeBeurt(beurt)
                                        break

                                else:  # Anders kan je je koning gewoon ergens naar verplaatsen
                                    if [new_y, new_x] in zetten:
                                        begin_positie.nieuwe_positie(new_x, new_y)

                                        board[new_y][new_x], board[oud_y][oud_x] = begin_positie, 0
                                        promoveer(begin_positie)
                                        beurt = draaiDeBeurt(beurt)
                                        break

                            else:  # Als je hier komt heb je een normale damsteen geselecteerd
                                zetten = damZetten(board, begin_positie)
                                if type(zetten[0][0]) != list and not alleen_sprong:  # Als je niks kan pakken
                                    if [new_y, new_x] in zetten:
                                        begin_positie.nieuwe_positie(new_x, new_y)

                                        board[new_y][new_x], board[oud_y][oud_x] = begin_positie, 0
                                        promoveer(begin_positie)
                                        beurt = draaiDeBeurt(beurt)
                                    break
                                else:  # Als je iets kan pakken
                                    for diagonaal in range(0, len(zetten)):
                                        positie = zetten[diagonaal]
                                        if [new_y, new_x] == positie[1]:
                                            begin_positie.nieuwe_positie(new_x, new_y)

                                            te_verwijderen_stuk_positie = positie[0]

                                            pieces.remove(board[te_verwijderen_stuk_positie[0]][te_verwijderen_stuk_positie[1]])

                                            aantal_witte_stukken, aantal_zwarte_stukken = stukkenBijhouden(aantal_witte_stukken, aantal_zwarte_stukken, begin_positie)

                                            board[new_y][new_x], board[oud_y][oud_x], board[te_verwijderen_stuk_positie[0]][te_verwijderen_stuk_positie[1]] = begin_positie, 0, 0

                                            volgende_sprong = damZetten(board, begin_positie)  # We kijken of het stuk nog een keer kan springen

                                            if volgende_sprong:
                                                if type(volgende_sprong[0][0]) == list:  # Als hij nog een keer kan springen slaan we dat op
                                                    alleen_sprong = True
                                                    stuk_dat_moet_springen = begin_positie
                                                    break

                                            #  Anders gaan we door

                                            alleen_sprong = False
                                            stuk_dat_moet_springen = 0
                                            promoveer(begin_positie)
                                            beurt = draaiDeBeurt(beurt)
                                            break


            clock.tick(10)  # Frames per second
            draw_board(board, scherm, breedte, hoogte)  # We tekenen het nieuwe bord
            pygame.display.flip()  # We updaten het scherm


innerLoop()