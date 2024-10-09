# HuggingQwen-Assistant

HuggingQwen-Assistant是一个基于Streamlit开发的交互式聊天应用，集成了Hugging Face的大型语言模型。它允许用户与AI进行对话，并可以根据不同场景选择或自定义系统提示。

## 功能特点

- 使用Hugging Face的大型语言模型进行对话
- 支持多种预设系统提示，如翻译助手、代码解释器、创意写作等
- 允许用户自定义和管理系统提示
- 可调整模型参数，如temperature、max tokens和top p
- 实时流式输出AI响应
- 支持对话历史查看和清除
- 错误重试机制，提高稳定性

## 安装说明

1. 克隆仓库到本地：

   ```
   git clone https://github.com/nicekate/HuggingQwen-Assistant.git
   cd HuggingQwen-Assistant
   ```

2. 安装依赖：

   ```
   pip install -r requirements.txt
   ```

3. 获取Hugging Face API密钥：
   - 访问 [https://huggingface.co/settings/tokens/new?globalPermissions=inference.serverless.write&tokenType=fineGrained](https://huggingface.co/settings/tokens/new?globalPermissions=inference.serverless.write&tokenType=fineGrained) 创建新的API token。
   - 确保选择了 `inference.serverless.write` 权限。

4. 复制`.env.example`文件并重命名为`.env`，然后在其中填入你的Hugging Face API密钥：

   ```
   HUGGINGFACE_API_KEY=你的api密钥
   ```

## 使用方法

1. 运行应用：

   ```
   streamlit run app.py
   ```

2. 在浏览器中打开显示的本地地址（通常是 http://localhost:8501）

3. 在侧边栏选择或自定义系统提示，调整模型参数

4. 在聊天输入框中输入你的问题或指令，与AI助手进行对话

5. 使用"清除对话"按钮可以重置当前对话

## 自定义提示词

- 你可以在应用的侧边栏中添加、选择或删除自定义的系统提示
- 自定义提示词会保存在`custom_prompts.json`文件中

## 注意事项

- 请确保你有足够的Hugging Face API使用额度
- 大型语言模型可能会产生不准确或不适当的内容，请谨慎使用

## 许可证

[MIT License](LICENSE)