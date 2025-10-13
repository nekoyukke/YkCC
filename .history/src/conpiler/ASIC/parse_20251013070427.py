"""
lexerからのものを解析しYkIRを出力
"""
from lexer import Token

def parse(source:str, tokens:list[Token]):
    pos:int = 0
    line:list[str] = []
    def ad():
        pos += 1
        if len(tokens) <= pos:
            raise RuntimeError(f"out of range of pos. now pos token:{tokens[pos-1]}")
    def cu():
        return tokens[pos]
    def ex(tt:str, message:str):
        if tt != cu().type:
            raise RuntimeError(f"{message}")
        res = cu()
        ad()
        return res
    
    def stmt():
        assembly = ""
        while cu().type == "EOF":
            assembly+=f"{expr()}\n"
            ex("NEWLINE", "is not have line")
    def expr():
        nonlocal line
        # 行を分析
        linetok = ex("LINE_NUM", "is not line number")
        line += [linetok.value]
        match (cu().type):
            case _:
                