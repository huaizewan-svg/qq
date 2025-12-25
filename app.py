import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide", page_title="App加载中...")

# 调试模式：检查文件到底在不在
if not os.path.exists("index.html"):
    st.error("❌ 错误：找不到 index.html 文件！")
    st.info("请去 GitHub 确认：\n1. 文件名是不是全小写 index.html？\n2. 它是和 app.py 在同一个仓库根目录下吗？")
    # 列出当前所有文件帮你找找
    st.code(f"当前目录下的文件有: {os.listdir('.')}")
else:
    # 文件存在，开始读取
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_code = f.read()
        # 渲染
        components.html(html_code, height=1000, scrolling=True)
    except Exception as e:
        st.error(f"❌ 读取文件出错: {e}")
