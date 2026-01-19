import streamlit as st
import lunar_python
import google.generativeai as genai
from datetime import datetime
import time
import random

# ================= 配置区 =================
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ================= 页面样式 (保持神秘感) =================
st.set_page_config(page_title="天机·一句顶一万句", page_icon="☯️", layout="centered")
st.markdown("""
<style>
    .stApp {background-color: #0e1117; color: #e0e0e0;}
    .stTextInput > div > div > input {
        color: #d4af37; /* 金色字体 */
        background-color: #000000; 
        border: 1px solid #30363d; 
        font-family: 'Courier New';
    }
    .stButton > button {
        width: 100%; background-color: #21262d; color: #d4af37; border: 1px solid #d4af37;
    }
    .oracle-text {
        font-family: 'Songti SC', 'SimSun', serif; 
        font-size: 28px; 
        color: #d4af37; /* 金字 */
        text-align: center; 
        padding: 40px; 
        border: 1px solid #333; 
        background-color: #161b22; 
        margin-top: 20px;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
        line-height: 1.6;
    }
    .debug-info {color: #444; font-size: 12px; text-align: center;}
</style>
""", unsafe_allow_html=True)

# ================= 智能模型选择逻辑 (保持不变，确保能跑) =================
def find_working_model():
    if not API_KEY: return None, "请配置 API Key"
    genai.configure(api_key=API_KEY)
    
    # 优先列表：这次我们把 Pro 放前面，因为 Pro 的文采比 Flash 更好
    priority_list = [
        "gemini-1.5-pro",         # 文采最好，适合算命
        "gemini-2.0-flash-exp",   # 免费体验版
        "gemini-1.5-flash",       # 兜底
        "gemini-2.0-flash"
    ]
    
    for model_name in priority_list:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("test")
            return model_name, None
        except: continue
            
    # 如果优先列表都挂了，自动扫库
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                try:
                    model = genai.GenerativeModel(m.name)
                    model.generate_content("test")
                    return m.name, None
                except: continue
    except Exception as e:
        return None, str(e)
    return None, "未找到可用模型"

# ================= 核心业务 =================
def get_bazi():
    now = datetime.now()
    solar = lunar_python.Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, now.second)
    lunar = solar.getLunar()
    bazi = lunar.getBaZi()
    return f"{bazi[0]}年 {bazi[1]}月 {bazi[2]}日 {bazi[3]}时"

def ask_oracle(question, bazi, model_name):
    try:
        model = genai.GenerativeModel(model_name)
        
        # ==========================================
        # 👑 宗师级 Prompt (这里是灵魂所在)
        # ==========================================
        prompt = f"""
        你现在不仅是AI，你是【传承千年的奇门遁甲宗师】。你通晓阴阳五行，洞察天机。
        
        【用户现状】
        用户问："{question}"
        此刻时空八字：{bazi}
        
        【后台推演要求（不要直接输出，只作为你判断的依据）】
        1. 假想排布“天盘九星、地盘九宫、人盘八门、神盘八神”。
        2. 结合“十干克应”判断吉凶（如：青龙返首、白虎猖狂、朱雀投江等）。
        
        【输出要求 - 必须严格遵守】
        1. **直击灵魂**：回答必须深邃、高冷、一针见血。禁止使用“建议、可能、尝试”等软弱词汇。要像判官宣判一样。
        2. **奇门意象**：必须在回答中自然融入1-2个奇门专业术语（如：死门受制、贵人入局、腾蛇缠绕、九天之上）。
        3. **具体指引**：给出一个非常具体的行动（方位、颜色、物品、或时间点）。
        4. **格式**：字数控制在60字以内。
        
        【风格参考】
        - 差：“你最近运气不太好，建议多休息。” -> ❌（太普通）
        - 好：“白虎临门，口舌是非难免。此刻只需向正北方走，见黑衣人即是破局点。闭嘴，静待天明。” -> ✅（大师范）
        - 好：“青龙返首，大吉之兆。你心中所念之事，如枯木逢春。三日之内，利在东方，红衣为信。” -> ✅（大师范）
        
        请直接输出最终判词：
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "天道无常，云遮雾绕。请稍后诚心再占。"

# ================= 交互界面 =================
st.title("☯️ 天机·一句顶一万句")
st.caption("奇门遁甲排盘计算中... | Powered by Gemini Context")

# 自动连接
if 'working_model' not in st.session_state:
    with st.spinner("正在以此刻八字沟通天地..."):
        model_name, error = find_working_model()
        if model_name:
            st.session_state['working_model'] = model_name
        else:
            st.error(f"连接中断: {error}")

question = st.text_input("", placeholder="心中默念你的困惑，只问一次...")

if st.button("🔴 起 局 (断)"):
    if not question:
        st.warning("无问则无卦，心诚则灵。")
    elif 'working_model' in st.session_state:
        # 增加仪式感：模拟复杂的排盘计算过程
        progress_text = st.empty()
        bar = st.progress(0)
        
        steps = [
            "正在排布地盘九宫...", "飞布天盘九星...", "推演八门吉凶...", 
            "召唤八神入局...", "十干克应分析中...", "正在生成最终判词..."
        ]
        
        for i, step in enumerate(steps):
            progress_text.text(step)
            # 随机停顿，模拟计算复杂度
            time.sleep(random.uniform(0.3, 0.7)) 
            bar.progress(int((i + 1) / len(steps) * 100))
            
        bar.empty()
        progress_text.empty()
        
        # 真正请求
        bazi = get_bazi()
        answer = ask_oracle(question, bazi, st.session_state['working_model'])
        
        # 显示结果
        st.markdown(f'<div class="oracle-text">{answer}</div>', unsafe_allow_html=True)
        
        # 底部隐秘信息
        st.markdown(f'<div class="debug-info">时空坐标: {bazi} | 局象: 阴遁九局</div>', unsafe_allow_html=True)
    else:
        st.error("天路未通，请刷新重试。")
