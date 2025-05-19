import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings

# ✅ 1. 환경 변수 로딩
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# ✅ 2. JSON 파일 경로 설정
JSON_PATH = "data/achievement_standards.json"

# ✅ 3. 임베딩 모델 설정
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# ✅ 4. 선택된 학년과 교과에 해당하는 성취기준 문서 로딩
def load_filtered_documents(json_path, selected_grade, selected_subject):
    docs = []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if selected_grade in data and selected_subject in data[selected_grade]:
        for content in data[selected_grade][selected_subject]:
            docs.append(Document(
                page_content=content,
                metadata={"학년": selected_grade, "교과": selected_subject}
            ))
    return docs

# ✅ 5. Streamlit UI
st.set_page_config(page_title="성취기준 추천기", page_icon="🎯")
st.title("🎯 성취기준 추천기")
st.markdown("**수업 활동을 입력하면, 관련된 성취기준을 추천합니다.**")

# 학년 및 교과 선택
grade_options = ["1~2학년", "3~4학년", "5~6학년"]
subject_options = ["국어", "수학", "사회", "과학", "슬기생활", "도덕", "체육", "음악", "미술", "실과"]

selected_grade = st.selectbox("📘 학년 선택", grade_options)
selected_subject = st.selectbox("📙 교과 선택", subject_options)
user_input = st.text_area("📝 수업 활동을 입력하세요", height=150)

# 검색 버튼
if st.button("🔍 성취기준 찾기"):
    if not user_input.strip():
        st.warning("수업 활동 내용을 입력해주세요.")
    else:
        with st.spinner("AI가 성취기준을 찾고 있어요..."):
            # 선택한 학년/교과 성취기준만 불러오기
            filtered_docs = load_filtered_documents(JSON_PATH, selected_grade, selected_subject)

            if not filtered_docs:
                st.error(f"{selected_grade} {selected_subject} 성취기준이 없습니다.")
            else:
                # ✅ 선택된 문서만 임베딩하여 검색
                vectorstore = Chroma.from_documents(filtered_docs, embedding=embedding_model)
                results_with_scores = vectorstore.similarity_search_with_score(user_input, k=10)

                # ✅ 중복 제거 및 학년·교과 필터링 후 최대 5개 출력
                unique_contents = set()
                final_results = []
                for doc, _ in results_with_scores:
                    content = doc.page_content.strip()
                    meta = doc.metadata
                    if meta.get("학년") == selected_grade and meta.get("교과") == selected_subject:
                        if content not in unique_contents:
                            unique_contents.add(content)
                            final_results.append(content)
                    if len(final_results) == 5:
                        break

                # 결과 출력
                if final_results:
                    st.subheader("📌 추천 성취기준")
                    for i, content in enumerate(final_results, 1):
                        st.markdown(f"**{i}.** {content}")
                else:
                    st.info("관련 성취기준을 찾을 수 없어요. 입력을 다시 시도해보세요.")