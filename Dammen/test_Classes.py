import unittest
from Dammen import Classes
from Dammen.Damsteen import Damsteen


class testSetup(unittest.TestCase):

    def test_setup(self):
        board = Classes.setup()
        self.assertEqual([[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]], board)


def test_stukken(spelbord):
    """In deze definitie maken we alle damstenen aan en we zetten die vervolgens op het bord"""
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
        board = Classes.setup()
        stukken_geplaatst = test_stukken(board)
        for i in stukken_geplaatst:
            positie = i.positie
            self.assertEqual(board[positie[1]][positie[0]], i)


class testCheckIfFriendly(unittest.TestCase):

    def test_checkIfEmpty(self):
        board = Classes.setup()
        test_stukken(board)
        leeg_vak = Classes.checkIfFriendly(board, 4, 5)
        self.assertEqual(True, leeg_vak)


class testDraaiDeBeurt(unittest.TestCase):

    def test_beurtOmdraaien(self):
        beurt = False
        andere_beurt = Classes.draaiDeBeurt(beurt)
        self.assertEqual(True, andere_beurt)


class testEinde(unittest.TestCase):

    def test_einde(self):
        aantal_witte_stukken = 0
        aantal_zwarte_stukken = 3
        gewonnen = Classes.einde(aantal_witte_stukken, aantal_zwarte_stukken)
        self.assertEqual(True, gewonnen)

    def test_nietEinde(self):
        aantal_witte_stukken = 1
        aantal_zwarte_stukken = 3
        gewonnen = Classes.einde(aantal_witte_stukken, aantal_zwarte_stukken)
        self.assertEqual(False, gewonnen)


class testJuisteStukken(unittest.TestCase):

    def test_juisteStukken(self):
        beurt = False
        board = Classes.setup()
        zwarte_stukken = Classes.juisteStukken(test_stukken(board), beurt)
        for i in range(0, len(zwarte_stukken)):
            zwarte_stukken[i] = zwarte_stukken[i].positie

        self.assertEqual([[0, 7], [2, 7]], zwarte_stukken)


class testPromoveer(unittest.TestCase):

    def test_promovering(self):
        dam = Damsteen(5, 0, False)
        self.assertEqual(False, dam.king)
        dam.promoveren()
        self.assertEqual(True, dam.king)


def Koningstukken1(spelbord):
    """In deze definitie maken we alle damstenen aan en we zetten die vervolgens op het bord"""
    w1 = Damsteen(5, 4, 'wit')

    alle_stenen = [w1]
    posities = []

    for steen in alle_stenen:  # Pakt van elke steen zijn positie
        posities.append(steen.positie)

    for i in range(0, len(posities)):  # Zet alle stenen op het bord
        spelbord[posities[i][1]][posities[i][0]] = alle_stenen[i]
    return alle_stenen


def Koningstukken2(spelbord):
    """In deze definitie maken we alle damstenen aan en we zetten die vervolgens op het bord"""
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
        board = Classes.setup()
        stuk = Koningstukken1(board)
        stuk[0].promoveren()
        alle_zetten = Classes.koningStappen(board, stuk[0])
        verwachte_uitkomst = [0, [[3, 4], [2, 3], [1, 2], [0, 1], [5,4],[6,3],[7,2],[3, 6], [2,7], [5,6], [6, 7]]]
        self.assertEqual(verwachte_uitkomst, alle_zetten)

    def test_koningStappenPakken(self):
        board = Classes.setup()
        stuk = Koningstukken2(board)
        stuk[0].promoveren()
        alle_zetten = Classes.koningStappen(board, stuk[0])
        verwachte_uitkomst = [stuk[0], [[[4, 3], [5, 2], [6, 1], [7, 0]]]]
        self.assertEqual(verwachte_uitkomst, alle_zetten)


def Koningstukken3(spelbord):
    """In deze definitie maken we alle damstenen aan en we zetten die vervolgens op het bord"""
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
        board = Classes.setup()
        stuk = Koningstukken3(board)
        stuk[0].promoveren()
        alle_zetten = Classes.diagonaalKoningSpringen(board, Classes.koningStappen(board, stuk[0]))
        verwachte_uitkomst = [stuk[0], [[[4, 3], [5, 2]]], 0]
        self.assertEqual(verwachte_uitkomst, alle_zetten)


class testStukkenBijhouden(unittest.TestCase):

    def test_stukkenBijhouden(self):
        z1 = Damsteen(0, 4, "Zwart")
        zwart = 5
        wit = 4
        self.assertEqual([3, 5], Classes.stukkenBijhouden(wit, zwart, z1))


def damPakken(spelbord):
    """In deze definitie maken we alle damstenen aan en we zetten die vervolgens op het bord"""
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
        board = Classes.setup()
        stuk = Koningstukken1(board)
        alle_zetten = Classes.damZetten(board, stuk[0])
        verwachte_uitkomst = [[5, 6], [5, 4]]
        self.assertEqual(verwachte_uitkomst, alle_zetten)

    def test_dammenPakken(self):
        board = Classes.setup()
        stukken = damPakken(board)
        alle_zetten = Classes.damZetten(board, stukken[0])
        verwachte_uitkomst = [[[6, 4], [7, 3]], [[4, 4], [3, 3]]]
        self.assertEqual(verwachte_uitkomst, alle_zetten)


class testHerhaling(unittest.TestCase):

    def test_nietHerhaling(self):
        self.assertEqual(False, Classes.herhaling(4))

    def test_welHerhaling(self):
        self.assertEqual(True, Classes.herhaling(15))


def kanNiksMeer(spelbord):
    """In deze definitie maken we alle damstenen aan en we zetten die vervolgens op het bord"""
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
        board = Classes.setup()
        stukken = damPakken(board)
        beurt = True
        wat_ik_verwacht = [True, False, [stukken[0]], [[[[6, 4], [7, 3]], [[4, 4], [3, 3]]]]]
        self.assertEqual(wat_ik_verwacht, Classes.watKanJeZetten(board, stukken, beurt, False))

    def test_watKanJeZetten(self):
        board = Classes.setup()
        stukken = Koningstukken1(board)
        beurt = True
        wat_ik_verwacht = [0, False, [stukken[0]], [[[5, 6], [5, 4]]]]
        self.assertEqual(wat_ik_verwacht, Classes.watKanJeZetten(board, stukken, beurt, False))

    def test_kanJePakken(self):
        board = Classes.setup()
        stukken = damPakken(board)
        beurt = True
        wat_ik_verwacht = True
        self.assertEqual(wat_ik_verwacht, Classes.watKanJeZetten(board, stukken, beurt, True))

    def test_kanNiksMeer(self):
        board = Classes.setup()
        stukken = kanNiksMeer(board)
        beurt = True
        wat_ik_verwacht = [False, True, 0, 0]
        self.assertEqual(wat_ik_verwacht, Classes.watKanJeZetten(board, stukken, beurt, False))


class testGameStaat(unittest.TestCase):

    def test_gameStaat(self):
        board = Classes.setup()
        stukken = kanNiksMeer(board)
        beurt = True
        self.assertEqual(-3, Classes.gameStaat(stukken, beurt, beurt))


class testEindNode(unittest.TestCase):

    def test_eindNode(self):
        game_over = True
        alleen_sprong = True
        aantal_stukken = [4, 5]
        beurt = True
        self.assertEqual(100, Classes.eindnode(game_over, alleen_sprong, aantal_stukken, beurt))


