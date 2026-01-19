import streamlit as st
import lunar_python
import google.generativeai as genai
from datetime import datetime
import time

# ================= 配置区 =================
# 获取 Key
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# 配置 AI
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
    .stTextInput > div > div > input {color: #00ff00; background-color: #0d1117; border: 1px solid #30363d;}
    .stButton > button {width: 100%; background-color: #21262d; color: #c9d1d9;}
    .oracle-text {font-size: 26px; color: #ffffff; text-align: center; padding: 30px; border: 1px solid #333; margin-top: 20px;}
</style>
""", unsafe_allow_html=True)

# ================= 核心逻辑 =================
def get_bazi_info():
    """获取八字 (已修复崩溃 bug)"""
    # 强制使用当前时间，修复 AttributeError
    now = datetime.now() 
    solar = lunar_python.Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, now.second)
    lunar = solar.getLunar()
    bazi = lunar.getBaZi()
    return f"{bazi[0]}年 {bazi[1]}月 {bazi[2]}日 {bazi[3]}时"

def ask_ai_oracle(question, bazi):
    """AI 算命"""
    if not AI_MODE:
        return "⚠️ 未检测到有效的 API Key，请在 Streamlit Secrets 中配置。"
    
    try:
        # 使用更通用的模型名称
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        你是一位精通奇门遁甲的大师。
        用户提问："{question}"
        当前八字：{bazi}
        请用一句简短、神秘、包含具体行动建议（方位/颜色/时间）的话回答。
        字数限制：40字以内。
        语气：绝对自信。
        """
        response = model.generate_content(prompt)
        if response.text:
            return response.text
        else:
            return "星象模糊，未能获取结果。"
    except Exception as e:
        # 这里会直接把错误打印出来，方便我们找原因
        return f"连接失败 (Error): {str(e)}"

# ================= 界面交互 =================
st.title("⛩️ 一句顶一万句")
question = st.text_input("", placeholder="在此输入你的困惑...")

if st.button("断"):
    if not question:
        st.warning("请输入问题。")
    else:
        with st.spinner('正在排盘...'):
            try:
                bazi = get_bazi_info()
                answer = ask_ai_oracle(question, bazi)
                st.markdown(f'<div class="oracle-text">{answer}</div>', unsafe_allow_html=True)
                
                # 调试信息 (方便你看是不是真的算出来了)
                with st.expander("查看天机 (Debug)"):
                    st.write(f"八字: {bazi}")
                    if "Error" in answer:
                        st.error("AI 报错了，请截图发给技术支持。")
            except Exception as e:
                st.error(f"程序崩溃: {e}")
