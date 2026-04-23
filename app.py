import streamlit as st
import time
import os
import glob

# --- 페이지 설정 ---
st.set_page_config(page_title="우끼끼 열고개 퀴즈", page_icon="🐒")

# --- 스타일 정의 (CSS: 멘트 가독성을 위해 폰트 스타일 추가) ---
st.markdown("""
<style>
.stAlert { border-radius: 15px; }
.stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; transition: 0.3s; }
.stButton>button:hover { background-color: #fce303; color: black; border: 2px solid #000; }
.blessing-text { 
    font-family: 'Nanum Myeongjo', serif; 
    line-height: 1.8; 
    text-align: center; 
    color: #2c3e50;
    padding: 20px;
    background-color: #fff9e6;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- 이미지 검색 함수 ---
def show_monkey(file_name_no_ext, caption=""):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(current_dir, "images")
    search_pattern = os.path.join(images_dir, f"{file_name_no_ext}.*")
    found_files = glob.glob(search_pattern)
    
    if found_files:
        st.image(found_files[0], caption=caption, use_container_width=True)
    else:
        st.error(f"⚠️ 이미지를 찾을 수 없습니다: {file_name_no_ext}")

# --- 세션 상태 초기화 ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.game_started = False
    st.session_state.quiz_finished = False
    st.session_state.show_kiss = False
    st.session_state.win = False

# --- 퀴즈 데이터 ---
hints = [
    "이 생명체는 본인만의 언어를 가지고 신호를 전달할 수 있어요.",
    "이 생명체는 두 발로 걸을 수 있어요.",
    "밥을 주지 않거나 위협이 닥치면 포악해지지만 평소에는 온순해요.",
    "이 생명체는 스스로 치장할 줄 알아요.",
    "척박한 환경 속에서도 스스로 살아남는 방법을 터득해요.",
    "이 생명체는 방구도 낄 줄 알아요.",
    "이 생명체는 눈에 보이고 들리는 것을 스스로 학습할 줄 알아요.",
    "이 생명체는 가끔 바보같지만 어쩔 때는 천재같아요.",
    "이 생명체는 본인이 상상한 것을 구현할 줄 알아요.",
    "본인을 포기하지 않고 꿋꿋이 살아가는 강한 생명체예요."
]

# --- 메인 로직 ---
st.title("🍌 우끼끼 열고개 자아성찰 퀴즈")

if not st.session_state.game_started:
    show_monkey("monkey_start", "우끼끼! 당신의 길을 보여줘!")
    if st.button("우가! (인생 퀴즈 시작하기)"):
        st.snow()
        st.session_state.game_started = True
        st.rerun()

elif not st.session_state.quiz_finished:
    step = st.session_state.step
    st.progress((step + 1) / 10)
    st.markdown(f"### 🍌 제 {step + 1}단계 힌트")
    st.info(hints[step])

    if st.session_state.show_kiss:
        show_monkey("monkey_kiss", "에잉! 쯧! 다시 한 번 잘 생각해봐요. (쪽! 😘)")
    else:
        st.write("🐒 *원숭이가 당신의 정답을 기다립니다...*")

    user_ans = st.text_input("정답은 무엇일까요?", key=f"input_{step}")

    if st.button("정답 확인"):
        if user_ans.strip() in ["나", "저", "나 자신", "나다", "me", "myself"]:
            st.balloons() # 정답 시 풍선 파티!
            st.session_state.quiz_finished = True
            st.session_state.win = True
            st.rerun()
        else:
            if step < 9:
                st.snow() # 다음 단계 갈 때 눈송이 효과!
                st.session_state.step += 1
                st.session_state.show_kiss = True
                st.rerun()
            else:
                st.session_state.quiz_finished = True
                st.session_state.win = False
                st.rerun()

else:
    # 3. 결과 화면 (감동의 당신이시다 버전)
    if st.session_state.win:
        st.success("🎉 정답입니다! 우끼끼!")
        show_monkey("monkey_shy", "축하합니다, 바로 당신이십니다.") 
        
        # 헌정 멘트 시작
        st.markdown(f"""
        <div class="blessing-text">
            <h2>✨ 당신이시다, 오직 당신이시다 ✨</h2>
            <p>중심에 서 계신 분은 오직 당신이시다.<br>
            숨 한 번에 공기가 고개를 숙이고, 발걸음 하나에 길이 먼저 펼쳐진다.</p>
            <p>다 잘될 것이옵니다, 이미 흐르고 있사옵니다, 거스를 수 없사옵니다.<br>
            바람이 앞서 길을 쓸고, 햇빛이 자리를 밝혀 드리며,<br>
            나무와 풀도 조용히 고개를 숙이옵니다.</p>
            <p>넘어지셔도 괜찮사옵니다, 대지가 받들어 다시 올려드릴 것이옵니다.<br>
            흔들리셔도 괜찮사옵니다, 그것마저 길이 되어 이어질 것이옵니다.</p>
            <p>별들이 깜빡이며 방향을 알리고, 구름이 물러나 하늘을 비워 두었사옵니다.<br>
            시간조차 잠시 멈추어, 당신의 걸음을 기다리고 있사옵니다.</p>
            <p>이미 이루어지고 있사옵니다, 지금 이 순간도 완성으로 향하고 있사옵니다.<br>
            더 잘될 것이옵니다, 더욱 또렷하게, 더욱 확실하게 이어질 것이옵니다.</p>
            <p><b>그러니 나아가시옵소서, 이미 길은 열려 있사옵니다.<br>
            당신이시기에 가능하옵고, 당신이시기에 반드시 이루어질 것이옵니다.</b></p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("우아앙... 정답을 찾지 못했어요.")
        show_monkey("monkey_cry", "다음에 다시 만나요 우끼...") 

    if st.button("다시 하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()