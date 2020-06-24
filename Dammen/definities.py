import pygame
from Dammen.Damsteen import Damsteen

def setup():
    """
    In deze definitie maken we het bord. Ik maak een 8 x 8 bord omdat dat de meest populaire variant is.
    """
    spelbord = []
    for row in range(8):
        spelbord.append([0] * 8)
    return spelbord


def stukken(spelbord):
    """
    In deze definitie maken we alle damstenen aan en we zetten die vervolgens op het bord
    """
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


def draw_board(board, scherm, lengte_vakje, hoogte_vakje):
    """
    In deze definitie tekenen we het bord en de overblijvende stukken
    """
    zwart = (0, 0, 0)
    wit = (220, 220, 220)

    for i in range(0, 8):
        for j in range(0, 8):
            if (i + j) % 2 == 0:  # Formule om te kijken of we een zwart of een wit vakje willen
                kleur_van_vakje = wit
            else:
                kleur_van_vakje = zwart

            vakje = pygame.draw.rect(scherm, kleur_van_vakje, [lengte_vakje * j, hoogte_vakje * i, lengte_vakje,
                                                               hoogte_vakje])  # Teken het vakje
            stuk = board[i][j]
            if stuk != 0:  # Als er een damsteen op dit vakje staat dan gaan we die er ook op tekenen
                if stuk.king:
                    stuk.draw_king(scherm, vakje.center)
                else:
                    stuk.draw_dam(scherm, vakje.center)


def checkIfFriendly(board, x, y):
    """Kijkt of je gekozen vak wel binnen het bord valt en of je een leeg vak hebt geselecteerd"""
    if len(board) >= y + 1:
        if len(board[y]) >= x + 1:
            if board[y][x] == 0:
                return True
    return False


def einde(wit, zwart):
    """ In deze definitie kijken we of een kleur al zijn stukken is verloren. In dat geval heeft die kleur verloren"""
    if wit == 0 or zwart == 0:
        if wit == 0:
            return [True, False]
        else:
            return [True, True]
    else:
        return [False, False]


def juisteStukken(stukken, beurt):
    """ Deze definitie haalt alle stukken van dezelfde kleur uit de lijst en geeft dat terug."""
    juiste_kleur_stukken = []

    for i in stukken:
        if i.team == beurt:
            juiste_kleur_stukken.append(i)
    return juiste_kleur_stukken


def promoveer(stuk):
    """ Met deze definitie promoveren we een stuk."""
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
    wel_springen = []

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
                                break
                            een_diagonaal.append([y, x])
                    else:  # Als het een leeg vak is slaan we hem op
                        een_diagonaal.append([y, x])
                else:
                    break
            alle_mogelijke_posities.append(een_diagonaal)  # We slaan elk diagonaal op

    for diagonaal in alle_mogelijke_posities:
        # Als we in dit diagonaal een stuk van het andere team tegenkomen dan slaan we alleen de posities daarna op.
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

    if len(wel_springen) != 0:  # Als we een stuk kunnen pakken en minstens één plek hebben om op te landen
        return [stuk, wel_springen]
    else:
        return [0, niet_springen]  # Als we niks kunnen pakken dan krijgen we gewoon een lijst met mogelijke posities terug


def diagonaalKoningSpringen(board, posities):
    """In deze definitie kijken we of onze koning nog een keer kan slaan en op welke positie op zijn diagonaal hij kan
    landen om dit te doen."""
    stuk = posities[0]
    mogelijke_posities = [stuk, [], 0]

    for i in posities[1]:
        mogelijke_posities[1].append([i[0]])

    coordinaten = []
    kan_stuk_slaan = False

    for i in stuk.positie:  # We slaan de positie van het stuk op
        coordinaten.append(i)

    for i in range(0, len(mogelijke_posities[1])):
        diagonaal = posities[1][i]
        y = board[diagonaal[0][0]][diagonaal[0][1]]
        board[diagonaal[0][0]][diagonaal[0][1]] = 0
        for j in range(1, len(
                diagonaal)):  # Voor elke positie waar we kunnen komen, kijken we of we daarvan nog iemand kunnen slaan
            # Dit zou ons volgens de regels verplichten op dat vak te landen
            board[diagonaal[j][0]][diagonaal[j][1]] = stuk
            stuk.positie[0] = diagonaal[j][1]
            stuk.positie[1] = diagonaal[j][0]

            x = koningStappen(board, stuk)
            if x[0] != 0:
                kan_stuk_slaan = True
                mogelijke_posities[1][i].append(posities[1][i][j])
            board[diagonaal[j][0]][diagonaal[j][1]] = 0

        # Nu zetten we alles weer normaal=
        stuk.positie = coordinaten
        board[diagonaal[0][0]][diagonaal[0][1]] = y

    if kan_stuk_slaan:  # Lijst met posities als het stuk nog een keer kan slaan
        return mogelijke_posities
    return posities  # Waar hij anders naartoe kan


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
                    if team and y > positie[1] or not team and y < positie[
                        1]:  # Witte damstenen moeten schuin naar beneden en zwarte damstenen moeten de andere kant op
                        stap_vooruit_posities.append([y, x])
                elif position.team != team:  # Als er een man van het andere team naast onze man ligt dan kijken we of het vakje daarna leeg is.
                    y2 = y + i
                    x2 = x + j
                    if 0 <= x2 <= 7 and 0 <= y2 <= 7:
                        if checkIfFriendly(board, x2, y2):
                            sprong_posities.append([[y, x], [y2, x2]])

    if sprong_posities:  # Als we iets kunnen pakken, krijgen we zoiets: [[positie van de steen die je pakt, positie waar je terecht komt]] terug
        return sprong_posities
    return stap_vooruit_posities  # Anders een lijst met waar ze naartoe kunnen lopen


def herhaling(zetten):
    if zetten == 15:  # Volgens sommige regels is het gelijkspel als er 15 keer achter elkaar alleen maar met koningen wordt gespeeld.
        print('Er zijn te vaak koningstappen achter elkaar gemaakt. Het is gelijkspel')
        return True
    return False


def watKanJeZetten(board, stukken, beurt, kan_je_pakken):
    kan_je_nog_iets = 0
    alleen_sprong = 0
    stukken_die_iets_kunnen = []
    stukken_die_iets_kunnen_pakken = []
    alle_zetten = []
    zetten_van_stukken_die_kunnen_pakken = []

    for dam in stukken:  # Hier kijken we of de speler nog zetten heeft. Zo niet, dan wint de ander
        if dam.team == beurt:
            if dam.king:
                koningZet = koningStappen(board, dam)
                if len(koningZet[1]) != 0:
                    kan_je_nog_iets = 1
                    if not alleen_sprong:
                        stukken_die_iets_kunnen.append(dam)
                        alle_zetten.append(koningZet)
                    if type(koningZet[0]) != int:
                        alleen_sprong = True
                        if kan_je_pakken:
                            return alleen_sprong
                        stukken_die_iets_kunnen_pakken.append(dam)
                        zetten_van_stukken_die_kunnen_pakken.append(diagonaalKoningSpringen(board, koningZet))
            else:
                mogelijke_zetten = damZetten(board, dam)
                if mogelijke_zetten:
                    kan_je_nog_iets = 1
                    if not alleen_sprong:
                        stukken_die_iets_kunnen.append(dam)
                        alle_zetten.append(mogelijke_zetten)
                    if type(mogelijke_zetten[0][
                                0]) == list:  # Als een normale man kan springen dan gaat 'alleen_sprong' aan
                        alleen_sprong = True
                        if kan_je_pakken:
                            return alleen_sprong
                        stukken_die_iets_kunnen_pakken.append(dam)
                        zetten_van_stukken_die_kunnen_pakken.append(mogelijke_zetten)

    if kan_je_pakken:
        return False

    if kan_je_nog_iets == 0:
        if beurt:
            return [False, True, 0, 0]
        else:
            return [True, True, 0, 0]
    if alleen_sprong:
        return [alleen_sprong, False, stukken_die_iets_kunnen_pakken, zetten_van_stukken_die_kunnen_pakken]
    return [alleen_sprong, False, stukken_die_iets_kunnen, alle_zetten]

