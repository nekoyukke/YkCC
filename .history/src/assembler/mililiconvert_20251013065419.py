from __future__ import annotations
# Robust import for `util` so this file works both when used as a package
# (e.g. `python -m src.assembler.mililiconvert`) and when executed directly
# (e.g. `python src/assembler/mililiconvert.py`).
    # Try project-root-qualified package first (project might be installed or
    # the workspace root added to sys.path by the environment):
    import YkCC.src.util as util

class Register(object):
    def __init__(self, number:int) -> None:
        self.number = number
    def __repr__(self) -> str:
        return f"r{self.number}"

class Literal(object):
    def __init__(self, value:int) -> None:
        self.value = value
    def __repr__(self) -> str:
        return str(self.value)

class Token(object):
    def __init__(self, name:str, order:list[Literal | Register]) -> None:
        self.name = name
        self.order = order
    def __repr__(self) -> str:
        if self.order:
            return f"{self.name} {' ,'.join([repr(o) for o in self.order]).replace(' ,', ',') }"
        return self.name

def lexer(Source:str) -> list[list[str]]:
    Tokens: list[list[str]] = []
    # Use splitlines() to handle CRLF/LF transparently and remove newline chars
    for line in Source.splitlines():
        # Remove comments starting with ';'
        if ';' in line:
            line = line.split(';', 1)[0]
        # Skip empty/whitespace-only lines
        if not line.strip():
            continue
        parts: list[str] = [p.strip() for p in line.split(',') if p.strip()]
        toks: list[str] = []
        for p in parts:
            toks.extend([t for t in p.split() if t != ''])
        Tokens.append(toks)
    return Tokens

def args(arg:list[str]) -> list[Literal | Register]:
    a:list[Literal | Register] = []
    for i in arg:
        token = i.strip()
        if not token:
            continue
        if token.startswith('r') and token[1:].isdecimal():
            a.append(Register(int(token[1:])))
        elif token.isdecimal():
            a.append(Literal(int(token)))
        elif token.startswith(';'):
            break
        else:
            # Unknown token; keep behavior but include token for debugging
            print(f"error: unexpected token '{token}'")
    return a

def parse(Source:list[list[str]]) -> list[Token]:
    Tokens:list[Token] = []
    for i in Source:
        print(i)
        if i == []:
            continue
        if i[0].startswith(';'):
            continue
        tok:Token = Token(i[0], args(i[1:]))
        Tokens.append(tok)
    return Tokens

def argsLoad(tok:Literal | Register, types:type[Register] | type[Literal] | None = None):
    # 型チェック: 指定された types があれば、その型と一致しない場合は明示的に例外を出す
    if types is not None and type(tok) is not types:
        raise TypeError(f"argsLoad expected {types.__name__}, got {type(tok).__name__}")
    # 値を返す: Literal は 8bit、Register は 4bit を想定して 16進で返す
    if isinstance(tok, Literal):
        # 2桁の16進（ゼロパディング）
        return format(tok.value & 0xff, '02x')
    if isinstance(tok, Register):
        return format(tok.number & 0xf, 'x')
    raise TypeError(f"Unsupported token type: {type(tok).__name__}")

def conversion(Tokens:list[Token]):
    out:str = ""
    for i in Tokens:
        print(i)
        match (i.name.upper()):
            case "ADD":
                if type(i.order[0]) == Register and type(i.order[1]) == Register and type(i.order[2]) == Register:
                    # OK
                    out += "0"
                    out += argsLoad(i.order[0], Register)
                    out += argsLoad(i.order[1], Register)
                    out += argsLoad(i.order[2], Register)
                else:
                    print("Error")
                    return ""
            case "SUB":
                if type(i.order[0]) == Register and type(i.order[1]) == Register and type(i.order[2]) == Register:
                    # OK
                    out += "1"
                    out += argsLoad(i.order[0], Register)
                    out += argsLoad(i.order[1], Register)
                    out += argsLoad(i.order[2], Register)
                else:
                    print("Error")
                    return ""
            case "ADDI":
                if type(i.order[0]) == Register and type(i.order[1]) == Literal:
                    # OK
                    out += "2"
                    out += argsLoad(i.order[0], Register)
                    out += argsLoad(i.order[1], Literal)
                else:
                    print("Error")
                    return ""
            case "SUBI":
                if type(i.order[0]) == Register and type(i.order[1]) == Literal:
                    # OK
                    out += "3"
                    out += argsLoad(i.order[0], Register)
                    out += argsLoad(i.order[1], Literal)
                else:
                    print("Error")
                    return ""
            case "NAND":
                if type(i.order[0]) == Register and type(i.order[1]) == Register and type(i.order[2]) == Register:
                    # OK
                    out += "4"
                    out += argsLoad(i.order[0], Register)
                    out += argsLoad(i.order[1], Register)
                    out += argsLoad(i.order[2], Register)
                else:
                    print("Error")
                    return ""
            case "SHIFT":
                if type(i.order[0]) == Register and type(i.order[1]) == Register and type(i.order[2]) == Literal:
                    # OK
                    out += "5"
                    out += argsLoad(i.order[0], Register)
                    out += argsLoad(i.order[1], Register)
                    out += hex(i.order[2].value & 0xf)[2::]
                else:
                    print("Error")
                    return ""
            case "STORE":
                if type(i.order[0]) == Register and type(i.order[1]) == Register and type(i.order[2]) == Register:
                    # OK
                    out += "6"
                    out += argsLoad(i.order[0], Register)
                    out += argsLoad(i.order[1], Register)
                    out += argsLoad(i.order[2], Register)
                else:
                    print("Error")
                    return ""
            case "LOAD":
                if type(i.order[0]) == Register and type(i.order[1]) == Register and type(i.order[2]) == Register:
                    # OK
                    out += "7"
                    out += argsLoad(i.order[0], Register)
                    out += argsLoad(i.order[1], Register)
                    out += argsLoad(i.order[2], Register)
                else:
                    print("Error")
                    return ""
            case "BRANCH":
                if type(i.order[0]) == Literal and type(i.order[1]) == Register and type(i.order[2]) == Register:
                    # OK
                    out += "8"
                    out += hex(i.order[0].value & 0xf)[2::]
                    out += argsLoad(i.order[1], Register)
                    out += argsLoad(i.order[2], Register)
                else:
                    print("Error")
                    return ""
            case "TIMER":
                if type(i.order[0]) == Register and type(i.order[1]) == Register and type(i.order[2]) == Register:
                    # OK
                    out += "9"
                    out += argsLoad(i.order[0], Register)
                    out += argsLoad(i.order[1], Register)
                    out += argsLoad(i.order[2], Register)
                else:
                    print("Error")
                    return ""
            case "RET":
                # OK
                out += "A"
                out += "000"
            case "HALT":
                # OK
                out += "B"
                out += "000"
            case _:
                print("Error!")
                return ""
    return out

"""
ADD r1 , r2 , r3      ; r1 = r2 + r3
SUB r1 , r2 , r3      ; r1 = r2 - r3
ADDI r1 , n2          ; r1 = r2 + nn
SUBI r1 , n2          ; r1 = r2 - nn
NAND r1 , r2 , r3     ; r1 = nand( r2 , r3 )
SHIFT r1 , r2 , r3    ; r1 = floor(r2 * 2 ^ ((1 - 2 * (r3 & 0b00001000) ) * r3))
STORE r1 , r2 , r3    ; memory(r2 * 2 ^ 8 + r3) = r1
LOAD r1 , r2 , r3     ; r1 = memory(r2 * 2 ^ 8 + r3)
BRANCH flag , r1 , r2 ; 参照フラグを指定し、それが真ならば r1 * 2 ^ 8 + r3 にジャンプ
TIMER r1 , r2 , r3    ; r1 時間待機した後に r2 * 2 ^ 8 + r3 にジャンプ
RET                   ; サブルーチンを終了しサブルーチン実行前に戻る
HALT                  ; 停止
"""

if __name__ == "__main__":
    source = util.read_a_file("ADDI r1,1\nSUBI r1,1")
    lexed = lexer(source)
    parsed = parse(lexed)
    res = conversion(parsed)
    with open("out.bin", "w") as f:
        f.write(res)