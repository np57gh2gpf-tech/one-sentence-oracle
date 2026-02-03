import streamlit as st
import streamlit.components.v1 as components

# 页面基础设置
st.set_page_config(page_title="超级皮皮 (完全版)", page_icon="🦜", layout="centered")

# 隐藏不必要的菜单
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 核心代码 (包含最新的逻辑大脑) ---
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Smart Parrot Final</title>
    <style>
        /* 界面样式 - 保持可爱风 */
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

        /* 鹦鹉头像区 */
        .parrot-wrapper {
            width: 160px; height: 160px; margin: 0 auto 20px; position: relative;
        }
        .parrot-display {
            width: 100%; height: 100%; border-radius: 50%; overflow: hidden;
            border: 5px solid #4ecdc4; background-color: #e0f7fa; 
            display: flex; align-items: center; justify-content: center;
        }
        .parrot-img { width: 100%; height: 100%; object-fit: cover; }
        .parrot-emoji { font-size: 90px; animation: float 3s ease-in-out infinite; }

        /* 对话气泡 */
        .chat-bubble {
            background-color: #4ecdc4; color: white; padding: 15px; border-radius: 18px;
            min-height: 60px; margin-bottom: 20px; font-size: 1.2em; line-height: 1.4;
            position: relative; box-shadow: 3px 3px 0px #2a9d8f;
            display: flex; align-items: center; justify-content: center; flex-direction: column;
        }
        .chat-bubble::after {
            content: ''; position: absolute; top: -10px; left: 50%; margin-left: -10px;
            border-width: 0 10px 10px; border-style: solid; border-color: #4ecdc4 transparent;
        }
        
        /* 状态文字 */
        .status-text { font-size: 14px; color: #888; margin-top: 10px; }

        /* 按钮 */
        .control-btn {
            width: 80px; height: 80px; border-radius: 50%; border: none;
            background-color: #ff6b6b; color: white; font-size: 30px;
            box-shadow: 0 5px 0 #c0392b; cursor: pointer; transition: all 0.2s;
        }
        .control-btn:active { transform: translateY(5px); box-shadow: 0 0 0; }
        .control-btn.listening { background-color: #2ecc71; animation: pulse 1.5s infinite; }

        /* 动画 */
        @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-8px);} }
        @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.1);} 100% {transform: scale(1);} }
        .shaking { animation: shake 0.4s infinite; }
        @keyframes shake { 0% {transform: rotate(0deg);} 25% {transform: rotate(5deg);} 75% {transform: rotate(-5deg);} }

    </style>
</head>
<body>

<div class="container">
    <h1>🦜 聪明的皮皮</h1>
    
    <div class="parrot-wrapper">
        <div class="parrot-display" id="parrotContainer">
            <img src="parrot.jpg" class="parrot-img" onerror="this.style.display='none'; document.getElementById('emoji').style.display='block';">
            <div id="emoji" class="parrot-emoji" style="display:none">🦜</div>
        </div>
    </div>

    <div class="chat-bubble" id="responseBox">
        你好！我是皮皮！<br>我们可以聊天、讲故事、做算术！
    </div>

    <button class="control-btn" id="micBtn" onclick="toggleConversation()">🎤</button>
    <div class="status-text" id="statusLog">点击麦克风开始聊天</div>
</div>

<script>
    // --- 🧠 大脑逻辑 (Brain) ---
    // 这里是皮皮怎么思考的地方
    class ParrotBrain {
        constructor() {
            this.name = "皮皮";
            this.userName = ""; // 记住小朋友名字
            this.stories = [
                "从前有只小猪，它吃太饱了，结果飘到了天上！变成了飞猪！🐷",
                "有一天太阳公公睡懒觉，月亮婆婆就出来替它值班，结果星星都笑醒了。⭐",
                "小白兔去钓鱼，钓上来一只螃蟹，螃蟹说：快放开我，我要去剪头发！🦀",
                "小蜗牛去爬山，爬呀爬，爬了三天，终于...爬到了门口的花盆上！🐌"
            ];
        }

        think(text) {
            // 1. 预处理：去掉标点
            const cleanText = text.replace(/[.,?!。，？！]/g, "").trim();
            if (!cleanText) return "呱？我没听清！";

            console.log("思考中: " + cleanText);

            // 2. 核心逻辑判断

            // --- 名字记忆 ---
            if (cleanText.includes("我叫")) {
                this.userName = cleanText.split("我叫")[1]; // 截取名字
                return `记住了！你叫${this.userName}！名字真好听！`;
            }
            if (cleanText.includes("我是谁")) {
                return this.userName ? `你是${this.userName}呀！我没忘！` : "你还没告诉我你叫什么呢！";
            }

            // --- 讲故事 ---
            if (cleanText.includes("故事")) {
                const story = this.stories[Math.floor(Math.random() * this.stories.length)];
                return "好哒！讲个故事：\n" + story;
            }

            // --- 算数 (识别 '1加2' 或 '3+5') ---
            // 这是一个简单的正则，提取两个数字
            const mathMatch = cleanText.match(/(\d+)\s*([加减\+\-])\s*(\d+)/);
            if (mathMatch) {
                const n1 = parseInt(mathMatch[1]);
                const op = mathMatch[2];
                const n2 = parseInt(mathMatch[3]);
                let res = 0;
                if(op === '加' || op === '+') res = n1 + n2;
                if(op === '减' || op === '-') res = n1 - n2;
                return `我知道！${n1} ${op} ${n2} 等于 ${res}！我聪明吧！`;
            }

            // --- 知识问答 (关键词匹配) ---
            if (cleanText.includes("名字")) return "我叫皮皮！是一只漂亮的鹦鹉！";
            if (cleanText.includes("几岁")) return "皮皮三岁啦！";
            if (cleanText.includes("你好")) return "你好呀！你好呀！要吃饼干吗？";
            if (cleanText.includes("天空")) return "天空是蓝色的！Blue!";
            if (cleanText.includes("草")) return "草是绿色的！Green!";
            if (cleanText.includes("苹果")) return "苹果红红的，甜甜的！";
            if (cleanText.includes("谢谢")) return "不客气！扑棱扑棱！";
            if (cleanText.includes("吃")) return "我喜欢吃瓜子，还喜欢吃饼干！🍪";
            if (cleanText.includes("爸爸")) return "爸爸最辛苦了！";
            if (cleanText.includes("妈妈")) return "妈妈最漂亮！";
            if (cleanText.includes("笨") || cleanText.includes("傻")) return "皮皮不笨！皮皮生气了！💢";
            if (cleanText.includes("爱")) return "皮皮也爱你！么么哒！❤️";
            
            // --- 兜底逻辑 (如果什么都没匹配到) ---
            // 为了不只是复读，增加一些“不知道”的可爱回答
            const fallbacks = [
                "呱？这是什么意思呀？",
                "皮皮没听懂，但是觉得很厉害！",
                "我要吃饼干！你刚刚说什么？",
                "扑棱扑棱！你说：" + cleanText
            ];
            return fallbacks[Math.floor(Math.random() * fallbacks.length)];
        }
    }

    // --- 👂 & 🗣️ 听觉与视觉 (IO System) ---
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    let recognition;
    const brain = new ParrotBrain();
    
    // 状态标记
    let isConversing = false; // 是否处于连续对话模式

    const micBtn = document.getElementById('micBtn');
    const responseBox = document.getElementById('responseBox');
    const parrotDiv = document.getElementById('parrotContainer');
    const statusLog = document.getElementById('statusLog');

    // 初始化检查
    if (!SpeechRecognition) {
        responseBox.innerHTML = "❌ 浏览器不支持<br>请使用 Chrome 或 Edge";
        micBtn.style.display = 'none';
    } else {
        recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false; // 听完一句就停，处理完再说
        recognition.interimResults = false;

        recognition.onstart = () => {
            micBtn.classList.add('listening');
            statusLog.innerText = "👂 正在听...";
        };

        recognition.onend = () => {
            micBtn.classList.remove('listening');
            // 如果不在说话状态，且处于对话模式，可能需要处理（但在onresult里处理更佳）
        };

        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            processInteraction(text);
        };
        
        recognition.onerror = (e) => {
            console.log("Error:", e.error);
            if (e.error === 'not-allowed') {
                statusLog.innerText = "❌ 请允许麦克风权限";
                isConversing = false;
            } else {
                // 如果没听清，稍微等一下再尝试重新听（如果是连续模式）
                statusLog.innerText = "没听清...";
                if(isConversing) setTimeout(startListening, 1000);
            }
        };
    }

    // 点击按钮的主开关
    function toggleConversation() {
        if (!recognition) return;

        if (isConversing) {
            // 停止一切
            isConversing = false;
            recognition.stop();
            synth.cancel();
            statusLog.innerText = "点击麦克风开始聊天";
            responseBox.innerText = "休息啦！再见！";
        } else {
            // 开始
            isConversing = true;
            // 激活音频上下文（解决手机不发声问题）
            synth.cancel();
            startListening();
        }
    }

    function startListening() {
        if(!isConversing) return;
        try {
            recognition.start();
        } catch(e) {
            console.log("Already started");
        }
    }

    function processInteraction(text) {
        // 1. 显示听到的话
        statusLog.innerText = "听到: " + text;
        
        // 2. 大脑思考
        const reply = brain.think(text);
        
        // 3. 显示回答
        responseBox.innerHTML = reply.replace(/\\n/g, '<br>');
        
        // 4. 说话
        speak(reply);
    }

    function speak(text) {
        parrotDiv.classList.add('shaking'); // 开始动
        statusLog.innerText = "🦜 正在说...";
        
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.pitch = 1.6; // 语调高
        u.rate = 1.3;  // 语速快
        
        u.onend = () => {
            parrotDiv.classList.remove('shaking'); // 停止动
            
            // 🌟 关键点：说完之后，自动重新开始听！实现“连续对话”
            if (isConversing) {
                statusLog.innerText = "准备听下一句...";
                setTimeout(startListening, 500); // 休息0.5秒再听
            } else {
                statusLog.innerText = "点击麦克风开始聊天";
            }
        };
        
        synth.speak(u);
    }

</script>
</body>
</html>
"""

components.html(html_code, height=700)
