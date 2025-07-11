import os
import re

# 입력 파일 경로
INPUT_FILE = 'testing_result_ver2'
# 함수별 출력 디렉터리
OUTPUT_DIR = './functions'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 파일을 한 줄씩 읽어들임
with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

i = 0
total = len(lines)

while i < total - 1:
    sig = lines[i].rstrip()
    # 함수 시그니처 탐지: 
    # 1) 앞뒤 공백 제거 후 ')'로 끝나고, 
    # 2) 다음 줄이 중괄호 '{' 하나만 있을 때
    if sig.endswith(')') and lines[i+1].strip() == '{':
        # 함수 이름 추출: '(' 앞 부분의 마지막 토큰
        func_name = sig.split('(')[0].split()[-1]
        func_lines = [lines[i], lines[i+1]]
        # 중괄호 카운터: '{' 로 열기, '}' 로 닫기
        brace_count = lines[i+1].count('{') - lines[i+1].count('}')
        j = i + 2

        # 짝이 맞을 때까지 계속 읽어들임
        while j < total and brace_count > 0:
            line = lines[j]
            brace_count += line.count('{') - line.count('}')
            func_lines.append(line)
            j += 1


        out_path = os.path.join(OUTPUT_DIR, f"{func_name}.c")
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(func_lines)
        print(f"[저장] {func_name}.c ({len(func_lines)} lines)")

        # 다음 검색 위치를 함수 끝 다음으로 이동
        i = j
    else:
        i += 1

