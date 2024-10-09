import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import json
import time
import requests

# 加载 .env 文件
load_dotenv()

# 从 .env 文件获取 API key
api_key = os.getenv("HUGGINGFACE_API_KEY")

client = InferenceClient(api_key=api_key)

# 预设提示词文件路径
PROMPTS_FILE = "custom_prompts.json"

# 加载预设提示词
def load_prompts():
    if os.path.exists(PROMPTS_FILE):
        with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "翻译助手": "翻译助手，给你中文你翻译成英文，给你英文你翻译成中文。直接翻译，不要解释。",
        "代码解释器": "你是一个代码解释器。请解释用户提供的代码，并在需要时提供改进建议。",
        "创意写作": "你是一个创意写作助手。根据用户提供的主题或开头，继续创作故事或文章。",
        "数学导师": "你是一个数学导师。帮助用户解决数学问题，并解释解题步骤。",
        "历史学家": "你是一个历史学家。回答用户关于历史事、人物和时期的问题，提供详细和准确的信息。"
    }

# 保存预设提示词
def save_prompts(prompts):
    with open(PROMPTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)

# 初始化会话状态
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'custom_prompts' not in st.session_state:
    st.session_state.custom_prompts = load_prompts()

# 设置页面标题
st.title("AI 助手")

# 创建侧边栏用于参数调整
st.sidebar.header("参数设置")

# 模型选择
models = [
    "Qwen/Qwen2.5-72B-Instruct",
]
selected_model = st.sidebar.selectbox("选择模型", models)

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 100, 32768, 8196, 100)
top_p = st.sidebar.slider("Top P", 0.1, 1.0, 0.9, 0.1)

# 提示词选择
selected_prompt = st.sidebar.selectbox("选择系统提示", list(st.session_state.custom_prompts.keys()) + ["自定义"])
if selected_prompt == "自定义":
    system_prompt = st.sidebar.text_area("输入自定义系统提示", "")
else:
    system_prompt = st.session_state.custom_prompts[selected_prompt]

# 如果提示词改变，重置对话
if 'current_prompt' not in st.session_state or st.session_state.current_prompt != system_prompt:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.current_prompt = system_prompt

# 显示对话历史
for message in st.session_state.messages[1:]:  # 跳过系统消息
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.code(message["content"], language="markdown")
        else:
            st.write(message["content"])

# 获取用户输入
user_input = st.chat_input("请输入你的问题：")

if user_input:
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 创建助手消息占位符
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                # 发送请求到模型
                for chunk in client.chat.completions.create(
                    model=selected_model, 
                    messages=st.session_state.messages, 
                    stream=True, 
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p
                ):
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
                
                break  # 如果成功，跳出重试循环
            except (requests.exceptions.RequestException, ConnectionError) as e:
                if attempt < max_retries - 1:
                    st.warning(f"连接错误，正在重试... ({attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    st.error(f"连接失败，请稍后再试。错误信息：{str(e)}")
                    full_response = "抱歉，我现在无法回答。请稍后再试。"

        message_placeholder.markdown(full_response)
    
    # 将助手的回复添加到消息历史
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # 在对话历史下方添加一个可复制的代码块
    st.code(full_response, language="markdown")

# 添加清除对话按钮
if st.button("清除对话"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.rerun()  # 使用 st.rerun() 替代 st.experimental_rerun()

# 系统提示管理（放在左侧最下面）
st.sidebar.markdown("---")
st.sidebar.subheader("系统提示管理")
new_prompt_name = st.sidebar.text_input("新系统提示名称")
new_prompt_content = st.sidebar.text_area("新系统提示内容")
if st.sidebar.button("添加新系统提示"):
    if new_prompt_name and new_prompt_content:
        st.session_state.custom_prompts[new_prompt_name] = new_prompt_content
        save_prompts(st.session_state.custom_prompts)
        st.sidebar.success(f"已添加新系统提示：{new_prompt_name}")

# 删除系统提示
prompt_to_delete = st.sidebar.selectbox("选择要删除的系统提示", list(st.session_state.custom_prompts.keys()))
if st.sidebar.button("删除选中的系统提示"):
    if prompt_to_delete in st.session_state.custom_prompts:
        del st.session_state.custom_prompts[prompt_to_delete]
        save_prompts(st.session_state.custom_prompts)
        st.sidebar.success(f"已删除系统提示：{prompt_to_delete}")