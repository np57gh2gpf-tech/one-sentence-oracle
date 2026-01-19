import streamlit as st
import lunar_python
import google.generativeai as genai
from datetime import datetime
import time
import random

# ================= 1. 基础配置 (逻辑不变) =================
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ================= 2. 页面样式 (视觉觉醒·奇门秘境) =================
st.set_page_config(page_title="天机·深渊推演", page_icon="🌑", layout="centered")

# 注入复杂的 CSS 魔法
st.markdown("""
<style>
    /* ================== 核心背景：呼吸感奇门图腾 ================== */
    @keyframes breathe {
        0% { opacity: 0.6; transform: scale(1.0); filter: brightness(0.8); }
        50% { opacity: 1.0; transform: scale(1.02); filter: brightness(1.2) sepia(0.2); }
        100% { opacity: 0.6; transform: scale(1.0); filter: brightness(0.8); }
    }
    
    @keyframes rotate-slow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .stApp {
        background-color: #020202; /* 极深渊黑 */
        /* 使用 SVG 绘制复杂的背景纹理 */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'%3E%3Cg fill='none' stroke='%232a2a2a' stroke-width='1.5' opacity='0.4'%3E%3Ccircle cx='200' cy='200' r='180'/%3E%3Ccircle cx='200' cy='200' r='140'/%3E%3Ccircle cx='200' cy='200' r='100'/%3E%3Cpath d='M200 20v360M20 200h360M73 73l254 254M327 73L73 327'/%3E%3C/g%3E%3Cg fill='%23333' font-family='Songti SC, serif' font-size='14' text-anchor='middle' opacity='0.5'%3E%3Ctext x='200' y='40' transform='rotate(0 200 200)'%3E甲%3C/text%3E%3Ctext x='200' y='40' transform='rotate(30 200 200)'%3E乙%3C/text%3E%3Ctext x='200' y='40' transform='rotate(60 200 200)'%3E丙%3C/text%3E%3Ctext x='200' y='40' transform='rotate(90 200 200)'%3E丁%3C/text%3E%3Ctext x='200' y='40' transform='rotate(120 200 200)'%3E戊%3C/text%3E%3Ctext x='200' y='40' transform='rotate(150 200 200)'%3E己%3C/text%3E%3Ctext x='200' y='40' transform='rotate(180 200 200)'%3E庚%3C/text%3E%3Ctext x='200' y='40' transform='rotate(210 200 200)'%3E辛%3C/text%3E%3Ctext x='200' y='40' transform='rotate(240 200 200)'%3E壬%3C/text%3E%3Ctext x='200' y='40' transform='rotate(270 200 200)'%3E癸%3C/text%3E%3Ctext x='280' y='200' font-size='20'%3E乾%3C/text%3E%3Ctext x='120' y='200' font-size='20'%3E坤%3C/text%3E%3C/g%3E%3C/svg%3E");
        background-attachment: fixed;
        background-position: center;
        background-repeat: repeat;
        /* 应用呼吸动画 */
        animation: breathe 12s infinite ease-in-out;
        /* 叠加一层暗色滤镜，增加神秘感 */
        background-blend-mode: soft-light;
    }

    /* ================== 控件样式优化 ================== */
    /* 输入框：隐秘的黑金 */
    .stTextInput > div > div > input {
        color: #e6c9a8; 
        background-color: rgba(20, 20, 20, 0.8); /* 半透明 */
        border: 1px solid #444; 
        font-family: 'Courier New';
        box-shadow: inset 0 0 10px #000;
    }
    
    /* 按钮：低调奢华 */
    .stButton > button {
        width: 100%; 
        background: linear-gradient(145deg, #1a1a1a, #2a2a2a);
        color: #888; 
        border: 1px solid #333;
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        text-shadow: 0 1px 2px #000;
    }
    .stButton > button:hover {
        border-color: #8a6d3b; color: #d4af37; 
        background: linear-gradient(145deg, #2a2a2a, #3a3a3a);
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
    }
    
    /* ================== 结果显示区样式 ================== */
    .oracle-main {
        font-family: 'Songti SC', 'SimSun', serif; 
        font-size: 32px; 
        color: #e6c9a8; 
        text-align: center; 
        padding: 40px 20px; 
        margin-top: 30px;
        line-height: 1.4;
        font-weight: 600;
        border-bottom: 1px solid #333;
        text-shadow: 0 0 20px rgba(230, 201, 168, 0.3);
        background: rgba(10, 10, 10, 0.6); /* 半透明背景 */
        backdrop-filter: blur(5px); /* 毛玻璃效果 */
        border-radius: 8px;
        animation: fade-in-up 1s ease-out;
    }
    
    .oracle-note {
        font-family: 'KaiTi', '楷体', serif;
        font-size: 14px;
        color: #666; 
        text-align: justify; 
        padding: 20px 20px;
        line-height: 1.8;
        letter-spacing: 1px;
        background: rgba(20, 20, 20, 0.4);
        border-radius: 0 0 8px 8px;
        animation: fade-in-up 1.2s ease-out;
    }
    
    @keyframes fade-in-up {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* ================== 🌟 核心：粒子汇聚加载动画 CSS ================== */
    .particle-container {
        position: relative;
        height: 150px; /* 动画区域高度 */
        width: 100%;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        background: radial-gradient(circle, rgba(40,40,40,0.2) 0%, rgba(0,0,0,0) 70%);
    }

    .particle-text {
        font-family: 'Songti SC', serif;
        position: absolute;
        color: #d4af37; /* 金色粒子 */
        opacity: 0;
        font-weight: bold;
        text-shadow: 0 0 5px #d4af37;
        /* 核心动画：从四周飞入并旋转 */
        animation: gatherParticles 2.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }

    /* 核心能量球，粒子汇聚点 */
    .core-energy {
        width: 20px;
        height: 20px;
        background: #d4af37;
        border-radius: 50%;
        box-shadow: 0 0 30px 10px rgba(212, 175, 55, 0.5);
        animation: pulse-core 1s infinite alternate;
        opacity: 0;
        animation-delay: 1.5s; /* 等粒子快到了再出现 */
    }
    
    @keyframes pulse-core {
        from { transform: scale(0.8); opacity: 0.5; }
        to { transform: scale(1.5); opacity: 1; }
    }

    @keyframes gatherParticles {
        0% {
            /* 初始状态：随机散落在屏幕外，透明，旋转 */
            transform: translate(var(--tx), var(--ty)) rotate(var(--r)) scale(0.5);
            opacity: 0;
        }
        20% { opacity: 1; } /* 快速显现 */
        80% {
            /* 中间状态：快到中心了，开始变小，加速旋转 */
            transform: translate(calc(var(--tx) * 0.1), calc(var(--ty) * 0.1)) rotate(calc(var(--r) * 3)) scale(0.8);
            opacity: 0.8;
        }
        100% {
            /* 最终状态：汇聚到中心点，消失，仿佛融化进答案 */
            transform: translate(0, 0) rotate(720deg) scale(0.1);
            opacity: 0;
        }
    }
    
    /* 辅助文本样式 */
    .loading-step { 
        font-family: 'Courier New'; font-size: 12px; color: #d4af37; text-align: center; margin-top:5px;
        text-shadow: 0 0 5px rgba(212, 175, 55, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. 智能模型连接 (逻辑不变) =================
def find_working_model():
    if not API_KEY: return None, "请配置 API Key"
    genai.configure(api_key=API_KEY)
    # 优先使用 Pro，逻辑最强
    priority_list = ["gemini-1.5-pro", "gemini-2.0-flash-exp", "gemini-1.5-flash"]
    for model_name in priority_list:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("test")
            return model_name, None
        except: continue
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                try:
                    model = genai.GenerativeModel(m.name)
                    model.generate_content("test")
                    return m.name, None
                except: continue
    except Exception as e: return None, str(e)
    return None, "未找到可用模型"

# ================= 4. 核心业务 (逻辑不变) =================
def get_bazi():
    now = datetime.now()
    solar = lunar_python.Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, now.second)
    lunar = solar.getLunar()
    bazi = lunar.getBaZi()
    return f"{bazi[0]}年 {bazi[1]}月 {bazi[2]}日 {bazi[3]}时"

def ask_oracle(question, bazi, model_name):
    try:
        model = genai.GenerativeModel(model_name)
        # 👑 宗师级 Prompt (保持不变)
        prompt = f"""
        【角色设定】：你是一位隐居的奇门遁甲宗师，精通《御定奇门宝鉴》与《三命通会》。
        【当前局势】：求测者问："{question}"；当前时空八字：{bazi}
        【深度思考任务 (Deep Reasoning)】
        1. 请立刻在后台排布此时的“奇门盘”：定局数、排地盘九宫、飞天盘九星、排人盘八门、布神盘八神。
        2. 寻找“值符”与“值使”，看它们落在何宫。
        3. 分析“十干克应”（如：乙+辛是青龙逃走，丙+戊是飞鸟跌穴）。
        4. **结合五行生克，得出唯一的、绝对的结论。**
        【输出指令 - 严格遵守】：请输出两部分，用 "|||" 分隔。
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
        【反模板机制】：哪怕问题一样，因为八字时辰在变，你的推演必须完全不同。每次生成的词汇、句式必须多变，不要重复。
        开始推演：
        """
        # 🔥 Temperature = 1.0 (保持不变)
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
        
        # === 🌟 核心修改：粒子汇聚动画替代进度条 ===
        # 创建一个空容器来放动画
        animation_placeholder = st.empty()
        
        # 定义要飞舞的玄学文字粒子
        particles = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", 
                     "休", "生", "伤", "杜", "景", "死", "惊", "开",
                     "乾", "坤", "震", "巽", "坎", "离", "艮", "兑", "天机", "遁"]
        
        # 生成 HTML 字符串
        particle_html = '<div class="particle-container">'
        for p in particles:
            # 随机生成起始位置和旋转角度，用于 CSS 动画
            tx = random.randint(-300, 300)
            ty = random.randint(-300, 300)
            r = random.randint(0, 360)
            size = random.randint(14, 24)
            # 注入带随机变量的 span
            particle_html += f'<span class="particle-text" style="--tx:{tx}px; --ty:{ty}px; --r:{r}deg; font-size:{size}px;">{p}</span>'
        
        particle_html += '<div class="core-energy"></div>' # 中心的能量球
        particle_html += '</div>'
        
        # 1. 显示粒子动画
        animation_placeholder.markdown(particle_html, unsafe_allow_html=True)
        
        # 2. 显示文字提示步进 (辅助)
        info_placeholder = st.empty()
        steps = ["正在定地盘九宫...", "飞布天盘九星...", "推演人盘八门...", "召唤神盘八神...", "分析十干克应...", "天机汇聚中..."]
        for step in steps:
            info_placeholder.markdown(f"<div class='loading-step'>{step}</div>", unsafe_allow_html=True)
            # 这里的延时要配合 CSS 动画的总时长 (大约 2.5s - 3s)
            time.sleep(random.uniform(0.4, 0.6)) 
            
        # === 获取结果 (在动画播放时后台请求) ===
        bazi = get_bazi()
        full_response = ask_oracle(question, bazi, st.session_state['working_model'])
        
        # 动画结束，清空动画容器
        animation_placeholder.empty()
        info_placeholder.empty()
        
        # 分割结果
        if "|||" in full_response:
            main_text, note_text = full_response.split("|||", 1)
        else:
            main_text = full_response
            note_text = "局象混沌，不可言说。"
            
        # 显示结果 (带淡入动画)
        st.markdown(f'<div class="oracle-main">{main_text}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="oracle-note"><b>【局象推演记录】</b><br>{note_text}</div>', unsafe_allow_html=True)
        
    else:
        st.error("通道未建立，请刷新。")
