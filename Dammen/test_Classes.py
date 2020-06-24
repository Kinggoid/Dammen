import unittest
from Dammen import definities
from Dammen.Damsteen import Damsteen


class testSetup(unittest.TestCase):

    def test_setup(self):
        """Hier kijk ik of de definitie wel een bord met de goede dimensies maakt."""
        board = definities.setup()
        self.assertEqual([[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]], board)


def test_stukken(spelbord):
    w1 = Damsteen(1, 0, 'wit')

    z1 = Damsteen(0, 7, 'zwart')
    z2 = Damsteen(2, 7, 'zwart')

    alle_stenen = [w1, z1, z2]
    posities = []

    for steen in alle_stenen:  # Pakt van elke steen zijn positie
        posities.append(steen.positie)

    for i in range(0, len(posities)):  # Zet alle stenen op het bord
        spelbord[posities[i][1]][posities[i][0]] = alle_stenen[i]
    return alle_stenen


class testDrawBoard(unittest.TestCase):

    def test_board(self):
        """Hier kijk ik of de posities van de stukken (objecten) overeenkomen met hun positie op het bord."""
        board = definities.setup()
        stukken_geplaatst = test_stukken(board)
        for i in stukken_geplaatst:
            positie = i.positie
            self.assertEqual(board[positie[1]][positie[0]], i)


class testCheckIfFriendly(unittest.TestCase):

    def test_checkIfEmpty(self):
        """Hier kijk ik of het vakje wat ik heb geselecteerd inderdaad wordt gezien als een leeg vak."""
        board = definities.setup()
        test_stukken(board)
        leeg_vak = definities.checkIfFriendly(board, 4, 5)
        self.assertEqual(True, leeg_vak)


class testEinde(unittest.TestCase):

    def test_einde(self):
        """Ik check of de definitie aangeeft of het spel inderdaad gewonnen is."""
        aantal_witte_stukken = 0
        aantal_zwarte_stukken = 3
        gewonnen = definities.einde(aantal_witte_stukken, aantal_zwarte_stukken)
        self.assertEqual(True, gewonnen)

    def test_nietEinde(self):
        """Ik check of de definitie aangeeft of het spel inderdaad niet gewonnen is."""
        aantal_witte_stukken = 1
        aantal_zwarte_stukken = 3
        gewonnen = definities.einde(aantal_witte_stukken, aantal_zwarte_stukken)
        self.assertEqual(False, gewonnen)


class testJuisteStukken(unittest.TestCase):

    def test_juisteStukken(self):
        """Ik check of de definitie inderdaad alleen maar de stukken hun positie teruggeeft."""
        beurt = False
        board = definities.setup()
        zwarte_stukken = definities.juisteStukken(test_stukken(board), beurt)
        for i in range(0, len(zwarte_stukken)):
            zwarte_stukken[i] = zwarte_stukken[i].positie

        self.assertEqual([[0, 7], [2, 7]], zwarte_stukken)


class testPromoveer(unittest.TestCase):

    def test_promovering(self):
        """Ik kijk of de definitie inderdaad een stuk kan promoveren."""
        dam = Damsteen(5, 0, False)
        self.assertEqual(False, dam.king)
        dam.promoveren()
        self.assertEqual(True, dam.king)


def Koningstukken1(spelbord):
    w1 = Damsteen(5, 4, 'wit')

    alle_stenen = [w1]
    posities = []

    for steen in alle_stenen:  # Pakt van elke steen zijn positie
        posities.append(steen.positie)

    for i in range(0, len(posities)):  # Zet alle stenen op het bord
        spelbord[posities[i][1]][posities[i][0]] = alle_stenen[i]
    return alle_stenen


def Koningstukken2(spelbord):
    w1 = Damsteen(7, 0, 'wit')

    z1 = Damsteen(3, 4, 'zwart')

    alle_stenen = [w1, z1]
    posities = []

    for steen in alle_stenen:  # Pakt van elke steen zijn positie
        posities.append(steen.positie)

    for i in range(0, len(posities)):  # Zet alle stenen op het bord
        spelbord[posities[i][1]][posities[i][0]] = alle_stenen[i]
    return alle_stenen


class testKoningStappen(unittest.TestCase):

    def test_koningStappenZetten(self):
        """Ik check of de definitie de juiste informatie teruggeeft wanneer een koning alleen maar kan zetten en niks kan pakken."""
        board = definities.setup()
        stuk = Koningstukken1(board)
        stuk[0].promoveren()
        alle_zetten = definities.koningStappen(board, stuk[0])
        verwachte_uitkomst = [0, [[3, 4], [2, 3], [1, 2], [0, 1], [5,4],[6,3],[7,2],[3, 6], [2,7], [5,6], [6, 7]]]
        self.assertEqual(verwachte_uitkomst, alle_zetten)

    def test_koningStappenPakken(self):
        """Ik check of de definitie de juiste informatie teruggeeft wanneer een koning iemand kan pakken."""
        board = definities.setup()
        stuk = Koningstukken2(board)
        stuk[0].promoveren()
        alle_zetten = definities.koningStappen(board, stuk[0])
        verwachte_uitkomst = [stuk[0], [[[4, 3], [5, 2], [6, 1], [7, 0]]]]
        self.assertEqual(verwachte_uitkomst, alle_zetten)


def Koningstukken3(spelbord):
    w1 = Damsteen(7, 0, 'wit')

    z1 = Damsteen(3, 4, 'zwart')
    z2 = Damsteen(3, 6, 'zwart')

    alle_stenen = [w1, z1, z2]
    posities = []

    for steen in alle_stenen:  # Pakt van elke steen zijn positie
        posities.append(steen.positie)

    for i in range(0, len(posities)):  # Zet alle stenen op het bord
        spelbord[posities[i][1]][posities[i][0]] = alle_stenen[i]
    return alle_stenen


class testDiagonaalKoningStappen(unittest.TestCase):

    def test_koningNogEenKeerSlaan(self):
        """Wanneer een koning nog een keer kan slaan, heeft hij meestal wat minder vakjes waar hij na zijn eerste
        sprong op kan landen. Hier check ik of de definitie inderdaad alleen die vakken teruggeeft en de bijbehorende informatie teruggeeft."""
        board = definities.setup()
        stuk = Koningstukken3(board)
        stuk[0].promoveren()
        alle_zetten = definities.diagonaalKoningSpringen(board, definities.koningStappen(board, stuk[0]))
        verwachte_uitkomst = [stuk[0], [[[4, 3], [5, 2]]], 0]
        self.assertEqual(verwachte_uitkomst, alle_zetten)


class testStukkenBijhouden(unittest.TestCase):

    def test_stukkenBijhouden(self):
        """Hier check ik of de definitie goed het aantal stukken bijhoudt."""
        z1 = Damsteen(0, 4, "Zwart")
        zwart = 5
        wit = 4
        self.assertEqual([3, 5], definities.stukkenBijhouden(wit, zwart, z1))


def damPakken(spelbord):
    w1 = Damsteen(5, 5, 'wit')

    z1 = Damsteen(4, 4, 'zwart')
    z2 = Damsteen(4, 6, 'zwart')

    alle_stenen = [w1, z1, z2]
    posities = []

    for steen in alle_stenen:  # Pakt van elke steen zijn positie
        posities.append(steen.positie)

    for i in range(0, len(posities)):  # Zet alle stenen op het bord
        spelbord[posities[i][1]][posities[i][0]] = alle_stenen[i]
    return alle_stenen


class testDamZetten(unittest.TestCase):

    def test_dammenVooruit(self):
        """Hier check ik of de definitie de goede zetten teruggeeft wanneer een gewone dam alleen maar vooruit kan zetten."""
        board = definities.setup()
        stuk = Koningstukken1(board)
        alle_zetten = definities.damZetten(board, stuk[0])
        verwachte_uitkomst = [[5, 6], [5, 4]]
        self.assertEqual(verwachte_uitkomst, alle_zetten)

    def test_dammenPakken(self):
        """Hier check ik of de definitie de juiste informatie teruggeeft wanneer een gewone dam kan slaan."""
        board = definities.setup()
        stukken = damPakken(board)
        alle_zetten = definities.damZetten(board, stukken[0])
        verwachte_uitkomst = [[[6, 4], [7, 3]], [[4, 4], [3, 3]]]
        self.assertEqual(verwachte_uitkomst, alle_zetten)


class testHerhaling(unittest.TestCase):

    def test_nietHerhaling(self):
        """Hier check ik of de definitie ziet dat het nog geen gelijkspel (door te vaak alleen de koning te zetten) is."""
        self.assertEqual(False, definities.herhaling(4))

    def test_welHerhaling(self):
        """Hier check ik of de definitie ziet dat het gelijkspel (door te vaak alleen de koning te zetten) is."""
        self.assertEqual(True, definities.herhaling(15))


def kanNiksMeer(spelbord):
    w1 = Damsteen(4, 5, 'wit')

    z1 = Damsteen(3, 6, 'zwart')
    z2 = Damsteen(2, 7, 'zwart')
    z3 = Damsteen(5, 6, 'zwart')
    z4 = Damsteen(6, 7, 'zwart')

    alle_stenen = [w1, z1, z2, z3, z4]
    posities = []

    for steen in alle_stenen:  # Pakt van elke steen zijn positie
        posities.append(steen.positie)

    for i in range(0, len(posities)):  # Zet alle stenen op het bord
        spelbord[posities[i][1]][posities[i][0]] = alle_stenen[i]
    return alle_stenen


class testWatKanJeZetten(unittest.TestCase):

    def test_watKanJePakken(self):
        """Hier kijk ik of de definitie, gegeven een positie waarin een dam kan slaan, de juiste informatie teruggeeft."""
        board = definities.setup()
        stukken = damPakken(board)
        beurt = True
        wat_ik_verwacht = [True, False, [stukken[0]], [[[[6, 4], [7, 3]], [[4, 4], [3, 3]]]]]
        self.assertEqual(wat_ik_verwacht, definities.watKanJeZetten(board, stukken, beurt, False))

    def test_watKanJeZetten(self):
        """Hier kijk ik of de definitie, gegeven een positie waarin een dam vooruit kan lopen, de juiste informatie teruggeeft."""
        board = definities.setup()
        stukken = Koningstukken1(board)
        beurt = True
        wat_ik_verwacht = [0, False, [stukken[0]], [[[5, 6], [5, 4]]]]
        self.assertEqual(wat_ik_verwacht, definities.watKanJeZetten(board, stukken, beurt, False))

    def test_kanJePakken(self):
        """De definitie heeft ook een stand waar je alleen kan kijken of je iets kan pakken. Ik kijk nu of hij
        inderdaad alleen zegt of dat het geval is."""
        board = definities.setup()
        stukken = damPakken(board)
        beurt = True
        wat_ik_verwacht = True
        self.assertEqual(wat_ik_verwacht, definities.watKanJeZetten(board, stukken, beurt, True))

    def test_kanNiksMeer(self):
        """In het geval dat je geen enkel stuk hebt dat kan bewegen, dan zou deze definitie moeten zeggen dat je hebt
        verloren. We kijken nu of hij dat inderdaad meegeeft."""
        board = definities.setup()
        stukken = kanNiksMeer(board)
        beurt = True
        wat_ik_verwacht = [False, True, 0, 0]
        self.assertEqual(wat_ik_verwacht, definities.watKanJeZetten(board, stukken, beurt, False))



