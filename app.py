import streamlit as st
import streamlit.components.v1 as components

# 页面基础设置
st.set_page_config(page_title="皮皮鹦鹉", page_icon="🦜", layout="centered")

# 隐藏不需要的菜单，让界面更干净
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
/* 手机端优化 */
.stApp { background-color: #fceea7; }
</style>
""", unsafe_allow_html=True)

# --- 核心代码 (HTML/JS/CSS) ---
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Parrot Final</title>
    <style>
        /* 1. 基础布局 */
        body {
            font-family: "Comic Sans MS", "YouYuan", "幼圆", sans-serif;
            background-color: #fceea7; /* 鹅黄色背景 */
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
            height: 100vh; margin: 0; padding-top: 20px;
            overflow: hidden; touch-action: manipulation;
        }

        /* 2. 主容器 */
        .container {
            background-color: #fff; padding: 20px; border-radius: 20px;
            width: 85%; max-width: 350px; text-align: center; 
            border: 5px solid #ff6b6b; box-shadow: 0 8px 15px rgba(0,0,0,0.1);
            position: relative; z-index: 10;
        }

        h1 { color: #ff6b6b; margin: 0 0 10px 0; font-size: 22px; }

        /* 3. 鹦鹉头像 */
        .parrot-box {
            width: 140px; height: 140px; margin: 0 auto 15px; border-radius: 50%;
            background: #e0f7fa; border: 4px solid #4ecdc4; overflow: hidden;
            display: flex; align-items: center; justify-content: center;
            position: relative; z-index: 5;
        }
        .parrot-img { width: 100%; height: 100%; object-fit: cover; }
        .parrot-emoji { font-size: 70px; animation: float 3s infinite; }

        /* 4. 对话气泡 */
        .bubble {
            background: #4ecdc4; color: white; padding: 12px; border-radius: 15px;
            min-height: 50px; margin-bottom: 20px; position: relative;
            font-size: 16px; line-height: 1.4; display: flex; align-items: center; justify-content: center;
        }
        .bubble::after {
            content: ''; position: absolute; top: -10px; left: 50%; margin-left: -8px;
            border-width: 0 8px 8px; border-style: solid; border-color: #4ecdc4 transparent;
        }

        /* 5. 麦克风按钮 (绝对置顶，防止点不到) */
        .mic-btn {
            width: 70px; height: 70px; border-radius: 50%; border: none;
            background: #ff6b6b; color: white; font-size: 30px;
            box-shadow: 0 5px 0 #c0392b; cursor: pointer; 
            display: block; margin: 0 auto 10px auto;
            position: relative; z-index: 100; /* 确保在最上层 */
            transition: transform 0.1s;
        }
        .mic-btn:active { transform: translateY(5px); box-shadow: none; }
        .mic-btn.active { background: #2ecc71; animation: pulse 1.5s infinite; }

        /* 6. 备用输入框 (默认隐藏) */
        .fallback-area {
            display: none; margin-top: 10px; width: 100%;
        }
        .input-box {
            width: 70%; padding: 10px; border: 2px solid #ddd; border-radius: 10px; font-size: 14px;
        }
        .send-btn {
            width: 20%; padding: 10px; background: #ff6b6b; color: white; border: none; border-radius: 10px;
        }

        /* 状态文字 */
        .status { font-size: 12px; color: #888; min-height: 20px; }
        .error { color: red; font-size: 12px; display: none; margin-top: 5px; }

        /* 动画 */
        @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-5px);} }
        @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.1);} 100% {transform: scale(1);} }
        .shaking { animation: shake 0.4s infinite; }
        @keyframes shake { 0% {transform: rotate(0deg);} 25% {transform: rotate(5deg);} 75% {transform: rotate(-5deg);} }
    </style>
</head>
<body>

<div class="container">
    <h1>🦜 超级皮皮</h1>
    
    <div class="parrot-box" id="parrot">
        <img src="parrot.jpg" class="parrot-img" onerror="this.style.display='none'; document.getElementById('emoji').style.display='block';">
        <div id="emoji" class="parrot-emoji" style="display:none">🦜</div>
    </div>

    <div class="bubble" id="msgBox">
        你好！我是皮皮！<br>点按钮和我说话！
    </div>

    <button class="mic-btn" id="micBtn" onclick="handleClick()">🎤</button>
    
    <div class="status" id="statusText">点击麦克风开始</div>
    <div class="error" id="errorText"></div>

    <div class="fallback-area" id="fallbackArea">
        <input type="text" id="txtInput" class="input-box" placeholder="在这打字也可以哦..." onkeypress="if(event.key==='Enter') sendText()">
        <button class="send-btn" onclick="sendText()">说</button>
    </div>
</div>

<script>
    // --- 1. 核心逻辑 (Brain) ---
    class ParrotBrain {
        constructor() {
            this.name = "皮皮";
            this.userName = "";
            this.stories = [
                "小猪吃太饱，变成了飞猪！🐷",
                "月亮婆婆值班，星星都笑醒了。⭐",
                "蜗牛爬山爬了三天，终于爬到了门口。🐌"
            ];
        }
        reply(text) {
            const t = text.replace(/[.,?!]/g, "").trim();
            if (!t) return "呱？没听见！";
            
            if (t.includes("我叫")) { this.userName = t.split("我叫")[1]; return `记住了！你叫${this.userName}！`; }
            if (t.includes("我是谁")) return this.userName ? `你是${this.userName}！` : "你还没告诉我名字！";
            if (t.includes("故事")) return "讲个故事：\n" + this.stories[Math.floor(Math.random()*this.stories.length)];
            
            // 数学
            const m = t.match(/(\d+)\s*([加减\+\-])\s*(\d+)/);
            if (m) {
                const n1 = parseInt(m[1]), op = m[2], n2 = parseInt(m[3]);
                return `我知道！等于 ${op==='+'||op==='加' ? n1+n2 : n1-n2}！`;
            }
            
            if (t.includes("名字")) return "我叫皮皮！";
            if (t.includes("几岁")) return "我三岁啦！";
            if (t.includes("吃")) return "我要吃饼干！🍪";
            if (t.includes("你好")) return "你好呀！扑棱扑棱！";
            
            return "你说：" + t + "！呱！";
        }
    }

    // --- 2. 控制系统 ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    let recognition;
    const brain = new ParrotBrain();

    const btn = document.getElementById('micBtn');
    const msgBox = document.getElementById('msgBox');
    const statusText = document.getElementById('statusText');
    const errorText = document.getElementById('errorText');
    const parrot = document.getElementById('parrot');
    const fallbackArea = document.getElementById('fallbackArea');
    const txtInput = document.getElementById('txtInput');

    // 检查浏览器支持情况
    if (!SpeechRecognition) {
        showFallback("你的浏览器不支持语音，请用打字哦！");
    } else {
        recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false;

        recognition.onstart = () => {
            btn.classList.add('active');
            statusText.innerText = "👂 正在听...";
            errorText.style.display = 'none';
        };
        recognition.onend = () => {
            btn.classList.remove('active');
            if(statusText.innerText === "👂 正在听...") statusText.innerText = "点击开始";
        };
        recognition.onresult = (e) => {
            const text = e.results[0][0].transcript;
            process(text);
        };
        recognition.onerror = (e) => {
            console.error(e.error);
            btn.classList.remove('active');
            // 核心修复：如果报错是 not-allowed，说明权限被锁，直接切到打字模式
            if (e.error === 'not-allowed' || e.error === 'service-not-allowed') {
                showFallback("❌ 麦克风被浏览器锁住了！请在下面打字：");
            } else if (e.error === 'no-speech') {
                statusText.innerText = "没听到声音，再试一次...";
            } else {
                statusText.innerText = "出错了: " + e.error;
            }
        };
    }

    // --- 3. 交互函数 ---
    
    function handleClick() {
        // 先检查是否有语音合成（TTS）能力，用来激活声音
        if (synth) synth.cancel();

        if (!recognition) {
            showFallback("语音功能不可用，请打字。");
            return;
        }

        if (btn.classList.contains('active')) {
            recognition.stop();
        } else {
            try {
                recognition.start();
                statusText.innerText = "启动中...";
            } catch (e) {
                // 如果启动直接报错，大概率是环境问题
                showFallback("无法启动麦克风，请在下面打字：");
            }
        }
    }

    function process(text) {
        statusText.innerText = "听到: " + text;
        const replyText = brain.reply(text);
        
        // 显示
        msgBox.innerHTML = replyText.replace(/\\n/g, '<br>');
        
        // 播放语音
        speak(replyText);
    }

    function speak(text) {
        parrot.classList.add('shaking');
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN'; u.pitch = 1.6; u.rate = 1.3;
        u.onend = () => { parrot.classList.remove('shaking'); };
        synth.speak(u);
    }

    // --- 4. 备用模式 (打字) ---
    function showFallback(msg) {
        errorText.innerText = msg;
        errorText.style.display = 'block';
        fallbackArea.style.display = 'block'; // 显示输入框
        btn.style.display = 'none'; // 隐藏没用的麦克风按钮
    }

    function sendText() {
        const val = txtInput.value;
        if (val) {
            process(val);
            txtInput.value = '';
        }
    }

</script>
</body>
</html>
"""

components.html(html_code, height=750)
