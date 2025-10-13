from enum import Enum
import utils  # type: ignore


class TokenType(Enum):
    # 仮代入
    STR = "str"
    NUMBER = "NUMBER"
    DECIMAL = "DECIMAL"

    # リテラル類
    ID = "ID"
    VAL = "val"
    LET = "let"
    CONT = "cont"
    IF = "if"
    ELSE = "else"
    ELIF = "elif"
    WHILE = "while"
    FOR = "for"
    FAMILY = "family"
    STATIC = "static"
    RETURN = "return"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "null"
    NONE = "none"
    DEFINE = "define"
    IMPORT = "import"
    IN = "in"
    ARGS = "...args"

    # アノテーション
    UNSAFE = "@unsafe"

    # 特別に用意するもの
    END = "@END@"
    DFFUNC = "@FUNC@" # 関数
    DFUNION = "@DFLIST@" # Nodeでリストを表すためにする（ゴミ仕様）
    DFACCESS = "@DFACCESS@" #アクセスとか
    DFMAP = "@MAP@" # マップ用
    DFLIST = "@LIST@" # リスト用
    DFARRAY = "@ARRAY@" # 配列
    DFTUPLE = "@TUPLE@" # タプル
    DFARGS = "@ARGS@" # 引数


    # 型
    tNUM = "Num"
    tDEC = "Dec"
    tSTR = "Str"
    tANY = "Any"
    tLIST = "List"
    tARRAY = "Array"
    tDYNAMIC = "Dynamic"
    tMAP = "Map"
    tPTR = "Ptr"
    tBOOL = "Bool"
    tTUPLE = "Tuple"
    tFUNCTION = "Function"
    tCLASS = "Class"

    #　自由型
    tANYNUMBER = "@number@"
    tANYFLOAT = "@float@"

    # 借用・所有権型
    tREF = "ref"
    tMUT = "&mut"
    tCOPY = "&copy"
    tBORROW = "&borrow"

    # MEM
    tINT8 = "int8"
    tUINT8 = "uint8"
    tINT16 = "int16"
    tUINT16 = "uint16"
    tINT32 = "int32"
    tUINT32 = "uint32"
    tINT64 = "int64"
    tUINT64 = "uint64"
    tINT128 = "int128"
    tUINT128 = "uint128"

    tFLOAT32 = "float32"
    tFLOAT64 = "float64"
    tFLOAT = "float"
    tDOUBLE = "double"
    tINT = "int"
    tLONG = "long"
    tSHORT = "short"
    tCHAR = "char"

    # イコール
    ASSIGN = "="
    ADD_ASSIGN = "+="
    SUB_ASSIGN = "-="
    MUL_ASSIGN = "*="
    DIV_ASSIGN = "/="
    DIVV_ASSIGN = "//="
    MOD_ASSIGN = "%="
    NULLCOALESCING_ASSIGN = "?="
    NONECOALESCING_ASSIGN = "%%="
    
    # Union
    tUNION = "TYPE_UNION"
    
    # かっこ類
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    LABRACKET = "<"
    RABRACKET = ">"
    LPAREN = "("
    RPAREN = ")"
    
    # 演算子
    PLUS = "+"
    MINUS = "-"
    MULT = "*"
    EXP = "**"
    ADD = "&"
    DIV = "/"
    DIVV = "//"
    LOGICAND = "&&"
    LOGICXOR = "^^"
    LOGICOR = "||"
    LOGICNOT = "!"
    BITNOT = "~"
    BITOR = "|"
    BITXOR = "^"
    SEMI = ";"
    COLON = ":"

    DOUBLEDOT = ".."

    INC = "++"
    DEC = "--"

    NULLCOALESCING = "??"
    NONECOALESCING = "%%%"
    ELVIS = "?:"
    NULLREJECT = "?!"
    NONEREJECT = "%%!"
    REJECT = "!!"
    COMMA = ","
    DOT = "."
    ARROW = "->"
    EQ = "=="
    NE = "!="
    EQSTRICT = "==="
    NESTRICT = "!=="
    LE = "<="
    GE = ">="
    CMP = "<=>"
    LSHIFT = "<<"
    RSHIFT = ">>"

class Token(object):
    def __init__(
        self,
        type_: TokenType,
        value: float | int | str,
        line: int = 0,
        column: int = 0,
    ) -> None:
        self.type: TokenType = type_
        self.value: float | int | str = value
        self.line: int = line
        self.column: int = column
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"

class Borrow(Enum):
    Have = 0
    Borrow = 1
    Hum = 2
    Ref = 3
    Humed = 4
    Borrowed = 5
    Moved = 6