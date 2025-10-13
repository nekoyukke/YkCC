from __future__ import annotations
from tokens import Token, TokenType 
from myast import *
import utils

def ast(Tokens:list[Token], source: str):
    pos = 0

    rexadd = 1
    def ad():
        nonlocal pos
        pos+=1
        print(f"{Tokens[pos],pos}")
    def cu(name:str = "unkwon"):
        nonlocal pos
        if (pos >= len(Tokens)):
            raise utils.ParseError("out of range", Tokens[pos-1].line, Tokens[pos-1].column, source, name)
        return Tokens[pos]
    def ex(tok:TokenType, name:str = "unkwon", message:str = "unkown"):
        nonlocal pos
        cua = cu(name)
        ad()
        if (cua.type == tok):
            return cua
        else:
            raise utils.ParseError(message,cua.line,cua.column,source,name)
    def rex(tok:TokenType, name:str):
        nonlocal rexadd
        if (cu().type == tok):
            cua = ex(tok, name, "unkown tokens")
            rexadd = cua
            return True
        else:
            return False
    
    def exprs(type:TokenType):
        exp = Expr([])
        while cu("exprs").type != type:
            exp.op += [expr()]
        return exp
    def expr():
        nod = Declaration()
        return nod
    
    def Declaration():
        if (rex(TokenType.LET, "Declaration")):
            # もしletなら
            rexa = rexadd
            typenode = _type()
            nametok = ex(TokenType.ID)
            if (rex(TokenType.ASSIGN, "Declaration")):
                right = expr()
                nod = DeclarationNode(rexa, right, nametok, typenode)
            else:
                nod = DeclarationNode(rexa, NilNode(), nametok, typenode)
            return nod
        elif (rex(TokenType.VAL, "Declaration")):
            # もしvalなら
            pass
        elif (rex(TokenType.CONT, "Declaration")):
            # もしcontなら
            pass
        else:
            return add()
    
    def _type():
        if (rex(TokenType.tLIST, "type")):
            # もしリストなら
            rexa = rexadd
            ex(TokenType.LABRACKET, "type", "it dont have '<' Token in type call")
            nod = _type()
            nod = TypeNode(rexa, nod)
            ex(TokenType.LABRACKET, "type", "it dont have '>' Token in type call")
            return nod
        nod = cu()
        ad()
        return TypeNode(nod, NilNode())
    
    def add():
        nod = mul()
        cus = cu()
        while (cus.type in (TokenType.PLUS, TokenType.MINUS)):
            ad()
            nod = BinaryOperation(cus, nod, mul())
            cus = cu()
        return nod
    
    def mul():
        nod = prime()
        cus = cu()
        while (cus.type in (TokenType.MULT, TokenType.MULT)):
            ad()
            nod = BinaryOperation(cus, nod, prime())
            cus = cu()
        return nod

    def prime():
        cus = cu()
        if (cus.type == TokenType.NUMBER):
            ad()
            return NumberNode(cus.value, cus)
        elif (cus.type == TokenType.ID):
            ad()
            return VariableNode(cus.value, cus)
        elif (cus.type == TokenType.LPAREN):
            ad()
            nod = expr()
            ex(TokenType.RPAREN, "prime", "it dont have ')' Token")
            return nod
        raise
    nod = exprs(TokenType.END)
    return nod