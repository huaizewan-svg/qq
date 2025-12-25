import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. 配置区域
# ==========================================
MY_API_KEY = "AIzaSyB2BjC7ueRjbWW3Uk_Sym47rTroEUra4gk"

# 粘贴你的 System Instructions (Prompt)
SYSTEM_PROMPT = """
在此处粘贴你在 AI Studio 里那个好用的 Prompt。
"""

APP_TITLE = "我的 AI 助手"

# ==========================================
# 2. 界面美化 (让它看起来像独立软件)
# ==========================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 注入 CSS 隐藏 Streamlit 的原生特征
st.markdown("""
<style>
    /* 隐藏顶部的红线、汉堡菜单、页脚 */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 调整整体背景，模拟 AI Studio 的清爽感 */
    .stApp {
        background-color: #ffffff;
    }
    
    /* 聊天气泡样式优化 */
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* 让输入框更像聊天软件 */
    .stChatInput input {
        border-radius: 20px !important;
        border: 1px solid #ddd !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心逻辑
# ==========================================
st.title(APP_TITLE)

if "messages" not in st.session_state:
    st.session_state.messages = []
    # 默认开场白
    st.session_state.messages.append({"role": "model", "content": "你好！我是你的专属 AI 助手。"})

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 配置 Gemini
try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025', system_instruction=SYSTEM_PROMPT)
except Exception as e:
    st.error(f"API配置错误: {e}")

# 处理输入
if prompt := st.chat_input("输入你的问题..."):
    # 显示用户输入
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 回复
    try:
        # 整理历史记录
        gemini_history = []
        for msg in st.session_state.messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=gemini_history)
        
        with st.chat_message("model"):
            with st.spinner("Thinking..."):
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"网络连接中断，请刷新重试。错误: {e}")
