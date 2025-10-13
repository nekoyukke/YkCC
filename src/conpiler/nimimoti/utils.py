import logging
"""
デバッグ便利コード用
フラグがTrueならINFO以下も表示
"""
FLAG=True
if FLAG:
    logging.basicConfig(
        level=logging.DEBUG,                # ログレベル（DEBUG 以上を表示）
        format="%(asctime)s  [%(levelname)s]:%(message)s ",  # 出力フォーマット
    )
else:
    logging.basicConfig(
        level=logging.INFO,                # ログレベル（DEBUG 以上を表示）
        format="%(asctime)s  [%(levelname)s]:%(message)s ",  # 出力フォーマット
    )
class ParseError(Exception):
    def __init__(self, message: str, line: int, column: int, source: str, name: str) -> None:
        self.message = message
        self.line = line
        self.column = column
        self.source = source
        self.name = name
        super().__init__(self.__str__())

    def __str__(self) -> str:
        # 行テキストを抽出
        line_text = self.source.splitlines()[self.line - 1]
        # カーソル位置に ^ を置く
        pointer = " " * (self.column - 1) + "^"
        return (
            f'\n呼び出し元: {self.name}'
            f'\n  File "<source>", line {self.line}\n'
            f"    {line_text}\n"
            f"    {pointer}\n"
            f"ParseError パーサ解析エラー！: {self.message}"
        )
    
class InterPreterError(Exception):
    def __init__(self, message: str, line: int, column: int, source: str, name: str) -> None:
        self.message = message
        self.line = line
        self.column = column
        self.source = source
        self.name = name
        super().__init__(self.__str__())

    def __str__(self) -> str:
        # 行テキストを抽出
        line_text = self.source.splitlines()[self.line - 1]
        # カーソル位置に ^ を置く
        pointer = " " * (self.column - 1) + "^"
        return (
            f'\n呼び出し元: {self.name}'
            f'\n  File "<source>", line {self.line}\n'
            f"    {line_text}\n"
            f"    {pointer}\n"
            f"InterPreterError 実行エラー！: {self.message}"
        )

class AnalysisError(Exception):
    def __init__(self, message: str, line: int, column: int, source: str, name: str) -> None:
        self.message = message
        self.line = line
        self.column = column
        self.source = source
        self.name = name
        super().__init__(self.__str__())

    def __str__(self) -> str:
        # 行テキストを抽出
        line_text = self.source.splitlines()[self.line - 1]
        # カーソル位置に ^ を置く
        pointer = " " * (self.column - 1) + "^"
        return (
            f'\n呼び出し元: {self.name}'
            f'\n  File "<source>", line {self.line}\n'
            f"    {line_text}\n"
            f"    {pointer}\n"
            f"Analysis 構文解析エラー！: {self.message}"
        )