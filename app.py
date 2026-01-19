import streamlit as st
import lunar_python
import google.generativeai as genai
from datetime import datetime
import time

# ================= 1. 配置与连接 =================
# 获取 Key
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# 配置 AI
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        AI_MODE = True
    except Exception as e:
        st.error(f"API Key 配置异常: {e}")
        AI_MODE = False
else:
    AI_MODE = False

# ================= 2. 页面样式 (黑客风) =================
st.set_page_config(page_title="一句顶一万句", page_icon="⛩️", layout="centered")
st.markdown("""
<style>
    .stApp {background-color: #0e1117; color: #e0e0e0;}
    .stTextInput > div > div > input {
        color: #00ff41; 
        background-color: #000000; 
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
        font-family: 'Songti SC', serif; 
        font-size: 28px; 
        color: #ffffff; 
        text-align: center; 
        padding: 40px;
        border: 1px solid #333;
        background-color: #161b22;
        margin-top: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. 核心功能 =================

def get_bazi():
    """获取八字"""
    now = datetime.now()
    solar = lunar_python.Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, now.second)
    lunar = solar.getLunar()
    bazi = lunar.getBaZi()
    return f"{bazi[0]}年 {bazi[1]}月 {bazi[2]}日 {bazi[3]}时"

def ask_oracle(question, bazi):
    """AI 算命逻辑"""
    if not AI_MODE:
        return "⚠️ 灵魂未注入：请在 Streamlit Secrets 填入 GEMINI_API_KEY"
    
    try:
        # 【关键】使用最稳的 1.5-flash 模型（免费且新驱动支持）
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        角色：精通奇门遁甲与赛博心理学的隐世大师。
        用户问："{question}"
        当前八字：{bazi}
        
        请输出【一句顶一万句】的判词。
        要求：
        1. 40字以内，简短有力，冷峻神秘。
        2. 必须包含一个行动指引（方位/颜色/物品/时间）。
        3. 拒绝模棱两可，直指核心。
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"连接受阻: {e}"

# ================= 4. 界面交互 =================

st.title("⛩️ 一句顶一万句")
st.caption("Cyber Oracle v3.0 // Powered by Gemini 1.5")

question = st.text_input("", placeholder="在此键入你的困惑...")

if st.button("断"):
    if not question:
        st.warning("无问则无解。")
    else:
        with st.spinner("正在链接高维时空..."):
            # 仪式感延迟
            time.sleep(0.8)
            
            # 执行预测
            bazi = get_bazi()
            answer = ask_oracle(question, bazi)
            
            # 显示结果
            st.markdown(f'<div class="oracle-text">{answer}</div>', unsafe_allow_html=True)
            
            # 调试信息 (折叠)
            with st.expander("🔍 查看底层数据"):
                st.text(f"八字坐标: {bazi}")
                st.text(f"模型版本: gemini-1.5-flash (Status: Active)")
