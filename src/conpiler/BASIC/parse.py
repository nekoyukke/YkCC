"""
IR設計を見直したためもう一度作成する

"""
from __future__ import annotations
from array import array
import sys
from lexer import Token
from pathlib import Path
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
import src.util as util

def CallError(tok:Token, message:str, name:str, source:str):
    raise util.ParseError(message, tok.lineno,tok.col,source, name)

def parse(tokens:list[Token], source:str):
    pos = 0
    llabeldict:dict[str,list[int]] = {}
    glabeldict:dict[str,list[int]] = {}
    llabelpos = 0
    glabelpos = 0
    Scope:list[str] = ["Global"]

    def usepos() -> int:
        nonlocal llabelpos, glabelpos
        if Scope[-1] == "Global" and len(Scope) == 1:
            glabelpos += 1
            return glabelpos
        llabelpos += 1
        return llabelpos
    
    def isglobal() -> bool:
        return Scope[-1] == "Global" and len(Scope) == 1
    
    def ad(name:str):
        nonlocal pos
        pos += 1
        if len(tokens) <= pos:
            print(f"out of range of pos. now pos token:{tokens[pos-1]}")
            CallError(tokens[pos-1], "Error! Out of range", name, source)

    def cu():
        return tokens[pos]
    
    def ex(tt:str, message:str, name:str):
        if tt != cu().type:
            CallError(cu(), message, name, source)
        res = cu()
        ad(name)
        return res
    
    def stmt() -> str:
        assembly = ""
        while cu().type != "EOF":
            exp = expr()
            assembly += exp
        return assembly
    
    def expr() -> str:
        # YkIR
        res = ""
        # 行を分析
        # Accept either a LINE_NUM token or a plain NUMBER (some lexers emit NUMBER for line labels)
        if cu().type == "LINE_NUM":
            linetok = ex("LINE_NUM", "is not line number", "Expr")
        else:
            # show what we actually have for easier debugging
            print("expected LINE_NUM or NUMBER, got", cu())
            CallError(cu(), "NEW LINE TOKEN is missing", "expr", source)
            raise
        if (cu().type != "KEYWORD"):
            return ""
        res += f"; LINE{linetok.value}\n"
        res += f"LINE{linetok.value}:\n"
        match (cu().value):
            case "LET":
                ad("Let")
                # letを分析
                IDNET:Token = ex("IDENT", "An identifier is required.", "Let")
                # ASS
                if ex("OP", "The = operator is unknown", "Let").value != "=":
                    CallError(cu(), "The = operator is unknown", "Let",source)
                # numbers
                
            case _:
                CallError(cu(), f"unkonw token {cu()}", "expr-end", source)
    def comp(name:str) -> tuple[str, int,]:
        addr:int = usepos()
        isglobal_ = isglobal()
        cur = cu()
        # 数字
        if cur.type == "NUMBER":
            if isglobal_:
                return f"${addr} = anyi:imm {cur.value}",addr
            return f"%{addr} = anyi:imm {cur.value}", addr
        elif cur.type == "IDENT":
            if isglobal_:
                CallError(cur, "Variable usage is only allowed within the scope.", f"Comp-{name}",source)
                raise
            return f"%{addr} = "

    return stmt()