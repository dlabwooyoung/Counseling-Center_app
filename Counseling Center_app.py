import streamlit as st
import random
import numpy as np
from scipy.io.wavfile import write
import os
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="고민 해결 센터",
    page_icon="🎯",
    layout="centered"
)

# 다크 테마 CSS 설정
st.markdown("""
    <style>
        :root {
            --primary-color: #FF0000;
            --background-color: #1a1a1a;
            --secondary-background-color: #262626;
            --text-color: #ffffff;
        }

        body {
            background-color: #1a1a1a;
            color: #ffffff;
        }

        .stTextInput > div > div > input {
            background-color: #2a2a2a;
            color: #ffffff;
            border: 2px solid #444;
            font-weight: 600;
        }

        .stButton > button {
            background-color: #FF6B6B;
            color: #ffffff;
            font-weight: 700;
            font-size: 18px;
            border-radius: 8px;
            border: none;
            padding: 12px 30px;
            width: 100%;
        }

        .stButton > button:hover {
            background-color: #FF8787;
            transform: scale(1.02);
        }

        h1, h2, h3, p, label {
            color: #ffffff;
            font-weight: 600;
        }

        .success-box {
            background-color: #2a2a2a;
            border: 2px solid #4CAF50;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }

        .answer-text {
            color: #FFD700;
            font-weight: 700;
            font-size: 24px;
            text-align: center;
            padding: 20px;
            animation: pulse 0.5s ease-in-out;
        }

        @keyframes pulse {
            0% { opacity: 0; }
            50% { opacity: 1; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# 어이없는 대답 목록
RIDICULOUS_ANSWERS = [
    "🤔 그건... 역으로 생각해봐. 네가 물음표라고 생각하고 살아봐.",
    "💡 답은 간단해. 넌 이미 알고 있었어.",
    "🎯 그 고민? 뭐... 그냥 웃고 넘어가.",
    "🚀 해결책: 3초 동안 눈을 감아봐.",
    "🎪 너의 고민은 실은... 당신의 착각일지도?",
    "🔮 내 구슬이 말한다: 다음 달에 좋아질 거야.",
    "🌙 밤하늘이 답변한다: 뭐... 그렇고 그런 거 아냐?",
    "⭐ 해결책: 너를 믿어봐. (아무도 안 도와줄 거니까)",
    "🎭 모든 문제는 마음가짐의 문제다. 긍정해!",
    "🎨 그 문제를 다르게 봐봐. 예를 들어... 예술작품처럼?",
    "🏰 고민같은 건... 성에 갇힌 고통일 뿐이야.",
    "🍕 피자를 먹어봤어? 아, 그게 답이구나.",
    "🚁 그냥 떠나버려. (도망)",
    "🎪 웃음이 최고의 약이라던데... 웃기만 해봐.",
    "🧘 명상해. 그러면... 문제가 아니게 되지.",
]

# 뾰로롱 효과음 생성 함수
def generate_zzingarum_sound():
    """뾰로롱 효과음 생성"""
    sample_rate = 22050
    duration = 0.6
    t = np.linspace(0, duration, int(sample_rate * duration))

    # 뾰로롱 소리: 주파수가 올라갔다 내려가는 느낌
    freq_start = 400
    freq_end = 800
    freq_mid = 1000

    # 3음절의 뾰-로-롱 효과
    sound = np.zeros_like(t)

    # 뾰 (상승)
    t1 = t < 0.2
    sound[t1] = 0.3 * np.sin(2 * np.pi * np.linspace(freq_start, freq_mid, t1.sum()) * t[t1])

    # 로 (하강)
    t2 = (t >= 0.2) & (t < 0.4)
    sound[t2] = 0.3 * np.sin(2 * np.pi * np.linspace(freq_mid, freq_end, t2.sum()) * t[t2])

    # 롱 (상승)
    t3 = t >= 0.4
    sound[t3] = 0.3 * np.sin(2 * np.pi * np.linspace(freq_end, freq_mid, t3.sum()) * t[t3])

    # 진폭 조절 (페이드 아웃)
    envelope = np.exp(-t * 3)
    sound = sound * envelope

    # 음성 정규화
    sound = (sound / np.max(np.abs(sound))) * 0.9

    return (sound * 32767).astype(np.int16), sample_rate

# 효과음 파일 생성 및 캐싱
sound_path = "zzingarum_sound.wav"
if not os.path.exists(sound_path):
    sound, sr = generate_zzingarum_sound()
    write(sound_path, sr, sound)

# UI 구성
st.markdown("<h1 style='text-align: center; color: #FFD700; font-weight: 900;'>🎯 고민 해결 센터 🎯</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #BBB; font-size: 16px;'>당신의 모든 고민을 해결해드립니다!</p>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)

# 고민 입력
st.markdown("<p style='font-weight: 700; font-size: 18px;'>💭 당신의 고민을 말씀해주세요:</p>", unsafe_allow_html=True)
concern = st.text_input(
    label="고민",
    label_visibility="collapsed",
    placeholder="예: 너무 피곤해... 뭘 해야 할까?"
)

# 해결 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    solve_button = st.button("🚀 해결해주기", use_container_width=True)

# 해결 로직
if solve_button:
    if concern.strip():
        # 어이없는 대답 선택
        answer = random.choice(RIDICULOUS_ANSWERS)

        # 효과음 재생
        st.audio(sound_path, format="audio/wav", autoplay=True)

        # 대답 표시
        st.markdown("<div class='success-box'>", unsafe_allow_html=True)
        st.markdown(f"<div class='answer-text'>{answer}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 성공 메시지
        st.markdown(
            "<p style='text-align: center; color: #4CAF50; font-weight: 700; font-size: 18px; margin-top: 20px;'>"
            "✨ 축하합니다! 고민이 해결되었습니다! ✨"
            "</p>",
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ 고민을 입력해주세요!")

st.markdown("<hr style='border: 1px solid #444; margin-top: 40px;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #999; font-size: 12px; margin-top: 30px;'>"
    "© 2026 어이없는 상담 센터 | 진지한 상담이 필요하시면 전문가를 찾아주세요."
    "</p>",
    unsafe_allow_html=True
)
