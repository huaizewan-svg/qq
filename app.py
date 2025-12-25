import streamlit as st
import google.generativeai as genai

# =========================================================
# 🔴 核心区域：这里决定了你的 App 长什么样
# =========================================================

# 1. 你的 API Key (为了朋友能用，请保留这个 key 在这里)
MY_API_KEY = "AIzaSyB2BjC7ueRjbWW3Uk_Sym47rTroEUra4gk"

# 2. 粘贴你在第一步里得到的【终极图纸】
# 把那一大段文字全部粘贴到下面三个引号中间！
SYSTEM_PROMPT = """
在此处粘贴 AI 刚刚帮你总结的那段【终极系统指令】。
例如：你是一个精通....的助手，你的回答必须....
"""

# 3. 你的 App 名字 (显示在网页标题)
APP_TITLE = "我的 AI 神器"

# 4. 创意程度 (Temperature)
# 如果你在 AI Studio 没改过，就保持 1.0。
# 如果你觉得原来的太发散，就改小点(0.5)；太死板，就改大点(1.5)。
TEMPERATURE = 1.0

# =========================================================
# 下面的代码负责把上面的“图纸”变成网页，不需要修改
# =========================================================

st.set_page_config(page_title=APP_TITLE, page_icon="✨", layout="centered")
st.title(f"✨ {APP_TITLE}")

# 隐藏右上角的菜单和页脚，让界面更像一个独立 App
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 配置 AI
try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-preview-09-2025",
        generation_config={"temperature": TEMPERATURE},
        system_instruction=SYSTEM_PROMPT
    )
except Exception as e:
    st.error(f"系统配置出错: {e}")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户输入
if prompt := st.chat_input("开始对话..."):
    # 显示用户输入
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用 AI
    try:
        # 将聊天历史转换为 Gemini 格式
        history_for_gemini = []
        for msg in st.session_state.messages[:-1]: # 不包含刚发的这一条
            role = "user" if msg["role"] == "user" else "model"
            history_for_gemini.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=history_for_gemini)
        
        with st.chat_message("model"):
            with st.spinner("对方正在思考..."):
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"连接中断，请重试。({e})")
