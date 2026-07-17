class Foo:
    x: int
    y: int

    def __init__(self):
        self.x, self.y = 0, 0
        print('empty', self.x, self.y)

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        print('int int', self.x, self.y)

    def __init__(self, x: int, y: float):
        self.x, self.y = x, int(y)
        print('int float', self.x, self.y)


Foo()
Foo(1, 2)
Foo(1, 2.3)
a: int = 3
b: int = 5
Foo(a, b)
