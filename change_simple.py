import re

# 원본 텍스트 파일 (붙여넣은 그대로 저장)
raw_path = "data/raw_standards.txt"
clean_path = "data/achievement_standards.txt"

with open(raw_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

result = []
current_grade = ""
current_subject = ""

for line in lines:
    line = line.strip()
    
    # 제목 줄인 경우 → 학년/교과 추출
    if line.startswith("▶"):
        m = re.match(r"▶\s*([0-9~학년]+)\s+(.+?)\s+성취기준", line)
        if m:
            current_grade = m.group(1).strip()
            full_subject = m.group(2).strip()            # ✅ 전체 과목명
            current_subject = full_subject.split()[0]    # ✅ "국어 읽기" → "국어"
    
    # 성취기준 줄인 경우 → 코드 포함 줄
    elif re.match(r"^\[[0-9가-힣\-]+\]", line):
        result.append(f"{current_grade},{current_subject},{line}")

# 결과 저장
with open(clean_path, "w", encoding="utf-8") as f:
    for r in result:
        f.write(r + "\n")

print(f"✅ 변환 완료! 저장 위치: {clean_path}")