; アセンブラ用置換ファイルmilili用
; ジャンプ・サブルーチン関連強化パッチ
def <JMP>  ,<BRANCH,1>:
def <JNC>  ,<BRANCH,2>:
def <JC>   ,<BRANCH,3>:
def <JNZ>  ,<BRANCH,4>:
def <JZ>   ,<BRANCH,5>:
def <JA>   ,<BRANCH,6>:
def <JNA>  ,<BRANCH 7>:
def <CALL> ,<TIMER r0>:
def <a>, <12>:
JMP strart



strart:
ADDI r1,2
JMP loop
loop:
ADDI r1,a
JMP loop