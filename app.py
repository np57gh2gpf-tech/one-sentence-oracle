import streamlit as st
import streamlit.components.v1 as components

# 页面基础设置
st.set_page_config(page_title="皮皮 (语音修复版)", page_icon="🦜", layout="centered")

# 隐藏不必要的菜单
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 核心代码 ---
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Smart Parrot Fixed</title>
    <style>
        /* 界面样式 */
        body {
            font-family: "Comic Sans MS", "Microsoft YaHei", "幼圆", sans-serif;
            background-color: #fceea7;
            background-image: radial-gradient(#ffd700 10%, transparent 10%);
            background-size: 30px 30px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; margin: 0; overflow: hidden;
        }

        .container {
            background-color: #fff; padding: 20px; border-radius: 25px;
            width: 90%; max-width: 400px; text-align: center; 
            border: 6px solid #ff6b6b; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }

        h1 { color: #ff6b6b; margin: 0 0 15px 0; font-size: 24px; }

        .parrot-wrapper {
            width: 150px; height: 150px; margin: 0 auto 20px; position: relative;
        }
        .parrot-display {
            width: 100%; height: 100%; border-radius: 50%; overflow: hidden;
            border: 5px solid #4ecdc4; background-color: #e0f7fa; 
            display: flex; align-items: center; justify-content: center;
        }
        .parrot-img { width: 100%; height: 100%; object-fit: cover; }
        .parrot-emoji { font-size: 80px; animation: float 3s ease-in-out infinite; }

        /* 对话框 */
        .chat-bubble {
            background-color: #4ecdc4; color: white; padding: 15px; border-radius: 18px;
            min-height: 50px; margin-bottom: 20px; font-size: 1.1em; line-height: 1.4;
            position: relative; display: flex; align-items: center; justify-content: center; flex-direction: column;
        }
        .chat-bubble::after {
            content: ''; position: absolute; top: -10px; left: 50%; margin-left: -10px;
            border-width: 0 10px 10px; border-style: solid; border-color: #4ecdc4 transparent;
        }

        /* 按钮 */
        .control-btn {
            width: 70px; height: 70px; border-radius: 50%; border: none;
            background-color: #ff6b6b; color: white; font-size: 28px;
            box-shadow: 0 5px 0 #c0392b; cursor: pointer; transition: all 0.2s;
            display: block; margin: 0 auto;
        }
        .control-btn:active { transform: translateY(5px); box-shadow: 0 0 0; }
        .control-btn.listening { background-color: #2ecc71; animation: pulse 1.5s infinite; }

        /* 状态与错误信息 */
        .status-text { font-size: 14px; color: #888; margin-top: 10px; min-height: 20px; }
        .error-msg { color: red; font-size: 12px; margin-top: 5px; display: none; }

        /* 备用输入框 (默认隐藏) */
        .fallback-input {
            display: none; width: 80%; padding: 10px; border: 2px solid #ddd;
            border-radius: 10px; margin-top: 10px; font-size: 16px;
        }

        /* 动画 */
        @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-8px);} }
        @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.1);} 100% {transform: scale(1);} }
        .shaking { animation: shake 0.4s infinite; }
        @keyframes shake { 0% {transform: rotate(0deg);} 25% {transform: rotate(5deg);} 75% {transform: rotate(-5deg);} }

    </style>
</head>
<body>

<div class="container">
    <h1>🦜 皮皮</h1>
    
    <div class="parrot-wrapper">
        <div class="parrot-display" id="parrotContainer">
            <img src="parrot.jpg" class="parrot-img" onerror="this.style.display='none'; document.getElementById('emoji').style.display='block';">
            <div id="emoji" class="parrot-emoji" style="display:none">🦜</div>
        </div>
    </div>

    <div class="chat-bubble" id="responseBox">
        你好！我是皮皮！<br>点按钮跟我说话！
    </div>

    <button class="control-btn" id="micBtn" onclick="toggleListening()">🎤</button>
    
    <div class="status-text" id="statusLog">点击开始</div>
    <div class="error-msg" id="errorLog"></div>

    <input type="text" id="typeInput" class="fallback-input" placeholder="麦克风没开? 在这打字吧!" onkeypress="handleType(event)">
</div>

<script>
    // --- 1. 鹦鹉大脑 (Logic) ---
    class ParrotBrain {
        constructor() {
            this.name = "皮皮";
            this.userName = "";
            this.stories = [
                "小猪吃太饱飘到了天上变成了飞猪！🐷",
                "月亮婆婆出来值班，星星都笑醒了。⭐",
                "蜗牛爬山爬了三天，终于爬到了花盆上！🐌"
            ];
        }
        think(text) {
            const cleanText = text.replace(/[.,?!。，？！]/g, "").trim();
            if (!cleanText) return "呱？没听清！";
            
            // 逻辑处理
            if (cleanText.includes("我叫")) {
                this.userName = cleanText.split("我叫")[1];
                return `记住了！你叫${this.userName}！`;
            }
            if (cleanText.includes("我是谁")) return this.userName ? `你是${this.userName}！` : "你还没告诉我名字呢！";
            if (cleanText.includes("故事")) return "讲个故事：\n" + this.stories[Math.floor(Math.random() * this.stories.length)];
            
            // 数学
            const mathMatch = cleanText.match(/(\d+)\s*([加减\+\-])\s*(\d+)/);
            if (mathMatch) {
                const n1 = parseInt(mathMatch[1]);
                const op = mathMatch[2];
                const n2 = parseInt(mathMatch[3]);
                let res = (op === '加' || op === '+') ? n1 + n2 : n1 - n2;
                return `我知道！等于 ${res}！`;
            }

            // 百科
            if (cleanText.includes("名字")) return "我叫皮皮！";
            if (cleanText.includes("天空")) return "天空是蓝色的！";
            if (cleanText.includes("苹果")) return "苹果红红的！";
            if (cleanText.includes("你好")) return "你好呀！要吃饼干吗？";

            return "你说：" + cleanText + "！呱！";
        }
    }

    // --- 2. 核心控制 ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    let recognition;
    const brain = new ParrotBrain();
    
    const micBtn = document.getElementById('micBtn');
    const statusLog = document.getElementById('statusLog');
    const errorLog = document.getElementById('errorLog');
    const parrotDiv = document.getElementById('parrotContainer');
    const typeInput = document.getElementById('typeInput');

    // 初始化
    if (!SpeechRecognition) {
        showError("你的浏览器不支持语音(Web Speech API)。请使用 Chrome。");
        enableFallbackMode();
    } else {
        recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false; 

        recognition.onstart = () => {
            micBtn.classList.add('listening');
            statusLog.innerText = "👂 正在听...";
            errorLog.style.display = 'none';
        };

        recognition.onend = () => {
            micBtn.classList.remove('listening');
            if (statusLog.innerText === "👂 正在听...") {
                statusLog.innerText = "点击开始";
            }
        };

        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            processInput(text);
        };

        recognition.onerror = (e) => {
            console.error(e.error);
            micBtn.classList.remove('listening');
            
            if (e.error === 'not-allowed') {
                showError("❌ 麦克风权限被拒绝！请点击浏览器地址栏的小锁开启权限。");
                enableFallbackMode();
            } else if (e.error === 'no-speech') {
                statusLog.innerText = "没听到声音，再试一次...";
            } else {
                showError("❌ 发生错误: " + e.error);
                enableFallbackMode(); // 出错时也显示打字框
            }
        };
    }

    // --- 3. 交互逻辑 ---
    
    function toggleListening() {
        if (!recognition) return;
        
        // 如果正在说话，先打断
        synth.cancel();

        if (micBtn.classList.contains('listening')) {
            recognition.stop();
        } else {
            try {
                recognition.start();
                statusLog.innerText = "正在启动麦克风...";
            } catch (err) {
                // 如果 start() 报错，通常是因为没权限或者还没准备好
                showError("无法启动麦克风: " + err.message);
                enableFallbackMode();
            }
        }
    }

    function processInput(text) {
        statusLog.innerText = "听到: " + text;
        const reply = brain.think(text);
        document.getElementById('responseBox').innerHTML = reply.replace(/\\n/g, '<br>');
        speak(reply);
    }

    function speak(text) {
        parrotDiv.classList.add('shaking');
        statusLog.innerText = "🦜 皮皮正在说...";
        
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.pitch = 1.6;
        u.rate = 1.3;
        
        u.onend = () => {
            parrotDiv.classList.remove('shaking');
            statusLog.innerText = "点击按钮继续";
        };
        
        synth.speak(u);
    }

    // --- 4. 备用打字模式 ---
    function enableFallbackMode() {
        typeInput.style.display = 'block';
        statusLog.innerText = "语音不可用，请使用下方输入框 👇";
    }

    function handleType(e) {
        if (e.key === 'Enter') {
            processInput(typeInput.value);
            typeInput.value = '';
        }
    }

    function showError(msg) {
        errorLog.innerText = msg;
        errorLog.style.display = 'block';
    }

</script>
</body>
</html>
"""

components.html(html_code, height=700)
