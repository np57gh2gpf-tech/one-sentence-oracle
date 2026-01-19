import streamlit as st
import lunar_python
import google.generativeai as genai
from datetime import datetime
import time

# ================= 配置区 =================
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ================= 页面样式 =================
st.set_page_config(page_title="一句顶一万句", page_icon="⛩️", layout="centered")
st.markdown("""
<style>
    .stApp {background-color: #0e1117; color: #e0e0e0;}
    .stTextInput > div > div > input {
        color: #00ff41; background-color: #000000; border: 1px solid #30363d; font-family: 'Courier New';
    }
    .stButton > button {
        width: 100%; background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d;
    }
    .oracle-text {
        font-family: 'Songti SC', serif; font-size: 26px; color: #ffffff; 
        text-align: center; padding: 30px; border: 1px solid #333; 
        background-color: #161b22; margin-top: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ================= 智能模型选择逻辑 =================
def find_working_model():
    """自动寻找可用的模型，不再盲猜"""
    if not API_KEY:
        return None, "请配置 API Key"
    
    genai.configure(api_key=API_KEY)
    
    # 优先尝试列表（根据你的截图定制）
    priority_list = [
        "gemini-2.0-flash-exp",           # 免费体验版 (最推荐)
        "gemini-2.0-flash-lite-preview-02-05", # 轻量预览版
        "gemini-1.5-flash",               # 经典版
        "gemini-1.5-pro",
        "gemini-exp-1206"
    ]
    
    # 1. 先试优先列表
    for model_name in priority_list:
        try:
            model = genai.GenerativeModel(model_name)
            # 发送一个极简请求测试是否通
            model.generate_content("test")
            return model_name, None # 成功找到！
        except Exception:
            continue # 失败就试下一个
            
    # 2. 如果优先列表都挂了，就遍历所有可用模型
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                try:
                    model = genai.GenerativeModel(m.name)
                    model.generate_content("test")
                    return m.name, None # 找到了
                except:
                    continue
    except Exception as e:
        return None, f"遍历失败: {str(e)}"

    return None, "未找到任何可用模型，请检查 API Key 权限。"

# ================= 核心业务 =================
def get_bazi():
    now = datetime.now()
    solar = lunar_python.Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, now.second)
    lunar = solar.getLunar()
    bazi = lunar.getBaZi()
    return f"{bazi[0]}年 {bazi[1]}月 {bazi[2]}日 {bazi[3]}时"

def ask_oracle(question, model_name):
    try:
        model = genai.GenerativeModel(model_name)
        prompt = f"""
        你是一位世界顶级奇门遁甲风水大师，深度学习了各种命理之书，开始排盘算命。用户问："{question}"
        请用【一句顶一万句】风格回答：简短（40字内）、冷峻、包含具体行动指引（方位/颜色）。
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"连接中断: {e}"

# ================= 交互界面 =================
st.title("⛩️ 一句顶一万句")

# 自动检测模型状态
if 'working_model' not in st.session_state:
    with st.spinner("正在自动寻找可用的 AI 通道..."):
        model_name, error = find_working_model()
        if model_name:
            st.session_state['working_model'] = model_name
            st.success(f"✅ 已连接至: {model_name}")
        else:
            st.error(f"❌ 系统崩溃: {error}")

question = st.text_input("", placeholder="在此键入你的困惑...")

if st.button("断"):
    if not question:
        st.warning("无问则无解。")
    elif 'working_model' in st.session_state:
        # 进度条仪式感
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i+1)
        bar.empty()
        
        bazi = get_bazi()
        # 使用刚才自动检测到的模型
        answer = ask_oracle(question, st.session_state['working_model'])
        st.markdown(f'<div class="oracle-text">{answer}</div>', unsafe_allow_html=True)
        
        with st.expander("查看数据流"):
            st.write(f"八字: {bazi}")
            st.write(f"Model: {st.session_state['working_model']}")
    else:
        st.error("AI 通道未建立，无法预测。")
