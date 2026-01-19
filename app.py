import streamlit as st
import lunar_python
import google.generativeai as genai
from datetime import datetime
import time

# ================= 配置区 =================
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        AI_MODE = True
    except Exception as e:
        st.error(f"API Key 配置错误: {e}")
        AI_MODE = False
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
    }
    .oracle-text {
        font-family: 'Songti SC', 'SimSun', serif; 
        font-size: 26px; 
        color: #ffffff; 
        text-align: center; 
        padding: 30px;
        border: 1px solid #333;
        margin-top: 20px;
        line-height: 1.5;
        text-shadow: 0 0 10px #ffffff55;
    }
    .footer {text-align: center; color: #444; font-size: 12px; margin-top: 50px;}
</style>
""", unsafe_allow_html=True)

# ================= 核心逻辑 =================

def get_bazi_info():
    """获取当前八字"""
    now = datetime.now()
    solar = lunar_python.Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, now.second)
    lunar = solar.getLunar()
    bazi = lunar.getBaZi()
    return f"{bazi[0]}年 {bazi[1]}月 {bazi[2]}日 {bazi[3]}时"

def ask_ai_oracle(question, bazi):
    """AI 算命"""
    if not AI_MODE:
        return "⚠️ 请先配置 API Key"
    
    try:
        # === 重点：这里换成了你账号里可用的 gemini-2.0-flash ===
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        你是一位精通奇门遁甲和现代心理学的隐世大师。
        用户问："{question}"
        当前八字：{bazi}
        
        请用【一句顶一万句】的风格回答。
        要求：
        1. 必须简短、有力、神秘，不超过40个字。
        2. 必须包含一个具体的行动指引（如方位、颜色、时间）。
        3. 语气要绝对自信，不准用"可能"、"也许"。
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"天机泄露太多，被拦截了 ({e})"

# ================= 界面交互 =================

st.title("⛩️ 一句顶一万句")
st.caption("Powered by Gemini 2.0 Flash")

question = st.text_input("", placeholder="在此输入你的困惑...")

if st.button("断"):
    if not question:
        st.warning("请输入问题。")
    else:
        progress_text = st.empty()
        bar = st.progress(0)
        
        # 模拟仪式感
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
        
        bar.empty()
        
        try:
            bazi = get_bazi_info()
            answer = ask_ai_oracle(question, bazi)
            st.markdown(f'<div class="oracle-text">{answer}</div>', unsafe_allow_html=True)
            
            with st.expander("查看底层数据流"):
                st.code(f"Time: {bazi}\nModel: Gemini-2.0-Flash\nStatus: Connected", language="yaml")
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('<div class="footer">v2.0.0 | 时空能量由 Gemini 2.0 提供</div>', unsafe_allow_html=True)
