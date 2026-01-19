import streamlit as st
import lunar_python
import google.generativeai as genai
from datetime import datetime
import time
import random

# ================= 1. 基础配置 (技术基石，不动) =================
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ================= 2. 页面样式 (宗师级审美) =================
st.set_page_config(page_title="天机·一言断", page_icon="☯️", layout="centered")

st.markdown("""
<style>
    /* 全局黑底 */
    .stApp {background-color: #0e1117; color: #c9d1d9;}
    
    /* 输入框：黑底金字，更显贵气 */
    .stTextInput > div > div > input {
        color: #e6c9a8; 
        background-color: #1a1d24; 
        border: 1px solid #3d342b; 
        font-family: 'Courier New';
    }
    
    /* 按钮：深邃灰 */
    .stButton > button {
        width: 100%; 
        background-color: #2b2d31; 
        color: #e6c9a8; 
        border: 1px solid #3d342b;
    }
    
    /* 核心判词 (大字)：如圣旨般醒目 */
    .oracle-main {
        font-family: 'Songti SC', 'SimSun', serif; 
        font-size: 30px; 
        color: #e6c9a8; /* 鎏金色 */
        text-align: center; 
        padding: 30px 20px; 
        border-top: 2px solid #3d342b;
        border-bottom: 1px dashed #3d342b;
        background-color: #16181c; 
        margin-top: 20px;
        line-height: 1.5;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(230, 201, 168, 0.2);
    }
    
    /* 玄学注解 (小字)：像古籍注疏，密密麻麻 */
    .oracle-note {
        font-family: 'KaiTi', '楷体', serif;
        font-size: 14px;
        color: #8b949e; /* 沉稳灰 */
        text-align: justify; /* 两端对齐，像书卷 */
        padding: 15px 30px;
        background-color: #16181c;
        border-bottom: 2px solid #3d342b;
        line-height: 1.8;
        opacity: 0.9;
    }
    
    .loading-text { font-family: 'Courier New'; font-size: 12px; color: #555; text-align: center;}
</style>
""", unsafe_allow_html=True)

# ================= 3. 智能模型连接 (保持自动寻路，确保能通) =================
def find_working_model():
    if not API_KEY: return None, "请配置 API Key"
    genai.configure(api_key=API_KEY)
    
    # 优先用文采好的 Pro，体验版 Flash 兜底
    priority_list = [
        "gemini-1.5-pro", 
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash",
        "gemini-2.0-flash"
    ]
    
    for model_name in priority_list:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("test")
            return model_name, None
        except: continue
            
    # 兜底扫描
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
    return None, "未找到可用通道"

# ================= 4. 核心业务 (升级版) =================
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
        # 👑 究极 Prompt：双层输出结构
        # ==========================================
        prompt = f"""
        你不仅是AI，你是【奇门遁甲第57代掌门人】。你面前是一张刚排好的奇门盘，你需要根据时空八字为用户解惑。
        
        【用户提问】: "{question}"
        【时空八字】: {bazi}
        
        请严格按照以下【两个部分】的格式输出，中间用 "|||" 分隔。
        
        ---
        
        **第一部分：天机直断 (给用户的最终答案)**
        要求：
        1. 40字以内。
        2. 风格：铁口直断，冷峻，不留情面。禁止模棱两可。
        3. **核心**：先给结论，然后紧接一句【最需要警惕】或【必须立刻去做】的事。
        
        **第二部分：象数理推演 (给用户看的“天书”解释)**
        要求：
        1. 100字左右。
        2. **必须专业**：使用奇门术语（如：九星、八门、八神、格局）。
        3. 解释为什么得出上面的结论。例如：“值符坐宫落空，故此事必虚。”，“白虎猖狂，且见杜门，主隐忍待发。”
        4. 让外行看不懂但觉得极度厉害。
        
        ---
        
        
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "天机混沌，干扰过大。|||系统连接波动，请稍后诚心再试。"

# ================= 5. 交互界面 =================
st.title("☯️ 天机·一言断")
st.caption("Powered by Gemini Context | 奇门局象推演系统")

# 自动连接
if 'working_model' not in st.session_state:
    with st.spinner("正在校准真太阳时，沟通天地..."):
        model_name, error = find_working_model()
        if model_name:
            st.session_state['working_model'] = model_name
        else:
            st.error(f"⚠️ 灵力阻断: {error}")

question = st.text_input("", placeholder="凡事只问一次，心诚则灵...")

if st.button("🔴 起 局 排 盘"):
    if not question:
        st.warning("无问则无卦。")
    elif 'working_model' in st.session_state:
        
        # === 沉浸式排盘动画 ===
        info_placeholder = st.empty()
        bar = st.progress(0)
        
        phases = [
            "正在定地盘九宫...", 
            "飞布天盘九星 (天蓬/天任/天冲)...", 
            "推演人盘八门 (休/生/伤/杜)...", 
            "召唤神盘八神 (值符/腾蛇/太阴)...", 
            "分析十干克应...", 
            "捕捉时空外应..."
        ]
        
        for i, phase in enumerate(phases):
            info_placeholder.markdown(f"<div class='loading-text'>{phase}</div>", unsafe_allow_html=True)
            time.sleep(random.uniform(0.5, 0.8)) # 随机延迟，模拟计算
            bar.progress(int((i + 1) / len(phases) * 100))
            
        bar.empty()
        info_placeholder.empty()
        
        # === 获取结果 ===
        bazi = get_bazi()
        full_response = ask_oracle(question, bazi, st.session_state['working_model'])
        
        # === 核心：分割结果并渲染 ===
        if "|||" in full_response:
            main_text, note_text = full_response.split("|||", 1)
        else:
            main_text = full_response
            note_text = "局象模糊，未能生成详细批注。"
            
        # 1. 显示大字判词
        st.markdown(f'<div class="oracle-main">{main_text}</div>', unsafe_allow_html=True)
        
        # 2. 显示小字注解 (玄学解释)
        st.markdown(f'<div class="oracle-note"><b>【局象推演】</b><br>{note_text}</div>', unsafe_allow_html=True)
        
        # 3. 底部数据流
        st.markdown(f"<div style='text-align:center; color:#333; font-size:10px; margin-top:10px;'>Time: {bazi} | Model: {st.session_state['working_model']}</div>", unsafe_allow_html=True)
        
    else:
        st.error("通道未建立，请刷新重试。")
