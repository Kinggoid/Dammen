import pygame
import random
from Dammen.Damsteen import Damsteen
from Dammen import definities
from Dammen.AI import DamAI


def innerLoop():
    """
    Deze loop is waar de magie gebeurt. Aan het begin worden andere definities en dergelijke aangeroepen om het
    spel op te starten. Ook wordt er gevraagd of je tegen een ai wil spelen of tegen een ander persoon. Zodra het game
    over is, stopt het spel en gaan we de definitie uit.
    """
    computer_beurt = None

    while True:  # Hier zeg je wat je voor instellingen wil
        computer = input('Wil je tegen de computer spelen? Y/N: ')
        if computer == 'N' or computer == 'n':
            break
        elif computer == 'Y' or computer == 'y':
            while True:
                difficulty = input('Op welke moeilijkheidsgraad wil je spelen? easy/medium/hard: ')
                if difficulty == 'easy':
                    moeilijkheidsgraad = 3
                    break
                elif difficulty == 'medium':
                    moeilijkheidsgraad = 5
                    break
                elif difficulty == 'hard':
                    moeilijkheidsgraad = 7
                    break
            while computer_beurt == None:
                voorkeur = input('Als welke kleur wil je beginnen?: wit/zwart/geen voorkeur: ')
                if voorkeur == 'wit' or voorkeur == 'Wit':
                    computer_beurt = False
                elif voorkeur == 'zwart' or voorkeur == 'Zwart':
                    computer_beurt = True
                elif voorkeur == 'geen voorkeur' or voorkeur == 'Geen voorkeur':
                    computer_beurt = random.choice([False, True])
            break

    pygame.init()  # Begin de game
    pygame.display.set_caption("Dammen")

    board = definities.setup()  # Zet het bord op
    pieces = definities.stukken(board)  # Zet de stukken erop
    aantal_witte_stukken = 12
    aantal_zwarte_stukken = 12

    aantal_koning_zetten = 0  # Hoe vaak de koningen achter elkaar hebben bewogen

    stuk_dat_moet_springen = 0  # Wanneer een stuk de vorige ronde heeft gesprongen maar nog een keer moet springen, wordt hier zijn naam opgeslagen
                                # Om te garanderen dat dat stuk nu nog een keer slaat.

    afmetingen = [700, 700]  # Hoe groot het scherm is
    breedte = afmetingen[0] // 8
    hoogte = afmetingen[1] // 8
    scherm = pygame.display.set_mode(afmetingen)

    Damsteen.radius = afmetingen[0] // 20
    Damsteen.rand = afmetingen[1] // 150

    ai = DamAI()  # Hier wordt de ai gemaakt

    beurt = True  # Als beurt True is dan is wit aan de beurt

    game_over = 0
    while game_over == 0:
        if computer_beurt is None or beurt != computer_beurt:  # Als een menselijke speler aan de beurt is, dan gaan we verder
            for event in pygame.event.get():
                clock = pygame.time.Clock()

                if event.type == pygame.QUIT:  # Als je wilt stoppen of als één kleur geen stukken meer over heeft
                    game_over = 1
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:  # Als je ergens op klikt
                    pos = pygame.mouse.get_pos()
                    oud_x = pos[0] // breedte
                    oud_y = pos[1] // hoogte
                    begin_positie = board[oud_y][oud_x]  # begin_positie is de plek op het bord waar je op hebt geklikt

                    if begin_positie == 0:  # Als je een leeg vak selecteerd breken we meteen af
                        break

                    if beurt % 2 == begin_positie.team:  # Als de gekozen damsteen van het goede team is
                        while True:
                            event = pygame.event.wait()

                            alleen_sprong, game_over, stukken_die_kunnen_bewegen, hun_zetten = definities.watKanJeZetten(board, pieces, beurt, False)

                            if game_over:
                                # Deze game over komt van de definitie 'watKanJeZetten'. Daarin kijken we ook of je wel een enkele zet hebt die je kan doen.
                                # Zo niet, dan is het game_over en wint het andere team
                                if alleen_sprong:
                                    print('Wit wint')
                                else:
                                    print('Zwart wint')
                                game_over = 1
                                break

                            if event.type == pygame.QUIT:
                                game_over = 1
                                break

                            if event.type == pygame.MOUSEBUTTONUP:  # Hier laten we onze muis los
                                new_pos = pygame.mouse.get_pos()
                                new_x = new_pos[0] // breedte
                                new_y = new_pos[1] // hoogte

                                if not definities.checkIfFriendly(board, new_x, new_y):
                                    # Als het gekozen nieuwe vak al bezet is. Kan je daar niks plaatsen en mag je opnieuw kiezen
                                    break

                                if begin_positie not in stukken_die_kunnen_bewegen:
                                    # Als ons gekozen stuk niet kan bewegen, is het beter om dat stuk niet te selecteren
                                    break

                                if stuk_dat_moet_springen != 0 and stuk_dat_moet_springen != begin_positie:
                                    # Als we een steen hebben die moet springen, maar niet springt, mag je opnieuw kiezen
                                    break

                                zetten = hun_zetten[stukken_die_kunnen_bewegen.index(begin_positie)]

                                if begin_positie.king:  # Als de damsteen een koning is
                                    aantal_koning_zetten += 1
                                    if alleen_sprong:  # Als je een stuk kan pakken, is deze True
                                        for richting in zetten[1]:
                                            if [new_y, new_x] in richting[1:]:
                                                # Als onze zet kan veranderen we de nodige dingen om deze te verwerken
                                                begin_positie.nieuwe_positie(new_x, new_y)

                                                gesprongen_stuk = richting[0]
                                                pieces.remove(board[gesprongen_stuk[0]][gesprongen_stuk[1]])

                                                board[new_y][new_x], board[oud_y][oud_x], board[gesprongen_stuk[0]][gesprongen_stuk[1]] = begin_positie, 0, 0  # Update het bord

                                                aantal_witte_stukken, aantal_zwarte_stukken = definities.stukkenBijhouden(
                                                    aantal_witte_stukken, aantal_zwarte_stukken, begin_positie)  # Houdt het aantal zwarte en witte stukken bij

                                                if type(zetten[-1]) == int:  # Als we nog een keer een stuk kunnen pakken, willen we volgende ronde ook met dat stuk springen.
                                                    stuk_dat_moet_springen = zetten[0]
                                                else:  # Anders draaien we de beurt om
                                                    definities.promoveer(begin_positie)
                                                    stuk_dat_moet_springen = 0
                                                    beurt = not beurt

                                    else:  # Anders kan je je koning gewoon ergens naar verplaatsen
                                        if [new_y, new_x] in zetten[1]:
                                            begin_positie.nieuwe_positie(new_x, new_y)

                                            board[new_y][new_x], board[oud_y][oud_x] = begin_positie, 0
                                            definities.promoveer(begin_positie)
                                            beurt = not beurt

                                else:  # Als je hier komt heb je een normale damsteen geselecteerd
                                    aantal_koning_zetten = 0
                                    if alleen_sprong:  # Als je iets kan pakken
                                        for diagonaal in range(0, len(zetten)):
                                            positie = zetten[diagonaal]
                                            if [new_y, new_x] == positie[1]:
                                                begin_positie.nieuwe_positie(new_x, new_y)

                                                te_verwijderen_stuk_positie = positie[0]

                                                pieces.remove(board[te_verwijderen_stuk_positie[0]][
                                                                  te_verwijderen_stuk_positie[1]])

                                                aantal_witte_stukken, aantal_zwarte_stukken = definities.stukkenBijhouden(
                                                    aantal_witte_stukken, aantal_zwarte_stukken, begin_positie)  # Houdt het aantal zwarte en witte stukken bij

                                                board[new_y][new_x], board[oud_y][oud_x], \
                                                board[te_verwijderen_stuk_positie[0]][
                                                    te_verwijderen_stuk_positie[1]] = begin_positie, 0, 0  # Houdt het bord bij

                                                volgende_sprong = definities.damZetten(board,
                                                                            begin_positie)  # We kijken of het stuk nog een keer kan springen

                                                if volgende_sprong:
                                                    if type(volgende_sprong[0][0]) == list:  # Als hij nog een keer kan springen slaan dat stuk op:
                                                        stuk_dat_moet_springen = begin_positie
                                                    else:  # Anders gaan we door
                                                        stuk_dat_moet_springen = 0
                                                        definities.promoveer(begin_positie)
                                                        beurt = not beurt

                                                else:  # Anders gaan we door
                                                    stuk_dat_moet_springen = 0
                                                    definities.promoveer(begin_positie)
                                                    beurt = not beurt

                                    else:  # Als je niks kan pakken en alleen kan zetten
                                        if [new_y, new_x] in zetten:
                                            begin_positie.nieuwe_positie(new_x, new_y)

                                            board[new_y][new_x], board[oud_y][oud_x] = begin_positie, 0

                                            definities.promoveer(begin_positie)
                                            beurt = not beurt

                                eind = definities.einde(aantal_witte_stukken, aantal_zwarte_stukken)
                                if eind[0]:  # We kijken of je zojuist alle stukken van het andere team hebt gepakt.
                                    # Zo ja? Dan win je!
                                    if eind[1]:
                                        print('wit wint')
                                    else:
                                        print('zwart wint')
                                    game_over = 1
                                    break

                                if definities.herhaling(aantal_koning_zetten):
                                    # Checkt of je niet zojuist de 15e koning zet achter elkaar hebt gezet. Anders is het gelijkspel.
                                    game_over = 1
                                break

                clock.tick(10)  # Frames per second
                definities.draw_board(board, scherm, breedte, hoogte)  # We tekenen het nieuwe bord
                pygame.display.flip()  # We updaten het scherm

        else:  # Als de computer aan zet is
            kan_je_iets = definities.watKanJeZetten(board, pieces, beurt, False)
            if kan_je_iets[1]:  # Als de ai zijn stukken niet meer kan bewegen dan heb jij gewonnen!
                if kan_je_iets[0]:
                    print('Wit wint')
                else:
                    print('Zwart wint')
                break


            # Hieronder sturen we informatie naar een andere file waar de ai berekent wat de beste zet is.
            # Hij update voor ons al het bord, de positie van het stuk en nog een paar andere dingen.
            ai.upToDate(board, pieces, beurt, moeilijkheidsgraad, aantal_witte_stukken, aantal_zwarte_stukken,
                         stuk_dat_moet_springen, aantal_koning_zetten)

            board, stuk_dat_moet_springen, beurt, [aantal_witte_stukken, aantal_zwarte_stukken], pieces, stuk = \
                ai.AIzet()

            if stuk.king:
                aantal_koning_zetten += 1

            if stuk_dat_moet_springen == 0:
                # Als een stuk nog een keer kan springen maar als op de koningsrij zit, mag hij nog niet gepromoveerd worden.
                definities.promoveer(stuk)

            definities.draw_board(board, scherm, breedte, hoogte)  # We tekenen het nieuwe bord
            pygame.display.flip()  # We updaten het scherm

            eind = definities.einde(aantal_witte_stukken, aantal_zwarte_stukken)
            if eind[0]:  # Als de ai zojuist al jouw stukken heeft gepakt, dan heeft hij gewonnen.
                if eind[1]:
                    print('wit wint')
                else:
                    print('zwart wint')
                break

            if definities.herhaling(aantal_koning_zetten):  # En als hij de 15e koning zet heeft gezet is het gelijkspel.
                break
