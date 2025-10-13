from lexer import tokenize
from tokens import Token
from myast import *
from parser import *

import logging
import utils  # type: ignore
# from interpreter import evaluate
# from environment import Environment

def run_source(source: str) -> None:
    """
    ソースコードを実行する
    """
    logging.debug(f"Tokens::")
    tokens: list[Token] = tokenize(source)
    for t in tokens:
        logging.debug(f"Token: {t}")
    node = ast(tokens, source)
    print(node)
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            print(run_source(f.read()))
    else:
        while True:
            try:
                line = input(">>> ")
                print(run_source(line))
            except Exception as e:
                print("Error:", e)