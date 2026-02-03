import streamlit as st
import streamlit.components.v1 as components

# --- 页面配置 ---
st.set_page_config(page_title="超级鹦鹉皮皮", page_icon="🦜", layout="centered")

# 隐藏多余菜单
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
@media (max-width: 600px) { .container { width: 95% !important; } }
</style>
""", unsafe_allow_html=True)

# --- 核心代码 (HTML + JS + CSS) ---
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Super Parrot</title>
    <style>
        body {
            font-family: "Comic Sans MS", "YouYuan", "幼圆", sans-serif;
            background-color: #fceea7;
            background-image: radial-gradient(#ffd700 10%, transparent 10%);
            background-size: 30px 30px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; margin: 0; overflow: hidden; touch-action: manipulation;
        }
        .container {
            background-color: #ffffff; padding: 20px; border-radius: 25px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 90%; max-width: 380px;
            text-align: center; border: 6px solid #ff6b6b; position: relative;
        }
        h1 { color: #ff6b6b; margin: 0 0 10px 0; font-size: 22px; }
        
        /* 鹦鹉显示区 */
        .parrot-wrapper { width: 160px; height: 160px; margin: 0 auto 15px auto; position: relative; }
        .parrot-display {
            width: 100%; height: 100%; border-radius: 50%; overflow: hidden;
            border: 5px solid #4ecdc4; background-color: #e0f7fa; position: relative;
        }
        .parrot-img { width: 100%; height: 100%; object-fit: cover; }
        .parrot-emoji { font-size: 80px; line-height: 160px; animation: float 3s ease-in-out infinite; }
        
        /* 状态标签 */
        .mode-badge {
            position: absolute; top: -10px; right: -10px; background: #9b59b6; color: white;
            padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; transform: rotate(10deg);
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2); display: none;
        }

        /* 气泡 */
        .chat-bubble {
            background-color: #4ecdc4; color: white; padding: 15px; border-radius: 18px;
            min-height: 60px; margin-bottom: 20px; font-size: 18px; line-height: 1.4;
            position: relative; box-shadow: 4px 4px 0px #2a9d8f;
            display: flex; align-items: center; justify-content: center; flex-direction: column;
        }
        .chat-bubble::after {
            content: ''; position: absolute; top: -12px; left: 50%; margin-left: -10px;
            border-width: 0 12px 12px; border-style: solid; border-color: #4ecdc4 transparent;
        }
        .sub-text { font-size: 12px; opacity: 0.8; margin-top: 5px; }

        /* 按钮 */
        .controls { display: flex; flex-direction: column; align-items: center; gap: 8px; }
        .mic-btn {
            width: 75px; height: 75px; border-radius: 50%; border: none;
            background-color: #ff6b6b; color: white; font-size: 30px;
            box-shadow: 0 6px 0 #c0392b; cursor: pointer; transition: transform 0.1s;
        }
        .mic-btn:active { box-shadow: 0 0 0; transform: translateY(6px); }
        .mic-btn.listening { background-color: #2ecc71; animation: pulse 1.5s infinite; }
        .hint { font-size: 14px; color: #7f8c8d; }

        /* 动画 */
        @keyframes shake { 0% {transform: rotate(0deg);} 25% {transform: rotate(5deg);} 75% {transform: rotate(-5deg);} 100% {transform: rotate(0deg);} }
        @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.1);} 100% {transform: scale(1);} }
        @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-8px);} }
        .talking { animation: shake 0.4s infinite; }
    </style>
</head>
<body>

<div class="container">
    <div id="modeBadge" class="mode-badge">🎮 游戏模式</div>
    <h1>🦜 超级皮皮</h1>
    
    <div class="parrot-wrapper">
        <div class="parrot-display" id="parrotContainer">
            <img src="parrot.jpg" class="parrot-img" id="parrotImg" onerror="this.style.display='none'; document.getElementById('emoji').style.display='block';">
            <div id="emoji" class="parrot-emoji" style="display:none">🦜</div>
        </div>
    </div>

    <div class="chat-bubble" id="responseBox">
        <span>你好！我是皮皮！</span>
        <span class="sub-text">按住按钮说话</span>
    </div>

    <div class="controls">
        <button class="mic-btn" id="micBtn" onmousedown="startListen()" onmouseup="stopListen()" ontouchstart="startListen()" ontouchend="stopListen()">🎤</button>
        <div class="hint" id="statusText">按住说话 / 松开结束</div>
    </div>
</div>

<script>
    // --- 🧠 鹦鹉大脑 (AI Core) ---
    class SuperBrain {
        constructor() {
            this.name = "皮皮";
            this.user_name = ""; // 记忆小朋友名字
            this.mode = "chat"; // chat(聊天), riddle(猜谜), math(算数), roleplay(角色扮演)
            this.current_answer = ""; // 当前问题的答案
            this.riddles = [
                {q: "身体白又胖，常在泥中滚，爱吃大萝卜。猜个动物？", a: "猪"},
                {q: "耳朵长，尾巴短，红眼睛，白毛衫。猜个动物？", a: "兔子"},
                {q: "一位游泳家，说话呱呱呱，小时有尾巴，长大掉尾巴。猜个动物？", a: "青蛙"},
                {q: "小小诸葛亮，独坐中军帐，摆下八卦阵，专捉飞来将。猜个昆虫？", a: "蜘蛛"},
                {q: "两只翅膀大，色彩真漂亮，爱在花丛飞。猜个昆虫？", a: "蝴蝶"}
            ];
            this.math_level = 10; // 算数难度
        }

        process(text) {
            // 预处理
            const cleanText = text.replace(/[.,?!。，？！]/g, "").trim();
            if (!cleanText) return "呱？你没说话呀！";

            // 1. 全局指令 (随时可以触发)
            if (cleanText.includes("不玩了") || cleanText.includes("退出") || cleanText.includes("普通")) {
                this.mode = "chat";
                updateBadge(false);
                return "好哒！回到聊天模式啦！想聊什么？";
            }
            if (cleanText.includes("变身奥特曼")) {
                this.mode = "roleplay";
                updateBadge("🦸 奥特曼模式");
                return "哔哔哔！我是皮皮奥特曼！我们要去打怪兽吗？";
            }

            // 2. 状态机分流
            if (this.mode === "riddle") return this.handleRiddle(cleanText);
            if (this.mode === "math") return this.handleMath(cleanText);
            if (this.mode === "roleplay") return this.handleRoleplay(cleanText);

            // 3. 默认聊天模式逻辑
            return this.handleChat(cleanText);
        }

        // --- 聊天模式逻辑 ---
        handleChat(text) {
            // 触发游戏
            if (text.includes("猜谜") || text.includes("游戏")) {
                this.mode = "riddle";
                updateBadge("🧩 猜谜模式");
                return this.nextRiddle();
            }
            if (text.includes("算数") || text.includes("考试")) {
                this.mode = "math";
                updateBadge("➕ 算数模式");
                return this.nextMath();
            }

            // 记忆系统
            if (text.match(/我叫(.*)/)) {
                this.user_name = text.match(/我叫(.*)/)[1];
                return `记住了！你叫${this.user_name}！名字真好听！`;
            }
            if (text.includes("我叫什么") || text.includes("我是谁")) {
                return this.user_name ? `你叫${this.user_name}呀！我没忘！` : "哎呀，你还没告诉我你叫什么呢！";
            }

            // 知识与互动
            if (text.includes("几岁")) return "我三岁啦！你几岁？";
            if (text.includes("苹果")) return "Apple! 苹果是红色的！";
            if (text.includes("香蕉")) return "Banana! 香蕉是黄色的！";
            if (text.includes("狗")) return "Dog! 汪汪汪！";
            if (text.includes("猫")) return "Cat! 喵喵喵！";
            if (text.includes("爸爸")) return "爸爸去上班赚钱买饼干！";
            if (text.includes("妈妈")) return "妈妈最漂亮！最爱你！";
            
            // 简单的数学计算 (聊天模式下也支持)
            const mathMatch = text.match(/(\d+)\s*([加\+])\s*(\d+)/);
            if (mathMatch) {
                return `这题我会！等于 ${parseInt(mathMatch[1]) + parseInt(mathMatch[3])}！`;
            }

            // 兜底回复
            const randomReplies = [
                `呱！"${text}" 是什么意思呀？`,
                "我有饼干吃吗？",
                "扑棱扑棱！真好玩！",
                "你可以叫我'讲个故事'或者'猜谜语'哦！"
            ];
            return randomReplies[Math.floor(Math.random() * randomReplies.length)];
        }

        // --- 猜谜模式 ---
        handleRiddle(text) {
            if (text.includes(this.current_answer)) {
                const reply = "答对啦！🎉 你太聪明了！呱呱呱！\n我们要不要'再来一个'？";
                this.current_answer = ""; // 清空答案，等待指令
                return reply;
            }
            if (text.includes("再来") || text.includes("继续")) return this.nextRiddle();
            if (text.includes("不知道") || text.includes("放弃")) {
                const reply = `答案是... ${this.current_answer}！笨笨皮皮！`;
                this.current_answer = "";
                return reply + "\n 说 '再来一个' 继续玩！";
            }
            if (!this.current_answer) return this.nextRiddle(); // 如果没在猜，就开始新的
            return "不对哦~ 再猜猜？提示：它是一种动物/昆虫。";
        }

        nextRiddle() {
            const r = this.riddles[Math.floor(Math.random() * this.riddles.length)];
            this.current_answer = r.a;
            return "听好啦：\n" + r.q;
        }

        // --- 算数模式 ---
        handleMath(text) {
            // 尝试找数字
            const num = text.match(/\d+/);
            if (text.includes("再来") || text.includes("题")) return this.nextMath();
            
            if (num) {
                if (parseInt(num[0]) == this.current_answer) {
                    return "💯 答对啦！数学天才！\n 说 '再来一题' 继续！";
                } else {
                    return `不对哦，不是 ${num[0]}。再算算？`;
                }
            }
            if (text.includes("不知道")) return `答案是 ${this.current_answer}！要好好学习哦！`;
            return "是多少呢？快告诉我数字！";
        }

        nextMath() {
            const a = Math.floor(Math.random() * 10) + 1;
            const b = Math.floor(Math.random() * 10) + 1;
            this.current_answer = a + b;
            return `请听题：${a} 加 ${b} 等于几？`;
        }

        // --- 角色扮演 ---
        handleRoleplay(text) {
            return `(奥特曼光线) Biu Biu! 我收到了你的信号："${text}"！怪兽被打跑了！`;
        }
    }

    // --- 语音与交互逻辑 ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    let recognition;
    const brain = new SuperBrain();
    
    const micBtn = document.getElementById('micBtn');
    const responseBox = document.getElementById('responseBox');
    const parrotDiv = document.getElementById('parrotContainer');
    const statusText = document.getElementById('statusText');
    const modeBadge = document.getElementById('modeBadge');

    function updateBadge(text) {
        if (text) {
            modeBadge.innerText = text;
            modeBadge.style.display = 'block';
        } else {
            modeBadge.style.display = 'none';
        }
    }

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            micBtn.classList.add('listening');
            statusText.innerText = "👂 在听...";
        };
        recognition.onend = () => {
            micBtn.classList.remove('listening');
            statusText.innerText = "按住说话 / 松开结束";
        };
        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            handleInput(text);
        };
    } else {
        responseBox.innerHTML = "<span>不支持语音 😭</span><span class='sub-text'>请使用 Chrome 浏览器</span>";
    }

    // 按住说话逻辑 (更符合手机习惯)
    function startListen() {
        if (!recognition) return;
        synth.cancel(); // 停止鹦鹉说话
        try { recognition.start(); } catch(e) {}
    }
    function stopListen() {
        if (!recognition) return;
        setTimeout(() => { recognition.stop(); }, 500); // 延迟一点，防止话被截断
    }

    function handleInput(text) {
        responseBox.innerHTML = `<span style="color:#eee">你说: ${text}</span>`;
        
        // AI 思考
        setTimeout(() => {
            const reply = brain.process(text);
            
            // 显示回复
            responseBox.innerHTML = `<span>${reply.replace(/\n/g, '<br>')}</span>`;
            
            // 语音播报
            speak(reply);
        }, 300);
    }

    function speak(text) {
        parrotDiv.classList.add('talking');
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.pitch = brain.mode === 'roleplay' ? 0.8 : 1.6; // 奥特曼声音低沉，鹦鹉声音尖
        u.rate = 1.2;
        u.onend = () => { parrotDiv.classList.remove('talking'); };
        synth.speak(u);
    }
</script>
</body>
</html>
"""

components.html(html_code, height=700)
