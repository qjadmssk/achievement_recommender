# 🎯 성취기준 추천기 (Achievement Standards Recommender)

초등학교 교육과정에 따라 수업 활동에 어울리는 성취기준을 인공지능으로 추천해주는 시스템입니다.  
Streamlit을 기반으로 한 웹 앱으로, 학년과 교과를 선택하고 수업 활동을 입력하면 관련된 성취기준을 추출합니다.

## 🔧 주요 기능

- ✅ 초등학교 성취기준 JSON 기반 자동 필터링
- ✅ OpenAI 임베딩(text-embedding-3-small) 기반 의미 유사도 검색
- ✅ 학년/교과 선택 후 **해당 범위 내에서만 임베딩** 수행
- ✅ 최대 5개의 유사 성취기준 추천 + 유사도 점수 표시
- ✅ 벡터 검색 라이브러리 Chroma 활용
- ✅ `.env`로 API 키 안전 관리

---

## 📁 프로젝트 구조

achievement_recommender/
│
├── app.py                         # Streamlit 메인 코드
├── data/
│   └── achievement_standards.json # 성취기준 JSON 파일
├── .env                           # OpenAI API 키 등 환경 변수 (미포함)
├── requirements.txt              # 필요한 패키지 목록
└── .gitignore                    # 업로드 제외 목록 (env/, pycache/, chroma_db 등)

---

## 🚀 실행 방법

1. 이 저장소를 클론하세요.

```bash
git clone https://github.com/qjadmssk/achievement_recommender.git
cd achievement_recommender

	2.	가상환경 설정 후 패키지 설치

python -m venv env
source env/bin/activate      # Windows는 .\env\Scripts\activate
pip install -r requirements.txt

	3.	.env 파일 생성

OPENAI_API_KEY=sk-...

	4.	앱 실행

streamlit run main.py


⸻

📌 데이터 설명
	•	achievement_standards.json:
학년 → 교과 → 성취기준 리스트로 구성된 구조.
예시:

{
  "3~4학년": {
    "국어": [
      "글의 중심 생각을 파악한다.",
      "적절한 어휘를 사용해 글을 쓴다."
    ]
  }
}


⸻

🤖 인공지능 원리
	•	text-embedding-3-small 모델로 임베딩
	•	Chroma에서 유클리드 거리를 기준으로 유사한 문장 검색
	•	학년/교과를 필터링한 뒤 유사도 높은 성취기준 최대 5개 추출
