"""
lexerからのものを解析しYkIRを出力
"""
from lexer import Token

def parse(source:str, tokens:list[Token]):
    pos:int = 0
    def cu():
        pos += 1
        if len(tokens) < pos:
            raise RuntimeError("")
    def ex():