from __future__ import annotations
import util as util

def assemble_with_labels(src:str):
    lines = [line.strip() for line in src.splitlines() if line.strip()]
    labels:dict[str, str] = {}
    if len(lines) <= 0:
        return ""

    # --- パス1: ラベル収集 ---
    code_lines: list[str] = []
    # 今の行（コード行としてカウントする番号）
    linenumber = 0
    for line in lines:
        # コメント行は無視
        if line.startswith(";"):
            continue
        # ラベル定義: 2つの形式を許容する
        # 1) def <name> <value>:
        # 2) def <old>,<new>:
        if line.lower().startswith("def") and line.endswith(":"):
            body = line[3:-1].strip()
            # カンマ区切り形式を優先
            if "," in body:
                old, new = [s.strip() for s in body.split(",", 1)]
                # 角括弧が使われている場合は剥がす
                if old.startswith("<") and old.endswith(">"):
                    old = old[1:-1].strip()
                if new.startswith("<") and new.endswith(">"):
                    new = new[1:-1].strip()
                labels[old] = new
            else:
                parts = body.split()
                if len(parts) >= 2:
                    name = parts[0]
                    value = parts[1]
                    if name.startswith("<") and name.endswith(">"):
                        name = name[1:-1].strip()
                    if value.startswith("<") and value.endswith(">"):
                        value = value[1:-1].strip()
                    labels[name] = value
                else:
                    # フォーマット不正なら無視
                    continue
        elif line.endswith(":"):
            # 形式: "label:" -> ラベル名を登録し、ラベル行自体は除去
            labelname = line[:-1].strip()
            # 角括弧がある場合は剥がす
            if labelname.startswith("<") and labelname.endswith(">"):
                labelname = labelname[1:-1].strip()
            # ラベルの値として、現在のコード行インデックスを文字列で保存
            labels[labelname] = str(linenumber)
        else:
            code_lines.append(line)
            linenumber+=1

    # --- パス2: ラベル置換 & コード生成 ---
    # --- パス2: 単純置換 & コード生成 ---
    import re
    final_lines: list[str] = []
    for line in code_lines:
        new = line
        for old, newval in labels.items():
            # 単語境界で置換（例: 'a' が 'ab' の一部にならないようにする）
            new = re.sub(rf"\b{re.escape(old)}\b", newval, new)
        final_lines.append(new)

    return "\n".join(final_lines)

if __name__ == "__main__":
    source = util.read_a_file("def <a>, <12>:\nADDI r1,a")

    res = assemble_with_labels(source)
    print(res)
    with open("out.bin", "w", encoding="utf-8") as f:
        f.write(res)