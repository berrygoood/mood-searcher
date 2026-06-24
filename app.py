import streamlit as st
from openai import OpenAI
import requests

# 1. 웹페이지 기본 설정 (타이틀 및 아이콘)
st.set_page_config(page_title="Mood Searcher", page_icon="✨", layout="centered")

# 디자인을 조금 더 귀엽고 깔끔하게 다듬는 CSS
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    h1 { color: #ff6b6b; font-family: 'Comic Sans MS', sans-serif; }
    .stButton>button { background-color: #ff8787; color: white; border-radius: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🐱 Mood Searcher ✨")
st.subheader("나만의 고유한 분위기를 시각적인 콘텐츠로 기록하기")

# 사이드바에서 API 키 입력 받기
with st.sidebar:
    st.header("🔑 설정")
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
    st.caption("DALL-E 이미지 생성을 위해 API 키가 필요합니다.")

# API 키가 있을 때만 작동하도록 설정
if api_key:
    client = OpenAI(api_key=api_key)
    
    # --- STEP 1: 대화 및 분석 ---
    st.header("💬 Step 1. 오늘의 무드 토크")
    
    col1, col2 = st.columns(2)
    with col1:
        color = st.selectbox("오늘 끌리는 색감은?", ["파스텔 핑크", "레몬 옐로우", "차분한 네이비", "싱그러운 초록", "모노톤 블랙/화이트"])
    with col2:
        place = st.text_input("오늘 가장 가고 싶은 장소는?", placeholder="예: 아기자기한 소품샵, 한적한 한강공원")
        
    music = st.radio("지금 듣고 싶은 음악 스타일은?", ["신나는 아이돌 팝", "잔잔한 인디 어쿠스틱", "힙한 알앤비/시티팝", "조용한 클래식/재즈"])

    # --- STEP 2 & 3: 키워드 입력 및 생성 ---
    st.header("🎒 Step 2. 왓츠 인 마이 백 & 스타일")
    items = st.text_area("오늘의 착장이나 가방 속 소지품 키워드를 적어줘!", 
                         placeholder="예: 필통, 유선 이어폰, 고양이 키링, 에어팟, 다이어리, 뿔테 안경")

    if st.button("✨ 나의 무드 보드 생성하기"):
        with st.spinner("너의 분위기를 수집해서 귀여운 일러스트를 그리고 있어... 🎨"):
            try:
                # DALL-E에 보낼 프롬프트 엔지니어링 (사용자가 요청한 '키치, 귀엽고 단순한 손그림' 반영)
                prompt = f"A cute, kitsch, and simple hand-drawn illustration style mood board. " \
                         f"The overall vibe is inspired by a person who likes {color} color, wants to go to {place}, and is listening to {music} music. " \
                         f"In a flat lay layout, cleanly arrange these items: {items}. " \
                         f"Minimal and clean pastel background, doodles, charming and cozy aesthetic, charming cartoon style, no realistic or complex shading."

                # 이미지 생성 요청 (DALL-E 3 사용)
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
                
                image_url = response.data[0].url
                
                # 결과 화면에 띄우기
                st.success("🎉 짜잔! 너만의 무드 보드가 완성되었어!")
                st.image(image_url, caption="나의 고유한 분위기 (Mood Searcher 결과물)", use_column_width=True)
                
                # --- STEP 4: 확장 기능 (감성 큐레이션 카드) ---
                st.subheader("📝 나의 감성 큐레이션")
                st.info(f"🎵 **오늘의 추천 스타일링 가이드:**\n"
                        f"오늘은 **{color}** 포인트가 들어간 룩에 **{place}**와 잘 어울리는 캐주얼한 무드를 추천해! "
                        f"**{music}**을(를) 들으며 나만의 개성 넘치는 하루를 보내봐!")
                
            except Exception as e:
                st.error(f"이미지 생성 중 오류가 발생했어: {e}")
else:
    st.warning("왼쪽 사이드바에 OpenAI API Key를 입력하면 무드서처가 활성화돼! 🔑")
