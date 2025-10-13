"""
lexerからのものを解析しYkIRを出力
"""
def parse():
    pos:int = 0
    def cu():
        pos += 1
    def ex():