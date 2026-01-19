import streamlit as st
import lunar_python
import random
import time
import os
import google.generativeai as genai
from datetime import datetime  # 修复点：引入标准时间库

# ================= 配置区 =================
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

if API_KEY:
    genai.configure(api_key=API_KEY)
    AI_MODE = True
else:
    AI_MODE = False

# ================= 页面样式 =================
st.set_page_config(page_title="一句顶一万句", page_icon="🔮", layout="centered")

st.markdown("""
<style>
    .stApp {background-color: #000000; color: #e0e0e0;}
    .stTextInput > div > div > input {
        color: #00ff00; 
        background-color: #0d1117; 
        border: 1px solid #30363d;
        font-family: 'Courier New';
    }
    .stButton > button {
        width: 100%;
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
        font-family: 'Courier New';
    }
    .oracle-text {
        font-family: 'Songti SC', 'SimSun', serif; 
        font-size: 28px; 
        color: #ffffff; 
        text-align: center; 
        padding: 40px 20px;
        border-top: 1px solid #333;
        border-bottom: 1px solid #333;
        margin-top: 20px;
        line-height: 1.5;
        text-shadow: 0 0 10px #ffffff55;
    }
    .footer {text-align: center; color: #444; font-size: 12px; margin-top: 50px;}
</style>
""", unsafe_allow_html=True)

# ================= 核心逻辑 =================

def get_bazi_info():
    """获取当前时空的能量坐标（八字）"""
    # 修复点：这里把 time.localtime() 改为了 datetime.now()
    solar = lunar_python.Solar.fromDate(datetime.now())
    lunar = solar.getLunar()
    bazi = lunar.getBaZi()
    return f"{bazi[0]}年 {bazi[1]}月 {bazi[2]}日 {bazi[3]}时"

def ask_ai_oracle(question, bazi):
    """真·AI 算命逻辑"""
    if not AI_MODE:
        mock_answers = [
            "局势如雾，但东南方有微光。此时静默胜过行动，三日后自有转机。",
            "火入乾宫，看似危机四伏，实则只需破釜沉舟。除了你自己，无人能阻你。",
            "卦象显示大吉。你担心的那个人，其实也在等你迈出第一步。",
            "利在这一刻。不要犹豫，那个看似疯狂的决定，才是唯一的正解。",
            "玄武临门，需防口舌之争。闭嘴做事，这就是你赢过他们的唯一方式。"
        ]
        time.sleep(1.5)
        return random.choice(mock_answers)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        你是一位精通奇门遁甲和现代心理学的隐世大师。
        用户问："{question}"
        当前时间八字：{bazi}
        
        请用【一句顶一万句】的风格回答。
        要求：
        1. 必须简短、有力、神秘，不超过40个字。
        2. 必须包含一个具体的行动指引（如方位、颜色、时间）。
        3. 语气要绝对自信，不准用"可能"、"也许"。
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "天机混沌，信号干扰。请稍后再试。"

# ================= 界面交互 =================

st.title("⛩️ 一句顶一万句")
st.caption("AI Oracle v1.0 // 时空决策机")

question = st.text_input("", placeholder="在此输入你的困惑...")

if st.button("断"):
    if not question:
        st.warning("心不诚，则卦不灵。请输入问题。")
    else:
        progress_text = st.empty()
        bar = st.progress(0)
        
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
            if i == 20: progress_text.text("正在校准真太阳时...")
            if i == 50: progress_text.text("正在排布奇门九宫...")
            if i == 80: progress_text.text("正在接入高维意识...")
        
        bar.empty()
        progress_text.empty()
        
        try:
            bazi = get_bazi_info()
            answer = ask_ai_oracle(question, bazi)
            st.markdown(f'<div class="oracle-text">{answer}</div>', unsafe_allow_html=True)
            with st.expander("查看底层数据流"):
                st.code(f"Time_Coordinate: {bazi}\nModel: Gemini-Pro\nStatus: Online", language="yaml")
        except Exception as e:
            st.error(f"运行时错误: {e}")

st.markdown('<div class="footer">Powered by Gemini & 奇门遁甲算法</div>', unsafe_allow_html=True)
