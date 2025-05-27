import re

input_path = "middle_standards.txt"  # 원본 텍스트 파일
output_path = "middle_standards_simple.txt"  # 저장할 새 텍스트 파일

subject = None
result = []

with open(input_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        # 과목명 갱신
        if line.startswith("▶"):
            m = re.search(r"▶\s*(중학교\s)?([가-힣]+)", line)
            if m:
                subject = m.group(2)
        elif re.match(r"^\[[0-9가-힣\- ]+\]", line):
            if subject:
                result.append(f"{subject}, {line}")

# 파일로 저장
with open(output_path, "w", encoding="utf-8") as f:
    for item in result:
        f.write(item + "\n")

print(f"✅ 전처리 완료: {output_path}")