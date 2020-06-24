import pygame


class Damsteen:
    radius = 0
    rand = 0
    waarde = 1

    def __init__(self, positie_x, positie_y, team):
        self.positie = [positie_x, positie_y]
        if team == 'wit' or team == 'Wit':
            self.team = True
        else:
            self.team = False
        self.king = False  # Iedereen begint als een man (man = normale damsteen en koning = gepromoveerde damsteen)

    def promoveren(self):  # Als je een damsteen wilt promoveren
        self.king = True
        self.waarde = 50

    def correcte_soort(self, koning):
        self.king = koning
        if koning:
            self.waarde = 6
        else:
            self.waarde = 1

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
        pygame.draw.circle(scherm, zwart_rand, plaats_vakje, self.radius + 2, self.rand)

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