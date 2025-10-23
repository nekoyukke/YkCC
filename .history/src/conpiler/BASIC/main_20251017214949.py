from __future__ import annotations
import sys
from pathlib import Path
import parse
import lexer

"""repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
import src.util as util"""

lex = lexer.Lexer()
toks = lex.tokenize("10 FOR I = 0 TO 10\n" \
                    "20 FOR J = 0 TO 10\n" \
                    "30 "
                    "40 NEXT\n" \
                    "50 NEXT\n")
print(toks)
print(parse.parse("", toks))