import streamlit as st
import streamlit.components.v1 as components

# 设置页面为宽屏模式，标题随意
st.set_page_config(layout="wide", page_title="我的 AI 应用")

# 读取刚才那个 HTML 文件
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
        
    # 渲染 HTML
    # height=1000 可以根据你的网页长短自己改
    components.html(html_code, height=1000, scrolling=True)

except FileNotFoundError:
    st.error("找不到 index.html 文件，请检查 GitHub 仓库里是否有这个文件！")
