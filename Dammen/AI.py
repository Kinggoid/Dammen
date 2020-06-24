from Dammen import definities
import random


def bijwerkenAI(board, stuk, beurt, nieuwe_plek, aangeraden_zet, pieces, aantal_witte_stukken, aantal_zwarte_stukken):
    if aangeraden_zet[-1] == 1:
        board[nieuwe_plek[0]][nieuwe_plek[1]], board[stuk.positie[1]][stuk.positie[0]] = stuk, 0
        stuk.nieuwe_positie(nieuwe_plek[1], nieuwe_plek[0])
        beurt = not beurt
        stuk_dat_moet_springen = 0


    elif aangeraden_zet[-1] == 2:
        pieces.remove(board[nieuwe_plek[0][0]][nieuwe_plek[0][1]])
        board[nieuwe_plek[1][0]][nieuwe_plek[1][1]], board[nieuwe_plek[0][0]][nieuwe_plek[0][1]], \
        board[stuk.positie[1]][stuk.positie[0]] = stuk, 0, 0
        stuk.nieuwe_positie(nieuwe_plek[1][1], nieuwe_plek[1][0])

        aantal_witte_stukken, aantal_zwarte_stukken = definities.stukkenBijhouden(
            aantal_witte_stukken, aantal_zwarte_stukken, stuk)

        if stuk.king:
            nog_een_sprong = definities.koningStappen(board, stuk)
        else:
            nog_een_sprong = definities.damZetten(board, stuk)

        if nog_een_sprong:
            if stuk.king:
                if type(nog_een_sprong[0]) == int:
                    beurt = not beurt
                    stuk_dat_moet_springen = 0
                else:
                    stuk_dat_moet_springen = stuk
            else:
                if not type(nog_een_sprong[0][0]) == list:
                    beurt = not beurt
                    stuk_dat_moet_springen = 0
                else:
                    stuk_dat_moet_springen = stuk
        else:
            beurt = not beurt
            stuk_dat_moet_springen = 0

    return [board, stuk_dat_moet_springen, beurt, [aantal_witte_stukken, aantal_zwarte_stukken], pieces, stuk]


def gameStaat(stukken, beurt, beurt_van_het_hoogste_niveau):
    punten_wit = 0
    punten_zwart = 0

    vakken_waarde_wit = [[0, 1.1, 0, 1.1, 0, 1.1, 0, 1.2], [1.2, 0, 1.2, 0, 1.2, 0, 1.2, 0], [0, 1.3, 0, 1.3, 0, 1.3, 0, 1.4],
                         [1.4, 0, 1.2, 0, 1.1, 0, 1.2, 0], [0, 1.2, 0, 1.1, 0, 1.2, 0, 1.4], [1.4, 0, 1.3, 0, 1.3, 0, 1.3, 0],
                         [0, 1.3, 0, 1.3, 0, 1.3, 0, 1.4], [1.4, 0, 1.4, 0, 1.4, 0, 1.4, 0]]
    vakken_waarde_zwart = [[1.4, 0, 1.4, 0, 1.4, 0, 1.4, 0], [0, 1.3, 0, 1.3, 0, 1.3, 0, 1.4], [1.4, 0, 1.3, 0, 1.3, 0, 1.3, 0],
                         [0, 1.2, 0, 1.1, 0, 1.2, 0, 1.4], [1.4, 0, 1.2, 0, 1.1, 0, 1.2, 0], [0, 1.3, 0, 1.3, 0, 1.3, 0, 1.4],
                         [1.2, 0, 1.2, 0, 1.2, 0, 1.2, 0], [0, 1.1, 0, 1.1, 0, 1.1, 0, 1.2]]

    for stuk in stukken:
        if stuk.team:
            punten_wit += (stuk.waarde * vakken_waarde_wit[stuk.positie[1]][stuk.positie[0]])
        else:
            punten_zwart += (stuk.waarde * vakken_waarde_zwart[stuk.positie[1]][stuk.positie[0]])

    if beurt == beurt_van_het_hoogste_niveau:
        if beurt:
            return punten_wit - punten_zwart
        return punten_zwart - punten_wit
    else:
        if beurt:
            return punten_zwart - punten_wit
        return punten_wit - punten_zwart


def eindnode(game_over, alleen_sprong, aantal_stukken, beurt):
    eind = definities.einde(aantal_stukken[0], aantal_stukken[1])
    if eind[0]:
        if eind[1]:
            return [100]
        else:
            return [-100]

    if game_over:
        if alleen_sprong == beurt:
            return [100]
        else:
            return [-100]
    return 0


def besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, soort_zet):
    if diepte == total_depth and new_value[0] > hoogste_waarde:
        return [new_value[0], soort_zet, [stuk, richting]]
    elif new_value[0] > hoogste_waarde:
        return [new_value[0], soort_zet]
    elif diepte == total_depth and new_value[0] == hoogste_waarde:
        if random.randint(0, 1) == 0:
            return [new_value[0], soort_zet, [stuk, richting]]
        else:
            return 0
    else:
        return 0


def miniMax(diepte, stukken, beurt, board, aantal_stukken, stuk_dat_moet_springen, total_depth, hoogste_beurt,
            koning_zetten):
    alleen_sprong, game_over, stukken_die_kunnen_bewegen, hun_zetten = definities.watKanJeZetten(board, stukken, beurt,
                                                                                              False)

    winst_of_verlies = eindnode(game_over, alleen_sprong, aantal_stukken, beurt)
    if winst_of_verlies != False:
        return winst_of_verlies

    if diepte == 0:
        if definities.herhaling(koning_zetten):
            return [-50]
        return [gameStaat(stukken, beurt, hoogste_beurt)]

    if stuk_dat_moet_springen != 0:
        hun_zetten = [hun_zetten[stukken_die_kunnen_bewegen.index(stuk_dat_moet_springen)]]
        stukken_die_kunnen_bewegen = [stuk_dat_moet_springen]

    hoogste_waarde = -200
    beste_zet = 0
    wat_voor_zet = 0

    new_board = []

    for i in board:
        new_board.append(i.copy())

    for i in range(0, len(stukken_die_kunnen_bewegen)):
        stuk = stukken_die_kunnen_bewegen[i]
        soort_stuk = stuk.king
        positie_van_stuk = stuk.positie.copy()

        if stuk.king:  # Als de damsteen een koning is
            new_koning_zetten = koning_zetten + 1
            if alleen_sprong:
                for richting in hun_zetten[i][1]:
                    new_stukken = stukken.copy()
                    new_new_board = []
                    for u in new_board:
                        new_new_board.append(u.copy())

                    new_stukken.remove(new_new_board[richting[0][0]][richting[0][1]])
                    new_new_board[richting[1][0]][richting[1][1]], new_new_board[stuk.positie[1]][stuk.positie[0]], \
                    new_new_board[richting[0][0]][richting[0][1]] = stuk, 0, 0
                    stuk.nieuwe_positie(richting[1][1], richting[1][0])

                    nog_een_sprong = definities.koningStappen(new_new_board, stuk)

                    if len(nog_een_sprong) > 0:
                        if type(nog_een_sprong[0]) != int:
                            stuk_dat_moet_springen = stuk
                            new_value = miniMax(diepte - 1, new_stukken, beurt, new_new_board, aantal_stukken,
                                                stuk_dat_moet_springen, total_depth, hoogste_beurt, new_koning_zetten)
                        else:
                            definities.promoveer(stuk)
                            stuk_dat_moet_springen = 0
                            new_value = miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                                stuk_dat_moet_springen, total_depth, hoogste_beurt, new_koning_zetten)

                    else:
                        definities.promoveer(stuk)
                        stuk_dat_moet_springen = 0
                        new_value = miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                            stuk_dat_moet_springen, total_depth, hoogste_beurt, new_koning_zetten)

                    stuk.nieuwe_positie(positie_van_stuk[0], positie_van_stuk[1])
                    stuk.correcte_soort(soort_stuk)

                    betere_waarde = besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, 2)

                    if type(betere_waarde) == list:
                        hoogste_waarde, wat_voor_zet = betere_waarde[0], betere_waarde[1]
                        if len(betere_waarde) > 2:
                            beste_zet = betere_waarde[2]

            else:
                for richting in hun_zetten[i][1]:
                    new_stukken = stukken.copy()
                    new_new_board = []
                    for u in new_board:
                        new_new_board.append(u.copy())

                    stuk.nieuwe_positie(richting[1], richting[0])

                    stuk_dat_moet_springen = 0

                    new_new_board[richting[0]][richting[1]], new_new_board[stuk.positie[1]][stuk.positie[0]] = stuk, 0

                    new_value = miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                        stuk_dat_moet_springen, total_depth, hoogste_beurt, new_koning_zetten)

                    stuk.nieuwe_positie(positie_van_stuk[0], positie_van_stuk[1])

                    definities.promoveer(stuk)

                    betere_waarde = besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, 1)

                    if type(betere_waarde) == list:
                        hoogste_waarde, wat_voor_zet = betere_waarde[0], betere_waarde[1]
                        if len(betere_waarde) > 2:
                            beste_zet = betere_waarde[2]

        else:
            koning_zetten = 0
            if alleen_sprong:
                for richting in hun_zetten[i]:
                    new_stukken = stukken.copy()
                    new_new_board = []
                    for u in new_board:
                        new_new_board.append(u.copy())

                    new_stukken.remove(new_new_board[richting[0][0]][richting[0][1]])
                    new_new_board[richting[1][0]][richting[1][1]], new_new_board[stuk.positie[1]][stuk.positie[0]], \
                    new_new_board[richting[0][0]][richting[0][1]] = stuk, 0, 0
                    stuk.nieuwe_positie(richting[1][1], richting[1][0])
                    nog_een_sprong = definities.damZetten(new_new_board, stuk)

                    if len(nog_een_sprong) > 0:
                        if type(nog_een_sprong[0][0]) == list:
                            stuk_dat_moet_springen = stuk
                            new_value = miniMax(diepte - 1, new_stukken, beurt, new_new_board, aantal_stukken,
                                                stuk_dat_moet_springen, total_depth, hoogste_beurt, koning_zetten)
                        else:
                            definities.promoveer(stuk)
                            stuk_dat_moet_springen = 0
                            new_value = miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                                stuk_dat_moet_springen, total_depth, hoogste_beurt, koning_zetten)

                    else:
                        definities.promoveer(stuk)
                        stuk_dat_moet_springen = 0
                        new_value = miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                            stuk_dat_moet_springen, total_depth, hoogste_beurt, koning_zetten)

                    stuk.nieuwe_positie(positie_van_stuk[0], positie_van_stuk[1])
                    stuk.correcte_soort(soort_stuk)

                    betere_waarde = besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, 2)

                    if type(betere_waarde) == list:
                        hoogste_waarde, wat_voor_zet = betere_waarde[0], betere_waarde[1]
                        if len(betere_waarde) > 2:
                            beste_zet = betere_waarde[2]

            else:
                for richting in hun_zetten[i]:
                    new_stukken = stukken.copy()
                    new_new_board = []
                    for u in new_board:
                        new_new_board.append(u.copy())

                    stuk_dat_moet_springen = 0
                    new_new_board[richting[0]][richting[1]], new_new_board[stuk.positie[1]][stuk.positie[0]] = stuk, 0
                    stuk.nieuwe_positie(richting[1], richting[0])

                    new_value = miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                        stuk_dat_moet_springen, total_depth, hoogste_beurt, koning_zetten)

                    stuk.nieuwe_positie(positie_van_stuk[0], positie_van_stuk[1])

                    betere_waarde = besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, 1)

                    if type(betere_waarde) != int:
                        hoogste_waarde, wat_voor_zet = betere_waarde[0], betere_waarde[1]
                        if len(betere_waarde) > 2:
                            beste_zet = betere_waarde[2]

    return [hoogste_waarde, beste_zet, wat_voor_zet]


class DamAI:
    def __init__(self):
        pass

    def AIzet(self, board, pieces, beurt, moeilijkheidsgraad, wit, zwart, stuk_dat_moet_springen, aantal_koning_zetten):
        posities_van_de_stukken = []
        for i in pieces:
            posities_van_de_stukken.append(i.positie.copy())

        new_board = board.copy()
        if beurt:
            aangeraden_zet = miniMax(moeilijkheidsgraad, pieces, beurt, new_board,
                                     [wit, zwart],
                                     stuk_dat_moet_springen, moeilijkheidsgraad, beurt, aantal_koning_zetten)
        else:
            aangeraden_zet = miniMax(moeilijkheidsgraad, pieces, beurt, new_board,
                                     [zwart, wit],
                                     stuk_dat_moet_springen, moeilijkheidsgraad, beurt, aantal_koning_zetten)

        stuk = aangeraden_zet[1][0]
        nieuwe_plek = aangeraden_zet[1][1]

        return bijwerkenAI(board, stuk, beurt, nieuwe_plek, aangeraden_zet, pieces, wit, zwart)






