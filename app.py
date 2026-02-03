import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="皮皮诊断版", page_icon="🦜", layout="centered")

# 隐藏多余元素
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parrot Debug</title>
    <style>
        body {
            font-family: "Comic Sans MS", "Microsoft YaHei", sans-serif;
            background-color: #fceea7;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; margin: 0;
        }
        .container {
            background-color: #fff; padding: 20px; border-radius: 20px;
            width: 90%; max-width: 380px; text-align: center; border: 5px solid #ff6b6b;
        }
        .parrot-box {
            width: 150px; height: 150px; margin: 0 auto 15px; border-radius: 50%;
            background: #e0f7fa; border: 5px solid #4ecdc4; overflow: hidden;
            display: flex; align-items: center; justify-content: center;
        }
        .parrot-emoji { font-size: 80px; }
        
        .chat-bubble {
            background: #4ecdc4; color: white; padding: 15px; border-radius: 15px;
            min-height: 50px; margin-bottom: 20px; position: relative;
        }
        
        /* 按钮样式 */
        .btn {
            width: 100%; padding: 15px; border: none; border-radius: 50px;
            background: #ff6b6b; color: white; font-size: 18px; font-weight: bold;
            cursor: pointer; box-shadow: 0 4px #c0392b; margin-bottom: 10px;
        }
        .btn:active { transform: translateY(4px); box-shadow: 0 0; }
        .btn.active { background: #2ecc71; box-shadow: 0 4px #27ae60; animation: pulse 1s infinite; }
        
        /* 错误日志区 */
        #log {
            font-size: 12px; color: #e74c3c; background: #eee; 
            padding: 5px; margin-top: 10px; border-radius: 5px;
            text-align: left; min-height: 20px; word-break: break-all;
        }

        @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.02);} 100% {transform: scale(1);} }
        .shaking { animation: shake 0.5s infinite; }
        @keyframes shake { 0% {transform: rotate(0deg);} 25% {transform: rotate(5deg);} 75% {transform: rotate(-5deg);} }
    </style>
</head>
<body>

<div class="container">
    <h3>🦜 修复版皮皮</h3>
    
    <div class="parrot-box" id="parrot">
        <div class="parrot-emoji">🦜</div>
    </div>

    <div class="chat-bubble" id="response">点击按钮，允许麦克风！</div>

    <button class="btn" id="micBtn" onclick="toggleMic()">点击开始说话</button>
    
    <div id="log">系统状态: 等待操作...</div>
</div>

<script>
    // --- 日志工具 ---
    const logDiv = document.getElementById('log');
    function log(msg) {
        console.log(msg);
        logDiv.innerText = "状态: " + msg;
    }

    // --- 核心变量 ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    let recognition;
    let isListening = false;
    
    const btn = document.getElementById('micBtn');
    const box = document.getElementById('response');
    const parrot = document.getElementById('parrot');

    // --- 初始化检查 ---
    if (!SpeechRecognition) {
        log("❌ 致命错误: 你的浏览器不支持语音识别(Web Speech API)。请使用 Chrome/Edge。");
        box.innerText = "请换个浏览器 (Chrome)";
        btn.disabled = true;
        btn.style.background = "#ccc";
    } else {
        log("✅ 浏览器支持检测通过。准备就绪。");
        recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            isListening = true;
            btn.classList.add('active');
            btn.innerText = "正在听... (点击停止)";
            box.innerText = "👂 我在听...";
            log("🎤 麦克风已激活");
        };

        recognition.onend = () => {
            isListening = false;
            btn.classList.remove('active');
            btn.innerText = "点击开始说话";
            log("🛑 录音结束");
        };

        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            log("收到语音: " + text);
            box.innerText = "你说: " + text;
            reply(text);
        };

        recognition.onerror = (event) => {
            isListening = false;
            btn.classList.remove('active');
            btn.innerText = "点击开始说话";
            
            // 详细报错翻译
            let errorMsg = event.error;
            if (event.error === 'not-allowed') errorMsg = "❌ 权限被拒绝！请在浏览器设置中允许麦克风。";
            if (event.error === 'no-speech') errorMsg = "⚠️ 没听到声音，请大声点。";
            if (event.error === 'network') errorMsg = "❌ 网络错误，请检查连接。";
            
            log(errorMsg);
            box.innerText = "出错啦: " + event.error;
        };
    }

    // --- 交互控制 ---
    function toggleMic() {
        if (!recognition) return;
        
        if (isListening) {
            recognition.stop();
        } else {
            // 这是一个必须要有的步骤：激活语音播放器
            synth.cancel(); 
            try {
                recognition.start();
                log("尝试启动麦克风...");
            } catch (e) {
                log("启动失败: " + e.message);
            }
        }
    }

    // --- 简单回复逻辑 ---
    function reply(text) {
        let answer = "呱！" + text; // 默认复读
        
        if (text.includes("你好")) answer = "你好呀！我是皮皮！";
        if (text.includes("名字")) answer = "我叫皮皮！";
        if (text.includes("吃")) answer = "我要吃坚果！";
        if (text.includes("算数")) answer = "我数学可好了！";
        
        // 延迟一点点播放
        setTimeout(() => {
            box.innerText = answer;
            speak(answer);
        }, 500);
    }

    function speak(text) {
        if (!synth) {
            log("浏览器不支持语音合成");
            return;
        }
        parrot.classList.add('shaking');
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.onend = () => { parrot.classList.remove('shaking'); };
        synth.speak(u);
    }

</script>
</body>
</html>
"""

components.html(html_code, height=600)
