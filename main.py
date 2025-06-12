import os
import json
import numpy as np
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

# ✅ 4. 코사인 유사도 계산 함수
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# ✅ 5. 필터링 함수
def load_filtered_documents(json_path, selected_grade=None, selected_subject=None):
    docs = []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if selected_grade:  # 초등
        if selected_grade in data and selected_subject in data[selected_grade]:
            for content in data[selected_grade][selected_subject]:
                docs.append(Document(
                    page_content=content,
                    metadata={"학년": selected_grade, "교과": selected_subject}
                ))
    else:  # 중/고등
        if selected_subject in data:
            for content in data[selected_subject]:
                docs.append(Document(
                    page_content=content,
                    metadata={"교과": selected_subject}
                ))
    return docs

# ✅ 6. Streamlit UI
st.set_page_config(page_title="성취기준 추천기", page_icon="🎯")
st.title("🎯 성취기준 추천기")

tab1, tab2, tab3 = st.tabs(["🧒 초등학교", "🏫 중학교", "🎓 고등학교"])

# ✅ 공통 추천 함수
def recommend_standard(user_input, filtered_docs, target_meta_key, target_meta_val):
    query_vector = embedding_model.embed_query(user_input)
    vectorstore = Chroma.from_documents(filtered_docs, embedding=embedding_model)
    results = vectorstore.similarity_search(user_input, k=10)

    unique_contents = set()
    final_results = []
    for doc in results:
        content = doc.page_content.strip()
        meta = doc.metadata
        if meta.get(target_meta_key) == target_meta_val and content not in unique_contents:
            doc_vector = embedding_model.embed_query(content)
            sim_score = cosine_similarity(query_vector, doc_vector)
            unique_contents.add(content)
            final_results.append((content, sim_score))
        if len(final_results) == 5:
            break
    return final_results

# ✅ 초등학교 탭
with tab1:
    st.markdown("**수업 활동을 입력하면, 관련된 초등학교 성취기준을 추천합니다.**")
    grade_options = ["1~2학년", "3~4학년", "5~6학년"]
    subject_options = ["국어", "수학", "사회", "과학", "도덕", "체육", "음악", "미술", "실과"]
    selected_grade = st.selectbox("📘 학년 선택", grade_options)
    selected_subject = st.selectbox("📙 교과 선택", subject_options)
    user_input = st.text_area("📝 수업 활동을 입력하세요", height=150, key="elem_input")

    if st.button("🔍 성취기준 찾기"):
        if not user_input.strip():
            st.warning("수업 활동 내용을 입력해주세요.")
        else:
            with st.spinner("AI가 성취기준을 찾고 있어요..."):
                docs = load_filtered_documents(ELEMENTARY_JSON_PATH, selected_grade, selected_subject)
                results = recommend_standard(user_input, docs, "교과", selected_subject)
                if results:
                    st.subheader("📌 추천 성취기준")
                    for i, (content, score) in enumerate(results, 1):
                        st.markdown(f"**{i}.** {content}")
                        st.caption(f"🧠 코사인 유사도: `{score:.3f}`")
                else:
                    st.info("관련 성취기준을 찾을 수 없어요.")

# ✅ 중학교 탭
with tab2:
    st.markdown("**수업 활동을 입력하면, 관련된 중학교 성취기준을 추천합니다.**")
    subject_options_m = ["과학", "미술", "수학"]
    selected_subject_m = st.selectbox("📙 교과 선택", subject_options_m)
    user_input_m = st.text_area("📝 수업 활동을 입력하세요", height=150, key="middle_input")

    if st.button("🔍 성취기준 찾기", key="middle"):
        if not user_input_m.strip():
            st.warning("수업 활동 내용을 입력해주세요.")
        else:
            with st.spinner("AI가 성취기준을 찾고 있어요..."):
                docs = load_filtered_documents(MIDDLE_JSON_PATH, selected_subject=selected_subject_m)
                results = recommend_standard(user_input_m, docs, "교과", selected_subject_m)
                if results:
                    st.subheader("📌 추천 성취기준")
                    for i, (content, score) in enumerate(results, 1):
                        st.markdown(f"**{i}.** {content}")
                        st.caption(f"🧠 코사인 유사도: `{score:.3f}`")
                else:
                    st.info("관련 성취기준을 찾을 수 없어요.")

# ✅ 고등학교 탭
with tab3:
    st.markdown("**수업 활동을 입력하면, 관련된 고등학교 성취기준을 추천합니다.**")
    subject_options_h = ["미술"]
    selected_subject_h = st.selectbox("📙 교과 선택", subject_options_h)
    user_input_h = st.text_area("📝 수업 활동을 입력하세요", height=150, key="high_input")

    if st.button("🔍 성취기준 찾기", key="high"):
        if not user_input_h.strip():
            st.warning("수업 활동 내용을 입력해주세요.")
        else:
            with st.spinner("AI가 성취기준을 찾고 있어요..."):
                docs = load_filtered_documents(HIGH_JSON_PATH, selected_subject=selected_subject_h)
                results = recommend_standard(user_input_h, docs, "교과", selected_subject_h)
                if results:
                    st.subheader("📌 추천 성취기준")
                    for i, (content, score) in enumerate(results, 1):
                        st.markdown(f"**{i}.** {content}")
                        st.caption(f"🧠 코사인 유사도: `{score:.3f}`")
                else:
                    st.info("관련 성취기준을 찾을 수 없어요.")