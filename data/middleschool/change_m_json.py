import json

# ✅ 입력 텍스트 파일과 출력 JSON 파일 경로 설정
input_path = "middle_standards_simple.txt"
output_path = "middle_standards.json"

# ✅ 결과를 저장할 딕셔너리
subject_dict = {}

# ✅ 파일 읽기 및 파싱
with open(input_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or "," not in line:
            continue
        subject, standard = line.split(",", 1)
        subject = subject.strip()
        standard = standard.strip()
        subject_dict.setdefault(subject, []).append(standard)

# ✅ JSON으로 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(subject_dict, f, ensure_ascii=False, indent=2)

print(f"✅ JSON 변환 완료: {output_path}")