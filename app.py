import streamlit as st
import lunar_python
import google.generativeai as genai
from datetime import datetime
import time
import random

# ================= 1. 基础配置 =================
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ================= 2. 页面样式 (保持神秘高级感) =================
st.set_page_config(page_title="天机·深层推演", page_icon="🌒", layout="centered")

st.markdown("""
<style>
    .stApp {background-color: #080808; color: #ccc;}
    
    /* 输入框：极简黑金 */
    .stTextInput > div > div > input {
        color: #d4af37; 
        background-color: #121212; 
        border: 1px solid #333; 
        font-family: 'Courier New';
    }
    
    .stButton > button {
        width: 100%; background-color: #1e1e1e; color: #888; border: 1px solid #333;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        border-color: #d4af37; color: #d4af37;
    }
    
    /* 结果容器：不再受限于边框，更像虚空浮现的文字 */
    .oracle-main {
        font-family: 'Songti SC', 'SimSun', serif; 
        font-size: 32px; 
        color: #e6c9a8; 
        text-align: center; 
        padding: 40px 10px; 
        margin-top: 20px;
        line-height: 1.4;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
    }
    
    .oracle-note {
        font-family: 'KaiTi', '楷体', serif;
        font-size: 15px;
        color: #555; 
        text-align: justify; 
        padding: 20px;
        border-top: 1px solid #222;
        margin-top: 10px;
        line-height: 1.8;
    }
    
    .loading-text { font-family: 'Courier New'; font-size: 12px; color: #444; text-align: center; margin-top:5px;}
</style>
""", unsafe_allow_html=True)

# ================= 3. 智能模型连接 =================
def find_working_model():
    if not API_KEY: return None, "请配置 API Key"
    genai.configure(api_key=API_KEY)
    
    # 优先使用 Pro，因为它的逻辑推理能力强，生成的语言更丰富多变
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
        # 👑 自由意志 Prompt (去模板化)
        # ==========================================
        prompt = f"""
        【指令】：你此刻是《奇门遁甲》与《易经》的集大成者。
        
        【输入信息】
        用户困惑："{question}"
        当前时空：{bazi}
        
        【深度思考任务】
        1. 请根据当前的“八字”，在你的庞大知识库中检索对应的“时空能量场”。不要瞎编，要基于五行生克原理。
        2. 将“用户的困惑”放入这个能量场中，看是“生”还是“克”。
        3. 就像一位真正的大师那样，根据这一瞬间的灵感，直接说出结论。
        
        【输出规则 - 绝对禁止套用模板】
        请输出两段话，中间用 "|||" 分隔。
        
        **第一段（给用户看的结果）：**
        - 不要用“根据卦象显示”这种废话开头。直接说事！
        - 语言风格要多变，可以是冷峻的、讽刺的、温暖的、或者神秘的，完全取决于当下的卦象是吉是凶。
        - **必须**包含一个只有在这个时间点才会出现的“独家建议”（比如具体的方位、颜色、或者一个奇怪的物品）。
        - 40字以内。
        
        **第二段（底层的玄学逻辑）：**
        - 用最专业的术语解释你为什么这么判。
        - 解释这一瞬间“天干地支”是如何撞击出这个结果的。
        - 这部分是为了展示你深不可测的逻辑链条。
        
        现在，释放你的深度学习能力，给出唯一的答案：
        """
        
        # 🔥 关键修改：temperature=1.0 
        # 这是一个控制“创造力”的参数。0是死板，1是极度奔放。
        # 设置为 1.0 保证每次生成的词汇、句式都完全不同，拒绝重复。
        config = genai.types.GenerationConfig(temperature=1.0)
        
        response = model.generate_content(prompt, generation_config=config)
        return response.text
    except Exception as e:
        return "灵感断流。|||系统干扰: " + str(e)

# ================= 5. 交互界面 =================
st.title("天机·深层推演")
st.caption("AI Deep Learning Oracle // Temperature: 1.0 (Max Creativity)")

# 自动连接
if 'working_model' not in st.session_state:
    with st.spinner("正在链接神经网络与时空场..."):
        model_name, error = find_working_model()
        if model_name:
            st.session_state['working_model'] = model_name
        else:
            st.error(f"连接失败: {error}")

question = st.text_input("", placeholder="在此输入，AI 将为你进行一次独一无二的推演...")

if st.button("⚜️ 开 启 推 演"):
    if not question:
        st.warning("空即是色，但此时需要输入问题。")
    elif 'working_model' in st.session_state:
        
        # 极简加载，不抢戏
        progress_text = st.empty()
        bar = st.progress(0)
        
        # 随机的加载语，也不重复
        loading_msgs = [
            "正在检索五行生克...", "神经网络拟合中...", "捕捉时空奇异点...", 
            "解析十干深层克应...", "生成唯一解..."
        ]
        
        for i in range(100):
            if i % 20 == 0:
                progress_text.text(random.choice(loading_msgs))
            time.sleep(0.01) 
            bar.progress(i + 1)
            
        bar.empty()
        progress_text.empty()
        
        # 获取结果
        bazi = get_bazi()
        full_response = ask_oracle(question, bazi, st.session_state['working_model'])
        
        if "|||" in full_response:
            main_text, note_text = full_response.split("|||", 1)
        else:
            main_text = full_response
            note_text = "玄机暗藏，不可言说。"
            
        # 1. 大字结果：不再有框，像浮在屏幕上
        st.markdown(f'<div class="oracle-main">{main_text}</div>', unsafe_allow_html=True)
        
        # 2. 小字逻辑：黑底灰字，极其专业
        st.markdown(f'<div class="oracle-note"><b>✦ 深度推演逻辑：</b><br>{note_text}</div>', unsafe_allow_html=True)
        
    else:
        st.error("通道未建立。")
