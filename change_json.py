import json

input_path = "data/achievement_standards.txt"
output_path = "data/achievement_standards_by_grade.json"

structured_data = {}

with open(input_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",", 2)
        if len(parts) == 3:
            grade, subject, content = [p.strip() for p in parts]
            if grade not in structured_data:
                structured_data[grade] = {}
            if subject not in structured_data[grade]:
                structured_data[grade][subject] = []
            structured_data[grade][subject].append(content)

# 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(structured_data, f, ensure_ascii=False, indent=2)

print(f"✅ 구조화된 JSON 저장 완료: {output_path}")