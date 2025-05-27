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
ELEMENTARY_JSON_PATH = "data/achievement_standards.json"
MIDDLE_JSON_PATH = "data/middleschool/middle_standards.json"
HIGH_JSON_PATH = "data/highschool/high_standards.json"

# ✅ 3. 임베딩 모델 설정
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# ✅ 4. 초등 필터링 함수 (학년+과목)
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

# ✅ 5. 중학교 필터링 함수 (과목만)
def load_filtered_documents_middle(json_path, selected_subject):
    docs = []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if selected_subject in data:
        for content in data[selected_subject]:
            docs.append(Document(
                page_content=content,
                metadata={"교과": selected_subject}
            ))
    return docs

# ✅ 6. 고등학교 필터링 함수 (과목만)
def load_filtered_documents_high(json_path, selected_subject):
    docs = []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if selected_subject in data:
        for content in data[selected_subject]:
            docs.append(Document(
                page_content=content,
                metadata={"교과": selected_subject}
            ))
    return docs

# ✅ 7. Streamlit UI
st.set_page_config(page_title="성취기준 추천기", page_icon="🎯")
st.title("🎯 성취기준 추천기")

tab1, tab2, tab3 = st.tabs(["🧒 초등학교", "🏫 중학교", "🎓 고등학교"])

# ✅ 초등학교 탭
with tab1:
    st.markdown("**수업 활동을 입력하면, 관련된 초등학교 성취기준을 추천합니다.**")
    grade_options = ["1~2학년", "3~4학년", "5~6학년"]
    subject_options = ["국어", "수학", "사회", "과학", "도덕", "체육", "음악", "미술", "실과"]
    selected_grade = st.selectbox("📘 학년 선택", grade_options, key="elem_grade")
    selected_subject = st.selectbox("📙 교과 선택", subject_options, key="elem_subject")
    user_input = st.text_area("📝 수업 활동을 입력하세요", height=150, key="elem_input")

    if st.button("🔍 성취기준 찾기", key="elem_search"):
        if not user_input.strip():
            st.warning("수업 활동 내용을 입력해주세요.")
        else:
            with st.spinner("AI가 성취기준을 찾고 있어요..."):
                filtered_docs = load_filtered_documents(ELEMENTARY_JSON_PATH, selected_grade, selected_subject)
                if not filtered_docs:
                    st.error(f"{selected_grade} {selected_subject} 성취기준이 없습니다.")
                else:
                    vectorstore = Chroma.from_documents(filtered_docs, embedding=embedding_model)
                    results_with_scores = vectorstore.similarity_search_with_score(user_input, k=10)

                    unique_contents = set()
                    final_results = []
                    for doc, score in results_with_scores:
                        content = doc.page_content.strip()
                        meta = doc.metadata
                        if meta.get("학년") == selected_grade and meta.get("교과") == selected_subject:
                            if content not in unique_contents:
                                unique_contents.add(content)
                                final_results.append((content, score))
                        if len(final_results) == 5:
                            break

                    if final_results:
                        st.subheader("📌 추천 성취기준")
                        for i, (content, score) in enumerate(final_results, 1):
                            st.markdown(f"**{i}.** {content}")
                            st.caption(f"🧠 유사도 점수: `{score:.3f}`")
                    else:
                        st.info("관련 성취기준을 찾을 수 없어요. 입력을 다시 시도해보세요.")

# ✅ 중학교 탭
with tab2:
    st.markdown("**수업 활동을 입력하면, 관련된 중학교 성취기준을 추천합니다.**")
    subject_options_m = ["과학", "미술", "수학"]
    selected_subject_m = st.selectbox("📙 교과 선택", subject_options_m, key="middle_subject")
    user_input_m = st.text_area("📝 수업 활동을 입력하세요", height=150, key="middle_input")

    if st.button("🔍 성취기준 찾기", key="middle_search"):
        if not user_input_m.strip():
            st.warning("수업 활동 내용을 입력해주세요.")
        else:
            with st.spinner("AI가 성취기준을 찾고 있어요..."):
                filtered_docs = load_filtered_documents_middle(MIDDLE_JSON_PATH, selected_subject_m)
                if not filtered_docs:
                    st.error(f"{selected_subject_m} 교과 성취기준이 없습니다.")
                else:
                    vectorstore = Chroma.from_documents(filtered_docs, embedding=embedding_model)
                    results_with_scores = vectorstore.similarity_search_with_score(user_input_m, k=10)

                    unique_contents = set()
                    final_results = []
                    for doc, score in results_with_scores:
                        content = doc.page_content.strip()
                        meta = doc.metadata
                        if meta.get("교과") == selected_subject_m:
                            if content not in unique_contents:
                                unique_contents.add(content)
                                final_results.append((content, score))
                        if len(final_results) == 5:
                            break

                    if final_results:
                        st.subheader("📌 추천 성취기준")
                        for i, (content, score) in enumerate(final_results, 1):
                            st.markdown(f"**{i}.** {content}")
                            st.caption(f"🧠 유사도 점수: `{score:.3f}`")
                    else:
                        st.info("관련 성취기준을 찾을 수 없어요. 입력을 다시 시도해보세요.")

# ✅ 고등학교 탭
with tab3:
    st.markdown("**수업 활동을 입력하면, 관련된 고등학교 성취기준을 추천합니다.**")
    subject_options_h = ["미술"]
    selected_subject_h = st.selectbox("📙 교과 선택", subject_options_h, key="high_subject")
    user_input_h = st.text_area("📝 수업 활동을 입력하세요", height=150, key="high_input")

    if st.button("🔍 성취기준 찾기", key="high_search"):
        if not user_input_h.strip():
            st.warning("수업 활동 내용을 입력해주세요.")
        else:
            with st.spinner("AI가 성취기준을 찾고 있어요..."):
                filtered_docs = load_filtered_documents_high(HIGH_JSON_PATH, selected_subject_h)
                if not filtered_docs:
                    st.error(f"{selected_subject_h} 교과 성취기준이 없습니다.")
                else:
                    vectorstore = Chroma.from_documents(filtered_docs, embedding=embedding_model)
                    results_with_scores = vectorstore.similarity_search_with_score(user_input_h, k=10)

                    unique_contents = set()
                    final_results = []
                    for doc, score in results_with_scores:
                        content = doc.page_content.strip()
                        meta = doc.metadata
                        if meta.get("교과") == selected_subject_h:
                            if content not in unique_contents:
                                unique_contents.add(content)
                                final_results.append((content, score))
                        if len(final_results) == 5:
                            break

                    if final_results:
                        st.subheader("📌 추천 성취기준")
                        for i, (content, score) in enumerate(final_results, 1):
                            st.markdown(f"**{i}.** {content}")
                            st.caption(f"🧠 유사도 점수: `{score:.3f}`")
                    else:
                        st.info("관련 성취기준을 찾을 수 없어요. 입력을 다시 시도해보세요.")