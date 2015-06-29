class Mario():

    def move(self):
        print('I am moving')

class Shroom():  # mushroom

    def eat_shroom(self):
        print('Now I am big!')

class BigMario(Mario, Shroom):  # When Mario eats a mushroom
    pass

bm = BigMario()
bm.move()
bm.eat_shroom()
