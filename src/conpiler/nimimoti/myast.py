from __future__ import annotations
from tokens import Token

# 総合ノード
class AllNode(object):
    def __repr__(self, level:int = 0) -> str:
        return ""

class NilNode(AllNode):
    def __init__(self) -> None:
        pass
    def __repr__(self, level: int = 0) -> str:
        return "    "*level + "None Node"

class TypeNode(AllNode):
    def __init__(self, thistype:Token, havetype:AllNode) -> None:
        self.thistype = thistype
        self.havetype = havetype
    def __repr__(self, level: int = 0) -> str:
        return "    "*level + f"{self.thistype}:[\n{self.havetype.__repr__(level+1)}\n]"

# exprノード
class Expr(AllNode):
    def __init__(self, op:list[AllNode]) -> None:
        self.op = op
    
    def __repr__(self, level: int = 0) -> str:
        return "    "*level + "\n".join([i.__repr__(level+1) for i in self.op])

# リテラルノード
class LiteralNode(AllNode):
    def __repr__(self, level:int = 0) -> str:
        return ""

# 数字トークン
class NumberNode(LiteralNode):
    def __init__(self, number:int, tok:Token) -> None:
        self.tok = tok
        self.number = number

    def __repr__(self, level:int = 0) -> str:
        return "    "*level + f"NumberNode:{self.number}"

# 変数ノード
class VariableNode(LiteralNode):
    def __init__(self, Variable:str, tok:Token) -> None:
        self.tok = tok
        self.Variable = Variable

    def __repr__(self, level:int = 0) -> str:
        return "    "*level + f"VariableNode:{self.Variable}"

# 組の
class SetNode(LiteralNode):
    def __init__(self, tok:Token, op:list[AllNode]) -> None:
        self.op = op
        self.tok = tok
    
    def __repr__(self, level: int = 0) -> str:
        return "    "*level + f"{self.tok}::" + "\n".join([i.__repr__(level+1) for i in self.op])


# 内部評価式ノード
class InExprNode(AllNode):
    def __repr__(self, level:int = 0) -> str:
        return ""
# 二項演算
class BinaryOperation(InExprNode):
    def __init__(self,OpTok:Token, Left:AllNode, Right:AllNode) -> None:
        self.tok = OpTok
        self.left = Left
        self.right = Right

    def __repr__(self, level:int = 0) -> str:
        return "    "*level + f"{self.tok}[\n" + f"{self.left.__repr__(level+1)}\n" + f"{self.right.__repr__(level+1)}\n" + "}"

class UnaryOperator(InExprNode):
    def __init__(self,OpTok:Token, Node:AllNode) -> None:
        self.tok = OpTok
        self.node = Node

    def __repr__(self, level:int = 0) -> str:
        return "    "*level + f"{self.tok}[\n" + f"{self.node.__repr__(level + 1)}\n" + "}"

# 外部評価式ノード
class OutExprNode(AllNode):
    def __repr__(self, level:int = 0) -> str:
        return ""

# 式宣言ノード
class DeclarationNode(OutExprNode):
    def __init__(self, Declarationtok:Token, right:AllNode, Declarationname:Token, type:AllNode) -> None:
        self.tok = Declarationtok
        self.right = right
        self.Declarationname = Declarationname
        self.type = type
    
    def __repr__(self, level: int = 0) -> str:
        return "    "*level + f"{self.tok}:{self.Declarationname}\n" + f"{self.right.__repr__(level+1)}\n" + "}"
# loopノード
class LoopNode(OutExprNode):
    def __init__(self, Looptok:Token, right:AllNode, Loopnode:AllNode) -> None:
        self.tok = Looptok
        self.right = right
        self.Loopnode = Loopnode
    
    def __repr__(self, level: int = 0) -> str:
        return "    "*level + f"{self.tok}:{self.Loopnode.__repr__(level + 1)}\n" + f"{self.right.__repr__(level+1)}\n" + "}"
# ifノード
class IfNode(OutExprNode):
    def __init__(self, Iftok:Token, right:AllNode, op:AllNode) -> None:
        self.iftok= Iftok
        self.right = right
        self.op = op

    def __repr__(self, level: int = 0) -> str:
        return "    "*level + f"{self.iftok}:[" + f"{self.op.__repr__(level+1)}\n" + "]"

# returnノード
class ReturnNode(OutExprNode):
    def __init__(self, op:AllNode) -> None:
        self.op = op
    def __repr__(self, level: int = 0) -> str:
        return "    "*level + f"return[{self.op.__repr__(level+1)}]\n"

# 関数ノード
class DefineNode(OutExprNode):
    def __init__(self, name:Token, formulas:AllNode, setnode:AllNode) -> None:
        self.setnode = setnode
        self.nametok = name
        self.formulas = formulas

    def __repr__(self, level: int = 0) -> str:
        return "    "*level + f"define{self.nametok}[\n" + f"{self.formulas.__repr__(level+1)}\n]"