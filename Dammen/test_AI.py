import unittest
from Dammen import Classes
from Dammen.Damsteen import Damsteen
from Dammen import AI



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
        board = Classes.setup()
        stukken = kanNiksMeer(board)
        beurt = True
        self.assertEqual(-3, AI.gameStaat(stukken, beurt, beurt))


class testEindNode(unittest.TestCase):

    def test_eindNode(self):
        game_over = True
        alleen_sprong = True
        aantal_stukken = [4, 5]
        beurt = True
        self.assertEqual(100, AI.eindnode(game_over, alleen_sprong, aantal_stukken, beurt))