"""
lexerからのものを解析しYkIRを出力
構文:
LET 変数名 = 式

(+,1,2)で区切る

IF 式 比較記号 式 THEN 番号 ELSE 番号

"""
from lexer import Token

def parse(source:str, tokens:list[Token], addr:list[int] = [], reg:list[int] = []):
    pos:int = 0
    line:list[str] = []
    useingaddress:list[int] = []
    useingaddress+=addr
    useingreg: list[int] = reg
    Variable:dict[str,int] = {} # 名前:番地
    number:int = 0
    def ad():
        nonlocal pos
        pos += 1
        if len(tokens) <= pos:
            print(f"out of range of pos. now pos token:{tokens[pos-1]}")
            raise RuntimeError(f"out of range of pos. now pos token:{tokens[pos-1]}")
    def cu():
        return tokens[pos]
    def ex(tt:str, message:str):
        if tt != cu().type:
            print(message, cu())
            raise RuntimeError(f"{message}{cu()}")
        res = cu()
        ad()
        return res
    def allocmem():
        n = 0
        while True:
            if n not in useingaddress:
                useingaddress.append(n)
                return n
            n += 1
    def freemem(number:int):
        useingaddress.pop(useingaddress.index(number))
    def allocreg():
        n = 0
        while True:
            if n not in useingreg:
                useingreg.append(n)
                return n
            n += 1
    def freereg(number:int):
        useingreg.pop(useingreg.index(number))
    def stmt():
        assembly = ""
        while cu().type != "EOF":
            strs = expr()
            if strs == "@BL@":
                # expr() returned NEXT signal: consume the NEXT keyword and its newline
                if cu().type == "KEYWORD" and cu().value == "NEXT":
                    ad()  # consume NEXT
                    if cu().type == "NEWLINE":
                        ad()  # consume newline after NEXT
                break
            assembly += strs + "\n"
            if (cu().type == "EOF"):

                
            ex("NEWLINE", "is not have line")
        return assembly
    def expr():
        nonlocal line, number, pos
        # アセンブリ
        res = ""
        # 行を分析
        # Accept either a LINE_NUM token or a plain NUMBER (some lexers emit NUMBER for line labels)
        if cu().type == "LINE_NUM":
            linetok = ex("LINE_NUM", "is not line number")
        elif cu().type == "NUMBER":
            linetok = ex("NUMBER", "is not line number")
        else:
            # show what we actually have for easier debugging
            print("expected LINE_NUM or NUMBER, got", cu())
            raise RuntimeError(f"is not line number{cu()}")
        line += [linetok.value]
        if (cu().type != "KEYWORD"):
            return ""
        res += f"; LINE{linetok.value}\n"
        res += f"LINE{linetok.value}:\n"
        match (cu().value):
            case "LET":
                ad()
                mem = allocmem()
                ident = ex("IDENT", "is not indent")
                op = ex("OP", "is not op")
                if op.value != "=":
                    raise RuntimeError(f"is not op{op}")
                computed = compute()
                res += computed[0]
                res += "\n"
                # メモリにセット
                res += f"; memset\nSET {mem}, r{computed[1][0]}\n"
                # 設定
                Variable[ident.value] = mem
                return res
            case "IF":
                ad()
                cm = cmp()
                res += cm[0]
                res += "\n"
                # THENトークン
                if not ex("KEYWORD", "THEN is no").value == "THEN":
                    print("THEN is no")
                    raise RuntimeError
                number1 = ex("NUMBER", "number is no")
                flag = cu().value == "ELSE"
                number2 = tokens[0]
                if flag:
                    ad()
                    number2 = ex("NUMBER", "number is no")
                match(cm[1].value):
                    case "==":
                        # JE
                        res += f"; je to then number\n"
                        res += f"JE LINE{number1.value}\n"
                        if flag:
                            res += f"; jmp to else\n"
                            res += f"JMP LINE{number2.value}\n"
                    case "!=":
                        # JNE
                        res += f"; je to then number\n"
                        res += f"JNE LINE{number1.value}\n"
                        if flag:
                            res += f"; jmp to else\n"
                            res += f"JMP LINE{number2.value}\n"
                    case ">":
                        # JA
                        res += f"; je to then number\n"
                        res += f"JA LINE{number1.value}\n"
                        if flag:
                            res += f"; jmp to else\n"
                            res += f"JMP LINE{number2.value}\n"
                    case "<":
                        # JNAE
                        res += f"; je to then number\n"
                        res += f"JNAE LINE{number1.value}\n"
                        if flag:
                            res += f"; jmp to else\n"
                            res += f"JMP LINE{number2.value}\n"
                    case ">=":
                        # JAE
                        res += f"; je to then number\n"
                        res += f"JAE LINE{number1.value}\n"
                        if flag:
                            res += f"; jmp to else\n"
                            res += f"JMP LINE{number2.value}\n"
                    case "<=":
                        # JNA
                        res += f"; je to then number\n"
                        res += f"JNA LINE{number1.value}\n"
                        if flag:
                            res += f"; jmp to else\n"
                            res += f"JMP LINE{number2.value}\n"
                    case _:
                        return ""
                return res
            case "GOTO":
                ad()
                numtok = ex("NUMBER", "number is no")
                res += f"; goto{numtok.value}\n"
                res += f"JMP LINE{numtok.value}\n"
                return res
            case "FOR":
                ad()
                mem = allocmem()
                nametok = ex("IDENT", "NOT HAVE IDENT")
                if not ex("OP", "NOT HAVE =").value == "=":
                    print("NOT HAVE =")
                    return ""
                # 式
                computed = compute()
                res += "; FOR INDENT\n"
                Variable[nametok.value] = mem
                # 次
                if not ex("KEYWORD", "NOTHAVE 'TO'").value == "TO":
                    print("NOT HAVE 'TO'")
                    return ""
                computed = compute()
                # レジスタを開放
                ex("NEWLINE", "NONE NEWLINE")
                res += stmt()
                # NEXT後の処理
                reg = allocreg()
                res += "; inc mem\n"
                res += f"FORLOOP{number}:\n"
                res += f"GET r{reg}, {mem}\n"
                res += f"INC r{reg}"
                res += f"SET {mem}, r{reg}"
                # もしなら
                res += "; CMP for registr\n"
                res += f"CMPI r{reg}, r{computed[1][0]}\n"
                res += f"JNE FORLOOP{number}"
                res += f"; END"
                freereg(computed[1][0])
                freereg(reg)
            case "NEXT":
                return "@BL@"
            case "PRINT":
                return res
            case "INPUT":
                return res
            case "END":
                # HALT
                return "; Halt\nHLT"
            case "GOSUB":
                return res
            case "RETURN":
                return res
            case "STEP":
                return res
            case "TO":
                return res
            case "REM":
                while cu().type != "NEWLINE":
                    ad()
                return ""
            case "AND":
                return res
            case "OR":
                return res
            case "NOT":
                return res
            case _:
                # パスする
                return ""
        return ""
    def cmp():
        res = ""
        a = compute()
        op = cu()
        ad()
        b = compute()
        res += f"; CMP A B\n"
        res += f"{a[0]}"
        res += f"{b[0]}"
        res += "; CMP\n"
        res += f"CMP r{a[1][0]}, r{b[1][0]}"
        freereg(a[1][0])
        freereg(b[1][0])
        return (res, op)

    def compute() -> tuple[str, list[int]]:
        res = ""

        regs = [allocreg()]
        # 初期化
        res += f"; SetZero\nLOAD r{regs[0]}, 0\n"
        if cu().type == "IDENT":
            print("inent")
            res = f"; Get a memory\nGET r{regs[0]}, {Variable[cu().value]}\n"
            ad()
            return (res, [regs[0]])
        elif cu().type == "NUMBER":
            print("number")
            res = f"; Set a number\nLOAD r{regs[0]}, {cu().value}\n"
            ad()
            return (res, [regs[0]])
        else:
            # トークン消費
            ex("LPAREN", "There is no left parenthesis ( LPAREN. ")
            # 計算をする
            optok = cu()
            ad()
            print("op")
            # +,14,a
            # ,消費
            ex("COMMA", "is no left parenthesis , COMMA")
            if optok.type == "CMPOP":
                #別の処理
                pass
            else:
                while cu().type != "RPAREN":
                    print(regs)
                    computed = compute()
                    regs += computed[1]
                    res += computed[0]
                    match (optok.value):
                        case "+":
                            res += f"; ADD\nADD r{regs[0]}, r{regs[1]}, r{regs[0]}\n"
                            freereg(regs[1])
                        case "-":
                            res += f"; SUB\nSUB r{regs[0]}, r{regs[1]}, r{regs[0]}\n"
                            freereg(regs[1])
                        case "*":
                            res += f"; MUL\nMUL r{regs[0]}, r{regs[1]}, r{regs[0]}\n"
                            freereg(regs[1])
                        case "/":
                            res += f"; DIV\nDIV r{regs[0]}, r{regs[1]}, r{regs[0]}\n"
                            freereg(regs[1])
                        case "MOD":
                            res += f"; MOD\nMOD r{regs[0]}, r{regs[1]}, r{regs[0]}\n"
                            freereg(regs[1])
                        case _:
                            raise RuntimeError
                    if cu().type == "RPAREN":
                        break
                    ex("COMMA", "is no left parenthesis , COMMA")
                    regs.pop()
            # トークン消費
            ex("RPAREN", "There is no left parenthesis ) RPAREN.")
            print(regs)
            return (res, regs)
    return stmt()