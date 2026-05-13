import platform
from datetime import datetime

import streamlit as st


st.set_page_config(
    page_title="EC2 Streamlit Demo",
    page_icon="☁️",
    layout="wide",
)


def build_message(name: str, topic: str, style: str) -> str:
    clean_name = name.strip() or "방문자"
    clean_topic = topic.strip() or "FastAPI와 연동할 기능"
    return (
        f"{clean_name}님, EC2에 배포된 Streamlit 앱이 정상적으로 동작하고 있습니다. "
        f"다음 단계에서는 '{clean_topic}' 주제로 {style} 형태의 기능을 붙여볼 수 있습니다."
    )


st.title("EC2 Streamlit Demo")
st.caption("오픈소스소프트웨어실습 실습 3: EC2 배포 확인용 기본 앱")

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.subheader("간단한 입력")
    name = st.text_input("이름", placeholder="예: 홍길동")
    topic = st.text_input(
        "다음 단계에서 붙여보고 싶은 기능",
        placeholder="예: 감정 분석, 요약, 추천",
    )
    style = st.selectbox(
        "출력 스타일",
        ["간단한 안내", "체크리스트", "짧은 소개 문구"],
        index=0,
    )

    if st.button("결과 생성", type="primary", use_container_width=True):
        st.session_state["result"] = build_message(name, topic, style)
        st.session_state.setdefault("history", []).append(
            {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": name.strip() or "방문자",
                "topic": topic.strip() or "미입력",
            }
        )

    result = st.session_state.get("result")
    if result:
        st.success(result)
        if style == "체크리스트":
            st.markdown(
                f"""
                - 사용자: `{name.strip() or "방문자"}`
                - 주제: `{topic.strip() or "미입력"}`
                - 상태: `EC2 배포 확인 완료`
                """
            )
        elif style == "짧은 소개 문구":
            st.info(
                f"이 앱은 EC2에서 실행 중이며, '{topic.strip() or '추가 기능'}' 같은 다음 단계 확장을 염두에 둔 데모입니다."
            )

with right:
    st.subheader("배포 상태")
    st.metric("앱 포트", "8501")
    st.metric("Python", platform.python_version())
    st.metric("플랫폼", platform.system())

st.divider()
st.subheader("실행 기록")
history = st.session_state.get("history", [])
if history:
    st.dataframe(history, use_container_width=True, hide_index=True)
else:
    st.write("아직 생성된 결과가 없습니다. 왼쪽 입력 폼을 사용해 보세요.")
