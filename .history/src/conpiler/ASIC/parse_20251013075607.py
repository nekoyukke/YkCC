"""
lexerからのものを解析しYkIRを出力
"""
from lexer import Token

def parse(source:str, tokens:list[Token], addr:list[int] = [], reg:list[int] = []):
    pos:int = 0
    line:list[str] = []
    useingaddress:list[int] = []
    useingaddress+=addr
    useingreg: list[int] = reg
    Variable:dict[str,int] = {} # 名前:番地
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
    def allocmem():
        n = 0
        while True:
            if n not in useingaddress:
                useingaddress.append(number)
            n += 1
    def freemem(number:int):
        useingaddress.append(number)
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
        if (cu().type != "KEYWORD"):
            return ""
        match (cu().value):
            case "LET":
                mem = allocmem()
                indent = ex("INDENT", "is not indent")
                if ex("OP", "is not op").value == "=":
                    raise RuntimeError("is not op")

            case "IF":
                pass
            case "THEN":
                pass
            case "GOTO":
                pass
            case "FOR":
                pass
            case "NEXT":
                pass
            case "PRINT":
                pass
            case "INPUT":
                pass
            case "END":
                # HALT
                return "HLT"
            case "GOSUB":
                pass
            case "RETURN":
                pass
            case "STEP":
                pass
            case "TO":
                pass
            case "ELSE":
                pass
            case "REM":
                pass
            case "AND":
                pass
            case "OR":
                pass
            case "NOT":
                pass
            case _:
                # パスする
                return ""
    def compute():
        if cu().type == "INDENT":
            return ""