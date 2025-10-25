def read_a_file(sample:str):
    import os

    def read_text_file(path: str) -> tuple[str, str]:
        """Try several encodings and return (text, encoding_used)."""
        encodings = ["utf-8", "utf-8-sig", "utf-16", "utf-16le", "utf-16be", "cp932", "shift_jis", "latin-1"]
        with open(path, "rb") as fb:
            data = fb.read()
        last_exc: Exception | None = None
        for enc in encodings:
            try:
                return data.decode(enc), enc
            except Exception as e:
                last_exc = e
                continue
        # 最後の手段
        if data:
            try:
                return data.decode("latin-1"), "latin-1"
            except Exception:
                pass
        raise last_exc or UnicodeDecodeError("utf-8", b"", 0, 1, "decode error")

    if os.path.exists("input.asm"):
        try:
            source, used = read_text_file("input.asm")
            print(f"[read input.asm using encoding: {used}]")
        except Exception as e:
            print(f"Failed to read input.asm: {e}")
            raise
    else:
        # サンプルソース（ファイルが無いときのデモ）
        source = sample
        print("[using sample source]")
        print(source)
    return source


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
            f'\nTraceback: {self.name}'
            f'\n  File "<source>", line {self.line}\n'
            f"    {line_text}\n"
            f"    {pointer}\n"
            f"ParseError: {self.message}"
        )