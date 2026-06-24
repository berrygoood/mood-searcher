import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
import io

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="Mood Searcher (무료 버전)", page_icon="🐱", layout="centered")

# 귀여운 키치 무드 스타일링 CSS
st.markdown("""
    <style>
    .main { background-color: #faf8f5; }
    h1 { color: #ff6b8b; font-family: 'Comic Sans MS', sans-serif; }
    .stButton>button { background-color: #ff87a0; color: white; border-radius: 20px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🐱 Mood Searcher ✨ (무료 버전)")
st.subheader("돈 안 쓰고 나만의 고유한 감성 보드 만들기")

# 사이드바에서 허깅페이스 키 받기
with st.sidebar:
    st.header("🔑 무료 설정")
    hf_token = st.text_input("Hugging Face 토큰을 입력하세요 (hf_...)", type="password")
    st.caption("허깅페이스 가입 후 무료로 발급받은 토큰을 넣으면 작동해요!")

if hf_token:
    # 허깅페이스 무료 인퍼런스 클라이언트 세팅
    client = InferenceClient(api_key=hf_token)
    
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

    if st.button("✨ 100% 무료 무드 보드 생성하기"):
        with st.spinner("무료 AI 엔진이 열심히 손그림을 그리고 있어... 🎨"):
            try:
                # 허깅페이스 FLUX 모델 맞춤형 키치/손그림 프롬프트
                prompt = f"A cute, kitsch, and simple hand-drawn illustration style mood board. " \
                         f"A person who likes {color} color, wants to go to {place}, and is listening to {music} music. " \
                         f"In a flat lay layout, cleanly arrange these items: {items}. " \
                         f"Minimal and clean pastel background, charming doodles, cozy aesthetic, charming cartoon style, no realism."

                # 무료 이미지 생성 모델 (FLUX.1-schnell 사용)
                image = client.text_to_image(
                    prompt=prompt,
                    model="black-forest-labs/FLUX.1-schnell"  # 현재 가장 성능 좋은 무료 모델 중 하나
                )
                
                # 결과 화면에 띄우기
                st.success("🎉 짜잔! 돈 한 푼 안 들고 너만의 무드 보드가 완성이 되었어!")
                st.image(image, caption="나의 고유한 분위기 (무료 무드서처 결과물)", use_column_width=True)
                
                # --- STEP 4: 확장 기능 ---
                st.subheader("📝 나의 감성 큐레이션")
                st.info(f"🎵 **오늘의 추천 스타일링 가이드:**\n"
                        f"오늘은 **{color}** 포인트가 들어간 룩에 **{place}**와 잘 어울리는 캐주얼한 무드를 추천해! "
                        f"**{music}**을(를) 들으며 개성 넘치는 하루를 보내봐!")
                
            except Exception as e:
                st.error(f"이미지 생성 중 오류가 발생했어: {e}")
else:
    st.warning("왼쪽 사이드바에 Hugging Face 토큰(hf_...)을 입력하면 무료 무드서처가 활성화돼! 🔑")
