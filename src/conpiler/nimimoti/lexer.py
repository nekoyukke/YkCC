import re
from tokens import Token, TokenType
import utils  # type: ignore

def tokenize(source: str) -> list[Token]:
    """
    Tokenに変換する
    """
    token_spec = [
        # 特殊
        ('TYPE_MUT', r'&mut'),
        ('TYPE_COPY', r'&copy'),
        ('TYPE_BORROW', r'&borrow'),
        ('ARGS', r'\.\.args'),
        ('UNSAFE', r'@unsafe'),
        # 2文字以上の演算子・記号（長い順）
        ('EQSTRICT', r'==='),
        ('NESTRICT', r'!=='),
        ('CMP', r'<=>'),
        ('LSHIFT', r'<<'),
        ('RSHIFT', r'>>'),
        ('NULLCOALESCING', r'\?\?'),
        ('NULLREJECT', r'\?!'),
        ('ELVIS', r'\?:'),
        ('REJECT', r'!!'),
        ('LOGICOR', r'\|\|'),
        ('LOGICAND', r'&&'),
        ('LOGICXOR', r'\^\^'),
        ('DIVV', r'//'),
        ('ARROW', r'->'),
        ('INC', r'\+\+'),
        ('DEC', r'--'),
        ('EQ', r'=='),
        ('NE', r'!='),
        ('LE', r'<='),
        ('GE', r'>='),
        ('DOUBLEDOT', r'\.\.'),
        ('ADD_ASSIGN', r'\+='),
        ('SUB_ASSIGN', r'-='),
        ('MUL_ASSIGN', r'\*='),
        ('DIV_ASSIGN', r'/='),
        ('DIVV_ASSIGN', r'//='),
        ('NULLCOALESCING_ASSIGN', r'\?='),
        ('NONECOALESCING_ASSIGN', r'%%='),
        # 1文字記号
        ('ASSIGN', r'='),
        ('LABRACKET', r'<'),
        ('RABRACKET', r'>'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        ('SEMI', r';'),
        ('COLON', r':'),
        ('COMMA', r','),
        ('DOT', r'\.'),
        ('DIV', r'/'),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULT', r'\*'),
        ('MOD', r'%'),
        ('ADD', r'&'),
        ('LOGICNOT', r'!'),
        ('BITXOR', r'\^'),
        ('BITOR', r'\|'),
        ('BITNOT', r'~'),
        # スキップ
        ('SKIP', r'\s+'),
        # リテラル
        ('STR', r'"[^"]*"'),
        ('FLOAT', r'\d+\.\d+'),
        ('NUMBER', r'\d+'),
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ]

    KEYWORDS = {"let", "val", "cont", "define", "Null", "None", "TRUE", "FALSE", "if", "else", "elif"
                , "null", "none", "while", "for", "return", "import", "in"}
    TYPES = {"Dec", "Num", "Str", "Any", "List", "Array",
             "Tuple", "Class", "Map", "Funcion", "Dynamic", "Ptr",
             "int8", "uint8", "int16", "uint16", "int32", "uint32", "int64", "uint64", "int128", "uint128",
             "float32", "float64",
             "float", "double", "Bool",
             "int", "long", "short", "char",
             "ref", "&mut", "&copy", "&borrow",}


    regex: str = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    tokens: list[Token] = []

    for mo in re.finditer(regex, source):
        kind: str | None = mo.lastgroup
        value: str = mo.group()
        start = mo.start()
        # 行・列番号を計算
        line = source.count("\n", 0, start) + 1
        col = start - source.rfind("\n", 0, start)
        # 分類 
        # swichに切り替えをする
        if col == -1:  # 改行がなければ先頭から
            col = start + 1
        if kind == 'NUMBER':
            tokens.append(Token(TokenType.NUMBER, int(value), line, col))
            continue
        if kind is None:
            raise RuntimeError(f"予想外のトークン！{mo.group()}")
        if kind == 'SKIP':
            continue
        if kind == 'TYPE_MUT':
            tokens.append(Token(TokenType.tMUT, value, line, col))
        elif kind == 'TYPE_COPY':
            tokens.append(Token(TokenType.tCOPY, value, line, col))
        elif kind == 'TYPE_BORROW':
            tokens.append(Token(TokenType.tBORROW, value, line, col))
        elif kind == 'TYPE_REF':
            tokens.append(Token(TokenType.tREF, value, line, col))
        elif kind == "UNSAFE":
            tokens.append(Token(TokenType.UNSAFE, value, line, col))
        elif value in KEYWORDS:
            tokens.append(Token(TokenType[value.upper()], value, line, col))
        elif value in TYPES:
            tokens.append(Token(TokenType[f't{value.upper()}'], value, line, col))
        elif kind == "ID":
            tokens.append(Token(TokenType.ID, value, line, col))
        elif kind == "STR":
            tokens.append(Token(TokenType.STR, value.strip('"'), line, col))
        else:
            tokens.append(Token(TokenType[kind], value, line, col))

    tokens.append(Token(TokenType.END, 0))
    return tokens
