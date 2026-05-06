import text
from random import randint, choice


class RetroEffects:

    def __init__(self):
        self.matrix_list = []
        self.max_len = 0
        self.texts = ['R_ACCESS DENIED', 'G_ACCESS GRANTED', 'R_UNEXPECTED ERROR', 'R_ERROR OCCURRED', 'G_MADE IN PYTHON',
                      'G_PROCESS FINISHED']
        self.glitch_text = text.TextAlpha((0, 0), 16, (0, 0, 0))

    def random_glitch(self):
        if randint(0, 500) == 1:
            new_text = choice(self.texts)
            if 'G_' in new_text:
                self.glitch_text = text.Text((choice((randint(10, 120), randint(660, 750))), randint(220, 900)), 16, (0, 255, 0), text=new_text[2:])
            elif 'R_' in new_text:
                self.glitch_text = text.Text((choice((randint(10, 120), randint(660, 750))), randint(220, 900)), 16, (255, 0, 0), text=new_text[2:])

    def draw_glitch(self):
        self.glitch_text.draw()

    def load_matrix_effect(self):
        y = -1000
        new_matrix_list = []
        for i in range(20):
            k = randint(3, 7)
            side = choice((-1, 1))
            if side:
                x = randint(0, 300)
            else:
                x = randint(700, 1000)
            for j in range(k):
                new_matrix_list.append(text.TextAlpha((x, y + randint(-10, 10)), 16, (35, 180, 0)))
                new_matrix_list[len(new_matrix_list) - 1].change_text(str(bin(randint(1, 2048)))[2:])
                x += side * randint(200, 400)
            y += randint(40, 60)
        self.max_len = len(new_matrix_list)
        self.matrix_list += new_matrix_list

    def clear(self):
        self.max_len = 0
        self.matrix_list = []
        RetroEffects.load_matrix_effect(self)

    def draw_matrix_effect(self):
        for index, digits in enumerate(self.matrix_list):
            if digits.position[1] >= 0:
                self.matrix_list[index].change_alpha(abs(int((1000 - digits.position[1]) / 1000 * 255)))
            digits.draw()
            self.matrix_list[index].change_position((digits.position[0], digits.position[1] + 1))

    def clear_matrix_effect(self):
        self.matrix_list = [i for i in self.matrix_list if i.position[1] <= 1000]

        if len(self.matrix_list) < self.max_len:
            RetroEffects.load_matrix_effect(self)
