import unittest
from Dammen import definities
from Dammen.Damsteen import Damsteen
from Dammen.AI import DamAI


ai = DamAI()

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


class testGameStaat(unittest.TestCase):

    def test_gameStaat(self):
        """
        Ik test of de definitie de goede waarde van het bord teruggeeft.
        """
        board = definities.setup()
        stukken = kanNiksMeer(board)
        beurt = True
        self.assertEqual(-3.3, ai.gameStaat(stukken, beurt, beurt))


class testEindNode(unittest.TestCase):

    def test_eindNode(self):
        """
        Ik test of de definitie de goede waarde teruggeeft wanneer hij geen stukken meer overheeft.
        """
        game_over = True
        alleen_sprong = True
        aantal_stukken = [4, 5]
        beurt = True
        self.assertEqual([100], ai.eindnode(game_over, alleen_sprong, aantal_stukken, beurt))


class testBesteWaarde(unittest.TestCase):

    def test_besteWaarde(self):
        diepte = 2
        total_depth = 2
        new_value = [3]
        hoogste_waarde = 0
        stuk = Damsteen(2, 3, 'wit')
        richting = [[3, 4]]
        soort_zet = 1

        x = ai.besteWaarde(diepte, total_depth, new_value, hoogste_waarde, stuk, richting, soort_zet)

        self.assertEqual([3, 1, [stuk, [[3, 4]]]], x)


class testBijWerkenAI(unittest.TestCase):

    def test_bijwerkenAI(self):
        stuk = Damsteen(2, 3, 'wit')
        pieces = [stuk]
        aantal_witte_stukken = 1
        aantal_zwarte_stukken = 0
        board = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,stuk,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]

        beurt = True
        nieuwe_plek = [3,4]
        aangeraden_zet = [1]

        x = ai.bijwerkenAI(board, stuk, beurt, nieuwe_plek, aangeraden_zet, pieces, aantal_witte_stukken, aantal_zwarte_stukken)

        self.assertEqual([[[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,stuk,0,0,0],
                           [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]], 0, False, [1, 0], pieces, stuk], x)

