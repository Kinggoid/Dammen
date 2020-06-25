from Dammen import definities
import random


class DamAI:
    def upToDate(self, board, pieces, beurt, moeilijkheidsgraad, wit, zwart, stuk_dat_moet_springen, aantal_koning_zetten):
        self.board = board
        self.pieces = pieces
        self.beurt = beurt
        self.moeilijkheidsgraad = moeilijkheidsgraad
        self.wit = wit
        self.zwart = zwart
        self.stuk_dat_moet_springen = stuk_dat_moet_springen
        self.aantal_koning_zetten = aantal_koning_zetten

    def bijwerkenAI(self, board, stuk, beurt, nieuwe_plek, aangeraden_zet, pieces, aantal_witte_stukken, aantal_zwarte_stukken):
        """
        In deze definitie werken we het bord en de positie van het stuk bij, gegeven dat de ai een zet heeft gemaakt.
        """
        if aangeraden_zet[-1] == 1:  # Als de ai een normale zet doet
            board[nieuwe_plek[0]][nieuwe_plek[1]], board[stuk.positie[1]][stuk.positie[0]] = stuk, 0
            stuk.nieuwe_positie(nieuwe_plek[1], nieuwe_plek[0])
            beurt = not beurt
            stuk_dat_moet_springen = 0

        elif aangeraden_zet[-1] == 2:  # Wanneer de ai iemand pakt
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

            if nog_een_sprong:  # We kijken of de ai met zijn nieuwe positie nog iemand kan pakken. Zo niet, dan gaan we door.
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


    def gameStaat(self, stukken, beurt, beurt_van_het_hoogste_niveau):
        """
        In deze definitie probeer ik te berekenen wat ongeveer de waarde van een positie is. Hiervoor geef ik waarde
        aan bepaalde vakken (vakken aan de zijkant en aan de overkant van het team zijn meer waard) op het bord. Ook
        hebben stukken van zichzelf een bepaalde waarde. Een damsteen is 1 punt en een koning is 6 punten. Deze twee
        factoren voeg ik samen en zo weeg ik af hoeveel een positie waard is.
        """
        punten_wit = 0
        punten_zwart = 0

        vakken_waarde_wit = [[0, 1.1, 0, 1.1, 0, 1.1, 0, 1.2], [1.2, 0, 1.2, 0, 1.2, 0, 1.2, 0],
                             [0, 1.3, 0, 1.3, 0, 1.3, 0, 1.4],
                             [1.4, 0, 1.2, 0, 1.1, 0, 1.2, 0], [0, 1.2, 0, 1.1, 0, 1.2, 0, 1.4],
                             [1.4, 0, 1.3, 0, 1.3, 0, 1.3, 0],
                             [0, 1.3, 0, 1.3, 0, 1.3, 0, 1.4], [1.4, 0, 1.4, 0, 1.4, 0, 1.4, 0]]
        # Waarde van de vakken van wit zijn perspectief
        vakken_waarde_zwart = [[0, 1.4, 0, 1.4, 0, 1.4, 0, 1.4], [1.4, 0, 1.3, 0, 1.3, 0, 1.3, 0],
                               [0, 1.3, 0, 1.3, 0, 1.3, 0, 1.4],
                               [1.4, 0, 1.2, 0, 1.1, 0, 1.3, 0], [0, 1.3, 0, 1.1, 0, 1.2, 0, 1.4],
                               [1.4, 0, 1.3, 0, 1.3, 0, 1.3, 0],
                               [0, 1.2, 0, 1.2, 0, 1.2, 0, 1.3], [1.1, 0, 1.1, 0, 1.1, 0, 1.1, 0]]
        # Waarde van de vakken van zwart zijn perspectief

        for stuk in stukken:  # Bereken de punten van elk team
            if stuk.team:
                punten_wit += (stuk.waarde * vakken_waarde_wit[stuk.positie[1]][stuk.positie[0]])
            else:
                punten_zwart += (stuk.waarde * vakken_waarde_zwart[stuk.positie[1]][stuk.positie[0]])

        if beurt == beurt_van_het_hoogste_niveau:  # Als de ai de kleur wit heeft, wil jij als zwart een zo laag mogelijke score hebben.
            if beurt:
                return punten_wit - punten_zwart
            return punten_zwart - punten_wit
        else:
            if beurt:
                return punten_zwart - punten_wit
            return punten_wit - punten_zwart

    def eindnode(self, game_over, alleen_sprong, aantal_stukken, beurt):
        """
        Deze definitie is ook voor de ai. Deze definitie kijkt of, in deze variatie, een team verloren of gewonnen
        heeft. Als je hebt gewonnen krijg je punten, anders verlies je punten.
        """
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

    def besteWaarde(self, diepte, total_depth, new_value, hoogste_waarde, stuk, richting, soort_zet):
        """
        In deze definitie kijken we of we met een bepaalde variatie een betere sequentie aan zetten hebben gevonden.
        Als we dezelfde waarde krijgen voor een eindstand, dan is er een gelijke kans welke we kiezen. Dit doe ik zodat
        je niet altijd precies dezelfde zetten van de ai krijgt. Zo blijft de ai zichzelf niet herhalen.
        """
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

    def miniMax(self, diepte, stukken, beurt, board, aantal_stukken, stuk_dat_moet_springen, total_depth, hoogste_beurt,
                koning_zetten):
        """
        Dit is het minimax algoritme. Hier krijgen we een bepaalde stand van een game binnen en dan proberen we de beste
        zet te vinden voor de ai. Dit doen we door een aantal stappen vooruit te kijken. Zo kunnen we zien dat het
        niet handig is om onze dam naar een bepaalde plek te zetten omdat de tegenstander deze gewoon kan pakken. Door
        zo elke situatie af te lopen komen we uiteindelijk met een zet waar we de best mogelijke toekomste positie voor
        ons hebben voorzien.
        """
        alleen_sprong, game_over, stukken_die_kunnen_bewegen, hun_zetten = definities.watKanJeZetten(board, stukken, beurt,
                                                                                                     False)

        winst_of_verlies = self.eindnode(game_over, alleen_sprong, aantal_stukken, beurt)
        if winst_of_verlies != False:  # Kijken of we wel nog stukken over hebben
            return winst_of_verlies

        if diepte == 0:
            # Als we bijvoorbeeld 3 stappen diep kunnen kijken, komen we op een gegeven moment bij diepte 0 aan.
            # Hier kijken we eerst of we niet voor de 15e keer met een koning hebben bewogen. Als dat niet het geval is
            # dan evalueren we de waarde van het bord en dat geven we mee aan hogere niveaus.
            if definities.herhaling(koning_zetten):
                return [-50]
            return [self.gameStaat(stukken, beurt, hoogste_beurt)]

        if stuk_dat_moet_springen != 0:
            # Als we een stuk hebben dat moet springen dan veranderen we de lijsten zo dat je alleen maar met dit stuk
            # Kan springen.
            hun_zetten = [hun_zetten[stukken_die_kunnen_bewegen.index(stuk_dat_moet_springen)]]
            stukken_die_kunnen_bewegen = [stuk_dat_moet_springen]

        hoogste_waarde = -200
        beste_zet = 0
        wat_voor_zet = 0

        new_board = []  # Maak een nieuw bord aan.

        for i in board:
            new_board.append(i.copy())

        for i in range(0, len(stukken_die_kunnen_bewegen)):  # Voor elk stuk dat zich kan bewegen van ons team in deze positie
            stuk = stukken_die_kunnen_bewegen[i]
            soort_stuk = stuk.king
            positie_van_stuk = stuk.positie.copy()

            if stuk.king:  # Als de damsteen een koning is
                new_koning_zetten = koning_zetten + 1
                if alleen_sprong:  # Als dit stuk iemand kan pakken
                    for richting in hun_zetten[i][1]:  # Elke zet die dit stuk kan doen.
                        new_stukken = stukken.copy()
                        new_new_board = []
                        for u in new_board:
                            new_new_board.append(u.copy())

                        # Nu veranderen we het bord zo dat het het een nieuw bord geeft alsof we die zet hebben gedaan.
                        new_stukken.remove(new_new_board[richting[0][0]][richting[0][1]])
                        new_new_board[richting[1][0]][richting[1][1]], new_new_board[stuk.positie[1]][stuk.positie[0]], \
                        new_new_board[richting[0][0]][richting[0][1]] = stuk, 0, 0
                        stuk.nieuwe_positie(richting[1][1], richting[1][0])

                        # Kan je nog een keer springen?
                        nog_een_sprong = definities.koningStappen(new_new_board, stuk)

                        if len(nog_een_sprong) > 0:
                            if type(nog_een_sprong[0]) != int:  # Zo ja? dat draaien we de beurt niet om en moet je nog eens met dit stuk springen.
                                # Ps. we kijken niet of het stuk kan promoveren want het is een regel dat je pas mag promoveren met een stuk als je niks kan slaan.
                                stuk_dat_moet_springen = stuk
                                new_value = self.miniMax(diepte - 1, new_stukken, beurt, new_new_board, aantal_stukken,
                                                    stuk_dat_moet_springen, total_depth, hoogste_beurt, new_koning_zetten)
                            else:  # Zo nee? Dan draaien we de beurt om en kijken we of het stuk een koning kan worden.
                                definities.promoveer(stuk)
                                stuk_dat_moet_springen = 0
                                new_value = self.miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                                    stuk_dat_moet_springen, total_depth, hoogste_beurt, new_koning_zetten)

                        else:
                            definities.promoveer(stuk)
                            stuk_dat_moet_springen = 0
                            new_value = self.miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                                stuk_dat_moet_springen, total_depth, hoogste_beurt, new_koning_zetten)

                        #  Nu we de situatie hebben uitgespeeld willen we stuk, waar we mee begonnen, weer terugzetten
                        #  Naar zijn oorspronkelijke positie zodat dit niet knoeit in volgende situaties in de toekomst.

                        stuk.nieuwe_positie(positie_van_stuk[0], positie_van_stuk[1])
                        stuk.correcte_soort(soort_stuk)

                        betere_waarde = self.besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, 2)

                        if type(betere_waarde) == list:
                            hoogste_waarde, wat_voor_zet = betere_waarde[0], betere_waarde[1]
                            if len(betere_waarde) > 2:
                                beste_zet = betere_waarde[2]

                else:
                    for richting in hun_zetten[i][1]:  # Voor elke zet die de koning kan doen
                        new_stukken = stukken.copy()
                        new_new_board = []
                        for u in new_board:
                            new_new_board.append(u.copy())

                        # We veranderen het bord en positie weer alsof we de zet hebben gezet
                        stuk.nieuwe_positie(richting[1], richting[0])

                        stuk_dat_moet_springen = 0

                        new_new_board[richting[0]][richting[1]], new_new_board[stuk.positie[1]][stuk.positie[0]] = stuk, 0

                        new_value = self.miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                            stuk_dat_moet_springen, total_depth, hoogste_beurt, new_koning_zetten)

                        # We zetten het weer terug.
                        stuk.nieuwe_positie(positie_van_stuk[0], positie_van_stuk[1])
                        stuk.correcte_soort(soort_stuk)

                        betere_waarde = self.besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, 1)

                        if type(betere_waarde) == list:
                            hoogste_waarde, wat_voor_zet = betere_waarde[0], betere_waarde[1]
                            if len(betere_waarde) > 2:
                                beste_zet = betere_waarde[2]

            else:  # Als je kan zetten met een normale damsteen
                koning_zetten = 0
                if alleen_sprong:  # Als je een stuk kan pakken
                    for richting in hun_zetten[i]:  # Voor elke zet die dit stuk kan doen
                        new_stukken = stukken.copy()
                        new_new_board = []
                        for u in new_board:
                            new_new_board.append(u.copy())

                        # We veranderen het bord en positie weer alsof we de zet hebben gezet
                        new_stukken.remove(new_new_board[richting[0][0]][richting[0][1]])
                        new_new_board[richting[1][0]][richting[1][1]], new_new_board[stuk.positie[1]][stuk.positie[0]], \
                        new_new_board[richting[0][0]][richting[0][1]] = stuk, 0, 0
                        stuk.nieuwe_positie(richting[1][1], richting[1][0])


                        # We kijken of dit stuk hierna nog een keer kan springen
                        nog_een_sprong = definities.damZetten(new_new_board, stuk)

                        if len(nog_een_sprong) > 0:
                            if type(nog_een_sprong[0][0]) == list:  # # Zo ja? dat draaien we de beurt niet om en moet je nog eens met dit stuk springen.
                                # Ps. we kijken niet of het stuk kan promoveren want het is een regel dat je pas mag promoveren met een stuk als je niks kan slaan.
                                stuk_dat_moet_springen = stuk
                                new_value = self.miniMax(diepte - 1, new_stukken, beurt, new_new_board, aantal_stukken,
                                                    stuk_dat_moet_springen, total_depth, hoogste_beurt, koning_zetten)
                            else:  # Zo niet? Dan is de ander aan de beurt en kijken we nog even of onze dam de overkant heeft bereikt.
                                definities.promoveer(stuk)
                                stuk_dat_moet_springen = 0
                                new_value = self.miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                                    stuk_dat_moet_springen, total_depth, hoogste_beurt, koning_zetten)

                        else:
                            definities.promoveer(stuk)
                            stuk_dat_moet_springen = 0
                            new_value = self.miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                                stuk_dat_moet_springen, total_depth, hoogste_beurt, koning_zetten)

                        # We zetten de situatie weer terug
                        stuk.nieuwe_positie(positie_van_stuk[0], positie_van_stuk[1])
                        stuk.correcte_soort(soort_stuk)

                        betere_waarde = self.besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, 2)

                        if type(betere_waarde) == list:
                            hoogste_waarde, wat_voor_zet = betere_waarde[0], betere_waarde[1]
                            if len(betere_waarde) > 2:
                                beste_zet = betere_waarde[2]

                else:  # Als je stuk een dam is maar niks kan pakken
                    for richting in hun_zetten[i]:
                        new_stukken = stukken.copy()
                        new_new_board = []
                        for u in new_board:
                            new_new_board.append(u.copy())

                        # We veranderen het bord en positie weer alsof we de zet hebben gezet
                        stuk_dat_moet_springen = 0
                        new_new_board[richting[0]][richting[1]], new_new_board[stuk.positie[1]][stuk.positie[0]] = stuk, 0
                        stuk.nieuwe_positie(richting[1], richting[0])

                        new_value = self.miniMax(diepte - 1, new_stukken, not beurt, new_new_board, aantal_stukken,
                                            stuk_dat_moet_springen, total_depth, hoogste_beurt, koning_zetten)

                        # We zetten alles weer terug en kijken of ons stuk de overkant heeft bereikt
                        stuk.nieuwe_positie(positie_van_stuk[0], positie_van_stuk[1])
                        definities.promoveer(stuk)

                        betere_waarde = self.besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, 1)

                        if type(betere_waarde) != int:
                            hoogste_waarde, wat_voor_zet = betere_waarde[0], betere_waarde[1]
                            if len(betere_waarde) > 2:
                                beste_zet = betere_waarde[2]

        # Om het algoritme goed te laten werken moeten we deze waardes teruggeven. De hoogste_waarde geven we alleen
        # terug omdat de functie in de definitie zelf wordt opgeroepen. Maar uiteindelijk kijken we alleen maar naar
        # wat de beste zet is en wat voor zet het is (een stuk die een ander stuk pakt of een stuk dat een normale zet
        # doet).
        return [hoogste_waarde, beste_zet, wat_voor_zet]

    def AIzet(self):
        """
        Dit is de main loop van het algoritme. Hier worden de andere definities opgeroepen om samen te besluiten wat de
        beste zet is. Ook wordt het bord en de positie van de stukken hier bijgewerkt na deze zet.
        """
        posities_van_de_stukken = []
        for i in self.pieces:
            posities_van_de_stukken.append(i.positie.copy())

        new_board = self.board.copy()
        # Het enige verschil tussen de volgende twee if'jes, is dat bij de één de witte stukken eerst worden meegegeven
        # en bij de andere eerst de zwarte stukken.
        if self.beurt:
            aangeraden_zet = self.miniMax(self.moeilijkheidsgraad, self.pieces, self.beurt, new_board,
                                     [self.wit, self.zwart],
                                     self.stuk_dat_moet_springen, self.moeilijkheidsgraad, self.beurt, self.aantal_koning_zetten)
        else:
            aangeraden_zet = self.miniMax(self.moeilijkheidsgraad, self.pieces, self.beurt, new_board,
                                     [self.zwart, self.wit],
                                     self.stuk_dat_moet_springen, self.moeilijkheidsgraad, self.beurt, self.aantal_koning_zetten)

        # Na het algoritme zetten we alles weer even normaal voor de zekerheid
        for i in range(0, len(self.pieces)):
            self.pieces[i].nieuwe_positie(posities_van_de_stukken[i][0], posities_van_de_stukken[i][1])
        stuk = aangeraden_zet[1][0]
        nieuwe_plek = aangeraden_zet[1][1]

        print(aangeraden_zet)

        # Hier werken we het bord en dergelijke bij
        return self.bijwerkenAI(self.board, stuk, self.beurt, nieuwe_plek, aangeraden_zet, self.pieces, self.wit, self.zwart)






