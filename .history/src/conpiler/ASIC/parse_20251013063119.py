"""
lexerからのものを解析しYkIRを出力
"""
from lexer import Token

def parse(source:str, tokens:list[Token]):
    pos:int = 0
    def ad():
        pos += 1
        if len(tokens) <= pos:
            raise RuntimeError(f"out of range of pos. now pos token:{tokens[pos-1]}")
    def cu():
        return tokens[pos]
    def ex(tt:str, message:str):
        if tt != cu().type:
            raise RuntimeError(f"{message}")
        ad()
    
    def stmt():
        while cu().type == "EOF":
            
            ex("NEWLINE", "is not have line")
    def expr():
        