import streamlit as st
import streamlit.components.v1 as components

# 设置网页标签页标题
st.set_page_config(page_title="鹦鹉皮皮", page_icon="🦜")

# 隐藏Streamlit默认的菜单，让界面更像个独立APP
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 定义我们的鹦鹉网页代码（HTML+CSS+JS）
# 注意：这里我们整合了语音版，并做了自适应调整
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: "Comic Sans MS", "YouYuan", "幼圆", sans-serif;
            background-color: #fceea7;
            background-image: radial-gradient(#ffd700 10%, transparent 10%);
            background-size: 30px 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden; /* 防止出现双滚动条 */
        }
        .container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 25px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 400px;
            text-align: center;
            border: 5px solid #ff6b6b;
            position: relative;
        }
        h1 { color: #ff6b6b; margin: 5px 0 15px 0; font-size: 24px; }
        .parrot-display {
            width: 180px;
            height: 180px;
            margin: 0 auto 15px auto;
            border-radius: 50%;
            overflow: hidden;
            border: 6px solid #4ecdc4;
            background-color: #e0f7fa;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .parrot-img { width: 100%; height: 100%; object-fit: cover; }
        .parrot-emoji { font-size: 80px; animation: bounce 2s infinite; }
        
        .chat-bubble {
            background-color: #4ecdc4;
            color: white;
            padding: 10px;
            border-radius: 15px;
            min-height: 40px;
            margin-bottom: 20px;
            font-size: 1.1em;
            position: relative;
            box-shadow: 3px 3px 0px #2a9d8f;
        }
        .chat-bubble::after {
            content: ''; position: absolute; top: -10px; left: 50%; margin-left: -10px;
            border-width: 0 10px 10px; border-style: solid; border-color: #4ecdc4 transparent;
        }
        .control-btn {
            width: 70px; height: 70px; border-radius: 50%; border: none;
            background-color: #ff6b6b; color: white; font-size: 28px;
            box-shadow: 0 5px 0 #c0392b; cursor: pointer; margin-bottom: 5px;
        }
        .control-btn:active { box-shadow: 0 0 0; transform: translateY(5px); }
        .control-btn.active { background-color: #e74c3c; animation: pulse-red 1s infinite; }
        
        @keyframes shake {
            0% { transform: rotate(0deg); } 25% { transform: rotate(5deg); }
            50% { transform: rotate(0deg); } 75% { transform: rotate(-5deg); } 100% { transform: rotate(0deg); }
        }
        @keyframes pulse-red { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        .shaking { animation: shake 0.4s infinite; }
    </style>
</head>
<body>

<div class="container">
    <h1>🦜 鹦鹉皮皮</h1>
    
    <div class="parrot-display" id="parrotContainer">
        <img src="parrot.jpg" class="parrot-img" id="parrotImg" onerror="this.style.display='none'; document.getElementById('emoji').style.display='block';">
        <div id="emoji" class="parrot-emoji" style="display:none">🦜</div>
    </div>

    <div class="chat-bubble" id="responseBox">点下面的话筒<br>跟我说话！呱！</div>

    <button class="control-btn" id="micBtn" onclick="toggleListening()">🎤</button>
    <div style="color:#888; font-size:12px;">点击开始 / 停止</div>
</div>

<script>
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    let recognition;
    let isSpeaking = false;
    const btn = document.getElementById('micBtn');
    const box = document.getElementById('responseBox');
    const parrot = document.getElementById('parrotContainer');

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false;
        
        recognition.onstart = () => { btn.classList.add('active'); box.innerText = "👂 在听你说..."; };
        recognition.onend = () => { if(!isSpeaking) btn.classList.remove('active'); };
        recognition.onresult = (e) => { processSpeech(e.results[0][0].transcript); };
    } else {
        box.innerText = "请使用 Chrome 浏览器！";
    }

    function toggleListening() {
        if (!recognition) return;
        if (btn.classList.contains('active')) {
            recognition.stop();
            btn.classList.remove('active');
            synth.cancel();
            box.innerText = "😴 休息中";
        } else {
            synth.cancel(); // 激活音频上下文
            recognition.start();
        }
    }

    function processSpeech(text) {
        recognition.stop();
        let reply = getReply(text);
        box.innerText = reply;
        speak(reply);
    }

    function getReply(text) {
        if (text.includes("名字")) return "我是皮皮！呱！";
        if (text.includes("吃")) return "我要吃饼干！还要吃苹果！🍎";
        if (text.includes("笨") || text.includes("傻")) return "你才笨！略略略！💢";
        if (text.includes("唱歌")) return "两只老虎~ 两只老虎~ 🎵";
        const prefix = ["呱！", "你说：", "扑棱扑棱！"];
        return prefix[Math.floor(Math.random()*prefix.length)] + text + "！";
    }

    function speak(text) {
        isSpeaking = true;
        parrot.classList.add('shaking');
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN'; u.pitch = 1.8; u.rate = 1.3;
        u.onend = () => { 
            isSpeaking = false; 
            parrot.classList.remove('shaking'); 
            // 自动重新开始听
            if(btn.classList.contains('active')) try{recognition.start();}catch(e){}
        };
        synth.speak(u);
    }
</script>
</body>
</html>
"""

# 使用Streamlit组件渲染HTML
# height设置得高一点以容纳整个界面
components.html(html_code, height=650)
