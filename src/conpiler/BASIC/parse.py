"""
IR設計を見直したためもう一度作成する

"""
from __future__ import annotations
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
        ad()
        return res
    def stmt():
        assembly = ""
        while cu().type != "EOF":
            exp = expr()
            assembly += exp
        return assembly
    def expr():
        # アセンブリ
        res = ""
        # 行を分析
        # Accept either a LINE_NUM token or a plain NUMBER (some lexers emit NUMBER for line labels)
        if cu().type == "LINE_NUM":
            linetok = ex("LINE_NUM", "is not line number")
        else:
            # show what we actually have for easier debugging
            print("expected LINE_NUM or NUMBER, got", cu())
            CallError(cu(), "NEW LINE TOKEN is missing", "expr", source)
        line += [linetok.value]
        if (cu().type != "KEYWORD"):
            return ""
        res += f"; LINE{linetok.value}\n"
        res += f"LINE{linetok.value}:\n"
        match (cu().value):
            case "LET":
                ad()
                # letを分析
                IDNET:Token = ex("IDENT", "An identifier is required.", "Let")
                # ASS
                if ex("OP", "The = operator is unknown", "Let").value != "=":
                    CallError(cu(), "The = operator is unknown", "Let",source)
                # numbers
            case _:
                CallError(cu(), f"unkonw token {cu()}", "expr-end", source)
    return stmt()