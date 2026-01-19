import streamlit as st
import lunar_python
import google.generativeai as genai
from datetime import datetime
import time
import random

# ================= 1. 基础配置 =================
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ================= 2. 页面样式 (宗师级·暗黑金风格) =================
st.set_page_config(page_title="天机·深渊推演", page_icon="🌑", layout="centered")

st.markdown("""
<style>
    /* 全局深渊黑 */
    .stApp {background-color: #050505; color: #a0a0a0;}
    
    /* 输入框：隐秘的灰金 */
    .stTextInput > div > div > input {
        color: #d4af37; 
        background-color: #111; 
        border: 1px solid #333; 
        font-family: 'Courier New';
    }
    
    /* 按钮：低调 */
    .stButton > button {
        width: 100%; background-color: #1a1a1a; color: #666; border: 1px solid #333;
        transition: all 0.5s;
    }
    .stButton > button:hover {
        border-color: #8a6d3b; color: #d4af37; background-color: #222;
    }
    
    /* 核心判词 (大字)：直击灵魂 */
    .oracle-main {
        font-family: 'Songti SC', 'SimSun', serif; 
        font-size: 32px; 
        color: #e6c9a8; 
        text-align: center; 
        padding: 40px 10px; 
        margin-top: 30px;
        line-height: 1.4;
        font-weight: 600;
        border-bottom: 1px solid #333;
        /* 文字微光效果 */
        text-shadow: 0 0 10px rgba(230, 201, 168, 0.1);
    }
    
    /* 玄学注解 (小字)：像古籍批注 */
    .oracle-note {
        font-family: 'KaiTi', '楷体', serif;
        font-size: 14px;
        color: #555; 
        text-align: justify; 
        padding: 20px 10px;
        line-height: 1.8;
        letter-spacing: 1px;
    }
    
    .loading-step { font-family: 'Courier New'; font-size: 12px; color: #444; text-align: center; margin-top:5px;}
</style>
""", unsafe_allow_html=True)

# ================= 3. 智能模型连接 (自动寻路) =================
def find_working_model():
    if not API_KEY: return None, "请配置 API Key"
    genai.configure(api_key=API_KEY)
    
    # 优先使用 Pro，因为它的逻辑推理能力最强，能编出最像样的“象数理”
    priority_list = [
        "gemini-1.5-pro", 
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash"
    ]
    
    for model_name in priority_list:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("test")
            return model_name, None
        except: continue
            
    # 兜底
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

# ================= 4. 核心业务 =================
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
        # 👑 宗师级 Prompt：禁止模板，强制深度推演
        # ==========================================
        prompt = f"""
        【角色设定】：你是一位隐居的奇门遁甲宗师，精通《御定奇门宝鉴》与《三命通会》。
        
        【当前局势】
        求测者问："{question}"
        当前时空八字：{bazi}
        
        【深度思考任务 (Deep Reasoning)】
        1. 请立刻在后台排布此时的“奇门盘”：定局数、排地盘九宫、飞天盘九星、排人盘八门、布神盘八神。
        2. 寻找“值符”与“值使”，看它们落在何宫。
        3. 分析“十干克应”（如：乙+辛是青龙逃走，丙+戊是飞鸟跌穴）。
        4. **结合五行生克，得出唯一的、绝对的结论。**
        
        【输出指令 - 严格遵守】
        请输出两部分，用 "|||" 分隔。
        
        **第一部分：天机直断 (给用户的答案)**
        - 要求：**一针见血，不留情面**。直接回答是吉是凶，行还是不行。
        - 必须包含一句**“最需要注意”的警告**（好的坏的都要说）。
        - 语气：斩钉截铁。禁止使用“可能、建议、也许、根据卦象”等废话。
        - 字数：40字以内。
        
        **第二部分：象数理推演 (给用户看的底层逻辑)**
        - 要求：这是你排盘的过程记录。
        - **必须使用专业黑话**：提到具体的星（如天蓬、天辅）、门（如死门、杜门）、神（如玄武、九天）、格局（如龙回首、虎猖狂）。
        - 解释此时的“象”是什么。为什么得出上面的结论？
        - 让人感觉玄乎其玄，但又逻辑自洽。
        
        【反模板机制】
        - 哪怕问题一样，因为八字时辰在变，你的推演必须完全不同。
        - 每次生成的词汇、句式必须多变，不要重复。
        
        开始推演：
        """
        
        # 🔥 Temperature = 1.0 (创造力拉满，拒绝模板)
        config = genai.types.GenerationConfig(temperature=1.0)
        
        response = model.generate_content(prompt, generation_config=config)
        return response.text
    except Exception as e:
        return "天道闭塞，灵感未至。|||系统震荡: " + str(e)

# ================= 5. 交互界面 =================
st.title("天机·深渊推演")
st.caption("Grandmaster Oracle // Depth: Maximum")

# 自动连接
if 'working_model' not in st.session_state:
    with st.spinner("正在校准真太阳时..."):
        model_name, error = find_working_model()
        if model_name:
            st.session_state['working_model'] = model_name
        else:
            st.error(f"连接失败: {error}")

question = st.text_input("", placeholder="在此写下你的困惑，只问一次...")

if st.button("👁‍🗨 开 启 天 眼"):
    if not question:
        st.warning("心不诚则卦不灵。")
    elif 'working_model' in st.session_state:
        
        # === 沉浸式加载动画 (模拟大师思考过程) ===
        progress_text = st.empty()
        bar = st.progress(0)
        
        # 这些步骤文案，让用户觉得AI真的在算
        steps = [
            "正在定地盘九宫...", 
            "飞布天盘九星 (天蓬/天任/天冲)...", 
            "推演人盘八门 (休/生/伤/杜)...", 
            "召唤神盘八神 (值符/腾蛇/太阴)...", 
            "分析十干克应 (青龙/白虎/朱雀)...", 
            "捕捉时空外应..."
        ]
        
        for i, step in enumerate(steps):
            progress_text.markdown(f"<div class='loading-step'>{step}</div>", unsafe_allow_html=True)
            # 随机停顿，模拟计算复杂度
            time.sleep(random.uniform(0.6, 1.0)) 
            bar.progress(int((i + 1) / len(steps) * 100))
            
        bar.empty()
        progress_text.empty()
        
        # 获取结果
        bazi = get_bazi()
        full_response = ask_oracle(question, bazi, st.session_state['working_model'])
        
        # 分割结果
        if "|||" in full_response:
            main_text, note_text = full_response.split("|||", 1)
        else:
            main_text = full_response
            note_text = "局象混沌，不可言说。"
            
        # 1. 大字判词：直接、狠辣
        st.markdown(f'<div class="oracle-main">{main_text}</div>', unsafe_allow_html=True)
        
        # 2. 小字注解：专业、唬人、玄乎
        st.markdown(f'<div class="oracle-note"><b>【局象推演记录】</b><br>{note_text}</div>', unsafe_allow_html=True)
        
    else:
        st.error("通道未建立，请刷新。")
