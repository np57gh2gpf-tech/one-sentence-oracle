import streamlit as st
import streamlit.components.v1 as components

# --- 页面配置 ---
st.set_page_config(page_title="智能鹦鹉皮皮", page_icon="🦜", layout="centered")

# 隐藏多余的菜单
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
/* 手机端优化 */
@media (max-width: 600px) {
    .container { width: 95% !important; }
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 核心代码 (HTML + JS + CSS) ---
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Smart Parrot</title>
    <style>
        /* 样式区：保持童趣风格 */
        body {
            font-family: "Comic Sans MS", "YouYuan", "幼圆", sans-serif;
            background-color: #fceea7;
            background-image: radial-gradient(#ffd700 10%, transparent 10%);
            background-size: 30px 30px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; margin: 0; overflow: hidden;
            touch-action: manipulation;
        }

        .container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 25px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 90%; max-width: 380px;
            text-align: center;
            border: 6px solid #ff6b6b;
            position: relative;
        }

        h1 { color: #ff6b6b; margin: 0 0 15px 0; font-size: 24px; }

        /* 鹦鹉显示区 */
        .parrot-wrapper {
            position: relative;
            width: 180px; height: 180px;
            margin: 0 auto 20px auto;
        }

        .parrot-display {
            width: 100%; height: 100%;
            border-radius: 50%;
            overflow: hidden;
            border: 6px solid #4ecdc4;
            background-color: #e0f7fa;
            position: relative;
            z-index: 2;
        }

        .parrot-img { width: 100%; height: 100%; object-fit: cover; }
        .parrot-emoji { font-size: 90px; line-height: 180px; animation: float 3s ease-in-out infinite; }

        /* 气泡对话框 */
        .chat-bubble {
            background-color: #4ecdc4; color: white;
            padding: 15px; border-radius: 18px;
            min-height: 50px; margin-bottom: 25px;
            font-size: 18px; line-height: 1.4;
            position: relative;
            box-shadow: 4px 4px 0px #2a9d8f;
            display: flex; align-items: center; justify-content: center;
        }
        .chat-bubble::after {
            content: ''; position: absolute; top: -12px; left: 50%; margin-left: -10px;
            border-width: 0 12px 12px; border-style: solid; border-color: #4ecdc4 transparent;
        }

        /* 按钮区 */
        .controls { display: flex; flex-direction: column; align-items: center; gap: 10px; }
        
        .mic-btn {
            width: 80px; height: 80px; border-radius: 50%; border: none;
            background-color: #ff6b6b; color: white; font-size: 32px;
            box-shadow: 0 6px 0 #c0392b; cursor: pointer;
            transition: transform 0.1s;
        }
        .mic-btn:active { box-shadow: 0 0 0; transform: translateY(6px); }
        .mic-btn.listening { background-color: #2ecc71; animation: pulse 1.5s infinite; }
        .mic-btn.disabled { background-color: #bdc3c7; box-shadow: none; cursor: not-allowed; }

        .hint { font-size: 14px; color: #7f8c8d; margin-top: 5px; }

        /* 动画定义 */
        @keyframes shake {
            0% { transform: rotate(0deg); } 20% { transform: rotate(-5deg); }
            40% { transform: rotate(5deg); } 60% { transform: rotate(-5deg); } 100% { transform: rotate(0deg); }
        }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        
        .talking { animation: shake 0.5s infinite; }
    </style>
</head>
<body>

<div class="container">
    <h1>🦜 聪明的皮皮</h1>
    
    <div class="parrot-wrapper">
        <div class="parrot-display" id="parrotContainer">
            <img src="parrot.jpg" class="parrot-img" id="parrotImg" onerror="this.style.display='none'; document.getElementById('emoji').style.display='block';">
            <div id="emoji" class="parrot-emoji" style="display:none">🦜</div>
        </div>
    </div>

    <div class="chat-bubble" id="responseBox">
        我是皮皮！<br>我会算数和讲故事哦！
    </div>

    <div class="controls">
        <button class="mic-btn" id="micBtn" onclick="toggleMic()">🎤</button>
        <div class="hint" id="statusText">点击开始说话</div>
    </div>
</div>

<script>
    // --- 智能核心 (Brain) ---
    // 这里并没有连接云端API，而是用逻辑模拟了一个聪明的鹦鹉
    
    class ParrotBrain {
        constructor() {
            this.name = "皮皮";
            this.stories = [
                "从前有只小猪，它吃太饱了，结果飘到了天上！变成了飞猪！",
                "有一天太阳公公睡懒觉，月亮婆婆就出来替它值班，结果大家都睡着了。",
                "小白兔去钓鱼，钓上来一只螃蟹，螃蟹说：'快放开我，我要去剪头发！'"
            ];
        }

        think(text) {
            text = text.replace(/[.,?!。，？！]/g, "").trim(); // 清理标点
            
            // 1. 数学能力 (比如 "1加1等于几", "3乘5")
            if (text.match(/(\d+).*([加减乘除]).*(\d+)/)) {
                return this.doMath(text);
            }
            
            // 2. 报时能力
            if (text.includes("几点") || text.includes("时间")) {
                const now = new Date();
                return `现在是 ${now.getHours()}点 ${now.getMinutes()}分！该吃点心了吗？`;
            }

            // 3. 互动指令
            if (text.includes("故事")) return this.getStory();
            if (text.includes("名字") || text.includes("是谁")) return `我是${this.name}！最聪明的鹦鹉！`;
            if (text.includes("你好") || text.includes("Hello")) return "你好呀！你好呀！要吃饼干吗？";
            
            // 4. 简单的知识库
            if (text.includes("天空") && text.includes("颜色")) return "天空是蓝色的！像我的羽毛一样！";
            if (text.includes("草") && text.includes("颜色")) return "草是绿色的！里面有虫子吃！";
            if (text.includes("苹果")) return "苹果红红的，甜甜的，好吃！";
            if (text.includes("爸爸") || text.includes("妈妈")) return "爸爸妈妈最爱你！呱！";
            
            // 5. 情绪反应
            if (text.includes("笨") || text.includes("傻") || text.includes("坏")) return "皮皮生气了！不理你了！扑棱扑棱！💢";
            if (text.includes("棒") || text.includes("聪明") || text.includes("爱你")) return "害羞害羞！皮皮也爱你！❤️";
            if (text.includes("再见") || text.includes("拜拜")) return "再见！记得下次带好吃的来！";

            // 6. 默认回复 (加上一点随机性，不单纯复读)
            const confusion = [
                "我不懂你的意思，但我饿了！",
                "你说啥？风太大听不清！",
                "呱？能不能再说一遍？",
                "扑棱扑棱！你说：" + text
            ];
            return confusion[Math.floor(Math.random() * confusion.length)];
        }

        doMath(text) {
            try {
                // 简单的中文数字转换逻辑可以扩展，这里只处理阿拉伯数字
                const match = text.match(/(\d+)\s*([加减乘除\+\-\*\/])\s*(\d+)/);
                if (match) {
                    let n1 = parseInt(match[1]);
                    let op = match[2];
                    let n2 = parseInt(match[3]);
                    let res = 0;
                    if (op === '加' || op === '+') res = n1 + n2;
                    else if (op === '减' || op === '-') res = n1 - n2;
                    else if (op === '乘' || op === '*') res = n1 * n2;
                    else if (op === '除' || op === '/') res = Math.floor(n1 / n2);
                    return `我知道！是 ${res}！我厉害吧！`;
                }
            } catch (e) { return "太难了！皮皮算不过来！"; }
            return "这是数学题吗？皮皮只会数瓜子！";
        }

        getStory() {
            const randomStory = this.stories[Math.floor(Math.random() * this.stories.length)];
            return "讲故事啦！" + randomStory + " 呱！";
        }
    }

    // --- 语音与界面逻辑 ---
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    let recognition;
    let isSpeaking = false;
    const brain = new ParrotBrain();
    
    const micBtn = document.getElementById('micBtn');
    const responseBox = document.getElementById('responseBox');
    const parrotDiv = document.getElementById('parrotContainer');
    const statusText = document.getElementById('statusText');

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false;

        recognition.onstart = () => {
            micBtn.classList.add('listening');
            statusText.innerText = "正在听...";
            responseBox.innerText = "...";
        };

        recognition.onend = () => {
            micBtn.classList.remove('listening');
            if (!isSpeaking) statusText.innerText = "点击说话";
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            handleInput(transcript);
        };
        
        recognition.onerror = (e) => {
             statusText.innerText = "没听清，再试一次";
             micBtn.classList.remove('listening');
        };
    } else {
        responseBox.innerText = "浏览器不支持语音，请用 Chrome！";
        micBtn.classList.add('disabled');
    }

    function toggleMic() {
        if (!recognition) return;
        if (micBtn.classList.contains('listening')) {
            recognition.stop();
        } else {
            // 停止之前的说话
            synth.cancel();
            isSpeaking = false;
            parrotDiv.classList.remove('talking');
            recognition.start();
        }
    }

    function handleInput(text) {
        // 1. 思考
        const reply = brain.think(text);
        
        // 2. 显示回复
        responseBox.innerHTML = reply;
        
        // 3. 说话
        speak(reply);
    }

    function speak(text) {
        if (!text) return;
        isSpeaking = true;
        statusText.innerText = "皮皮正在说...";
        parrotDiv.classList.add('talking');

        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.pitch = 1.6; // 鹦鹉音调高
        u.rate = 1.2;  // 语速快
        
        u.onend = () => {
            isSpeaking = false;
            parrotDiv.classList.remove('talking');
            statusText.innerText = "点击说话";
        };
        
        synth.speak(u);
    }
</script>
</body>
</html>
"""

components.html(html_code, height=700)
