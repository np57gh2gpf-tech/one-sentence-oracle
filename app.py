import streamlit as st
import streamlit.components.v1 as components

# 1. 页面基础配置
st.set_page_config(page_title="鹦鹉AI对话", page_icon="🦜", layout="centered")

# 2. 注入 CSS 隐藏多余菜单，聚焦体验
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #fceea7; }
    /* 手机端适配优化 */
    iframe { width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# 3. 核心 HTML/JS 代码
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parrot AI Context</title>
    <style>
        /* --- 视觉设计 (保持童趣但更现代化) --- */
        body {
            font-family: "Microsoft YaHei", "Comic Sans MS", sans-serif;
            background-color: #fceea7;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; margin: 0; padding: 10px; box-sizing: border-box;
        }

        .main-card {
            background: white; width: 95%; max-width: 400px;
            padding: 20px; border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border: 4px solid #ff6b6b;
            text-align: center; display: flex; flex-direction: column; align-items: center;
        }

        /* 鹦鹉形象 */
        .avatar-box {
            width: 120px; height: 120px; border-radius: 50%;
            background: #e0f7fa; border: 4px solid #4ecdc4;
            overflow: hidden; margin-bottom: 15px; position: relative;
            display: flex; justify-content: center; align-items: center;
        }
        .emoji-parrot { font-size: 70px; animation: float 3s infinite ease-in-out; }
        
        /* 对话显示区 */
        .chat-history {
            width: 100%; height: 150px; overflow-y: auto;
            background: #f9f9f9; border-radius: 10px; padding: 10px;
            margin-bottom: 15px; border: 1px solid #eee; text-align: left;
            font-size: 14px; color: #333;
        }
        .msg-user { color: #2980b9; margin-bottom: 5px; font-weight: bold; }
        .msg-ai { color: #e67e22; margin-bottom: 10px; }

        /* 控制按钮 */
        .mic-btn {
            width: 70px; height: 70px; border-radius: 50%; border: none;
            background: #ff6b6b; color: white; font-size: 28px;
            box-shadow: 0 6px 0 #c0392b; cursor: pointer; transition: all 0.1s;
        }
        .mic-btn:active { transform: translateY(6px); box-shadow: none; }
        .mic-btn.active { background: #2ecc71; animation: pulse 1.5s infinite; }

        /* 调试/状态信息 */
        .status-bar { font-size: 12px; color: #999; margin-top: 10px; min-height: 18px; }
        .debug-info { 
            font-size: 10px; color: red; margin-top: 5px; 
            background: #fff0f0; padding: 5px; border-radius: 4px;
            display: none; width: 100%; text-align: left;
        }

        /* 动画 */
        @keyframes float { 0%,100% {transform:translateY(0);} 50% {transform:translateY(-6px);} }
        @keyframes pulse { 0% {transform:scale(1);} 50% {transform:scale(1.1);} 100% {transform:scale(1);} }
        .speaking { animation: shake 0.5s infinite; }
        @keyframes shake { 0% {transform:rotate(0deg);} 25% {transform:rotate(5deg);} 75% {transform:rotate(-5deg);} }
    </style>
</head>
<body>

<div class="main-card">
    <div class="avatar-box" id="avatar">
        <div class="emoji-parrot">🦜</div>
    </div>

    <div class="chat-history" id="chatBox">
        <div class="msg-ai">🦜: 你好！我是皮皮！我可以记住我们刚刚聊了什么哦。(记忆容量: 5句)</div>
    </div>

    <button class="mic-btn" id="btn" onclick="toggleMic()">🎤</button>
    <div class="status-bar" id="status">点击麦克风开始说话</div>
    
    <div class="debug-info" id="debugLog"></div>
</div>

<script>
    // ==========================================
    // 1. 🧠 AI 记忆大脑 (Local Logic with Context)
    // ==========================================
    class ParrotBrain {
        constructor() {
            this.memory = []; // 记忆栈：[{role: 'user', text: '...'}, {role: 'ai', text: '...'}]
            this.maxHistory = 5; // 记忆深度
            this.userName = null;
        }

        // 核心处理函数
        process(input) {
            const text = input.trim();
            if (!text) return "呱？没听见！";

            // 1. 更新记忆 (User)
            this.addToMemory('user', text);

            // 2. 生成回复 (AI)
            const reply = this.generateReply(text);

            // 3. 更新记忆 (AI)
            this.addToMemory('ai', reply);

            return reply;
        }

        addToMemory(role, text) {
            this.memory.push({ role, text });
            if (this.memory.length > this.maxHistory * 2) {
                this.memory.shift(); // 保持记忆在限制范围内
            }
        }

        // 这里的逻辑模拟了“理解上下文”
        generateReply(text) {
            // 归一化处理
            const t = text.toLowerCase().replace(/[.,?!。，？！]/g, "");

            // --- A. 上下文回溯能力 ---
            
            // 问之前的对话
            if (t.includes("刚才") || t.includes("刚刚")) {
                if (this.memory.length < 3) return "刚刚？我们才刚开始聊天呀！";
                // 找到上一个用户说的话（倒数第二个记录是AI的，倒数第三个是User的）
                const lastUserMsg = this.memory[this.memory.length - 2]; 
                return `你刚刚说的是："${lastUserMsg.text}" 对不对？`;
            }

            // 问为什么 (简单的逻辑关联)
            if (t.includes("为什么") || t.includes("怎么")) {
                const lastAiMsg = this.memory.length > 1 ? this.memory[this.memory.length - 1] : null;
                if (lastAiMsg && lastAiMsg.text.includes("吃")) return "因为我是一只贪吃的小鹦鹉呀！";
                if (lastAiMsg) return "因为我是皮皮，所以我知道！";
            }

            // --- B. 记忆提取 ---
            
            // 记住名字
            if (t.includes("我叫") || t.includes("我是")) {
                const name = text.replace(/我叫|我是|你好/g, "").replace(/[^\u4e00-\u9fa5a-zA-Z]/g, "");
                if (name) {
                    this.userName = name;
                    return `记住了！你的名字是 ${name}！好听！`;
                }
            }
            // 询问名字
            if (t.includes("我叫什么") || t.includes("我是谁")) {
                if (this.userName) return `你是 ${this.userName} 呀！我记性可好了！`;
                return "你还没告诉我你叫什么名字呢！快告诉我！";
            }

            // --- C. 智能功能 (不设限的感觉) ---
            
            // 算数
            const math = t.match(/(\d+)\s*([加减乘除\+\-\*\/])\s*(\d+)/);
            if (math) {
                const n1 = parseInt(math[1]), op = math[2], n2 = parseInt(math[3]);
                let res = 0;
                if (op === '+' || op === '加') res = n1 + n2;
                if (op === '-' || op === '减') res = n1 - n2;
                if (op === '*' || op === '乘') res = n1 * n2;
                if (op === '/' || op === '除') res = (n2!==0 ? (n1/n2).toFixed(1) : "不能除以0");
                return `这个简单！等于 ${res}！我聪明吧！`;
            }

            // 讲故事
            if (t.includes("故事")) {
                const stories = [
                    "从前有座山，山里有座庙，庙里有只老鹦鹉在讲故事...",
                    "小鸭子想学游泳，可是它忘记带救生圈了，只好在岸边吃冰激凌。",
                    "一只大老虎牙疼，原来是糖吃多了，小朋友不能吃太多糖哦！"
                ];
                return stories[Math.floor(Math.random() * stories.length)];
            }

            // 通用对话 (增加随机性，看起来更像AI)
            const generics = [
                `"${text}" 是什么意思呀？给我讲讲！`,
                "哇，真的吗？然后呢？",
                "我要吃瓜子！还要吃苹果！",
                "你可以考考我算数，或者让我讲故事！"
            ];
            
            // 简单的关键词回应
            if (t.includes("你好")) return "你好呀！你好呀！";
            if (t.includes("再见")) return "拜拜！下次带好吃的来！";
            if (t.includes("笨")) return "你才笨！皮皮最聪明！";
            if (t.includes("喜欢")) return "我也喜欢！但我最喜欢饼干！";

            return generics[Math.floor(Math.random() * generics.length)];
        }
    }

    // ==========================================
    // 2. 🎤 硬件交互层 (Audio System)
    // ==========================================
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    
    // 初始化组件
    const brain = new ParrotBrain();
    const btn = document.getElementById('btn');
    const status = document.getElementById('status');
    const debugLog = document.getElementById('debugLog');
    const chatBox = document.getElementById('chatBox');
    const avatar = document.getElementById('avatar');

    let recognition = null;
    let isListening = false;

    // 日志与诊断函数
    function logDebug(msg) {
        console.log(msg);
        debugLog.style.display = 'block';
        debugLog.innerHTML += "• " + msg + "<br>";
    }

    function appendChat(role, text) {
        const div = document.createElement('div');
        div.className = role === 'user' ? 'msg-user' : 'msg-ai';
        div.innerText = (role === 'user' ? '👤 你: ' : '🦜 鹦鹉: ') + text;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight; // 自动滚动到底部
    }

    // 初始化识别器
    if (!SpeechRecognition) {
        status.innerText = "❌ 浏览器不支持语音";
        logDebug("Fatal: Browser does not support Web Speech API.");
    } else {
        recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false; // 也是为了兼容性，一句一句说
        recognition.interimResults = false;

        recognition.onstart = () => {
            isListening = true;
            btn.classList.add('active');
            status.innerText = "👂 正在听... (请说话)";
            logDebug("Mic started.");
        };

        recognition.onend = () => {
            isListening = false;
            btn.classList.remove('active');
            if (status.innerText.includes("正在听")) status.innerText = "点击麦克风开始";
            logDebug("Mic stopped.");
        };

        recognition.onerror = (e) => {
            isListening = false;
            btn.classList.remove('active');
            status.innerText = "⚠️ 出错了";
            // 翻译错误代码
            let msg = e.error;
            if (e.error === 'not-allowed') msg = "权限被拒绝 (请在浏览器地址栏允许麦克风)";
            if (e.error === 'no-speech') msg = "未检测到声音 (请大声点)";
            if (e.error === 'network') msg = "网络错误 (语音识别需要联网)";
            logDebug("Error: " + msg);
        };

        recognition.onresult = (e) => {
            const transcript = e.results[0][0].transcript;
            logDebug("Heard: " + transcript);
            handleInput(transcript);
        };
    }

    // ==========================================
    // 3. 🎮 控制逻辑 (Controller)
    // ==========================================

    function toggleMic() {
        if (!recognition) {
            alert("你的浏览器不支持语音功能，请使用 Chrome 或 Edge。");
            return;
        }

        // 必须由用户手势触发音频上下文
        if (synth) synth.cancel(); 

        if (isListening) {
            recognition.stop();
        } else {
            try {
                recognition.start();
                status.innerText = "启动中...";
            } catch (err) {
                logDebug("Start failed: " + err.message);
            }
        }
    }

    function handleInput(text) {
        // 1. 上屏
        appendChat('user', text);
        
        // 2. 思考
        status.innerText = "🤔 思考中...";
        // 模拟一点延迟，感觉更像AI
        setTimeout(() => {
            const reply = brain.process(text);
            
            // 3. 回复
            appendChat('ai', reply);
            speak(reply);
        }, 500);
    }

    function speak(text) {
        status.innerText = "🦜 正在说...";
        avatar.classList.add('speaking');
        
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.rate = 1.4; // 语速快一点，像鹦鹉
        u.pitch = 1.5; // 音调高一点
        
        u.onend = () => {
            status.innerText = "点击麦克风继续";
            avatar.classList.remove('speaking');
        };
        
        synth.speak(u);
    }

</script>
</body>
</html>
"""

# 4. 渲染 (高度调高一点，适应对话记录)
components.html(html_code, height=750)
