from lark import Lark, Transformer


grammar = r"""
    start: NUM
    NUM: /\d+/
"""


class T(Transformer):
    NUM = int


def main():
    tree = Lark(grammar, parser="lalr").parse("32")
    print("post_transform:", T().transform(tree))
    print("embedded_parse_start")
    print(Lark(grammar, parser="lalr", transformer=T()).parse("32"))


if __name__ == "__main__":
    main()
