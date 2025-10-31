import os

import gradio as gr
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)

# model = init_chat_model("deepseek-r1:1.5b", model_provider="ollama")
model = ChatTongyi(model="qwen-plus-latest", api_key=os.getenv("DASHSCOPE_API_KEY"), verbose=True)
system_prompt = ChatPromptTemplate.from_messages([
    ("system", "你的身份是小智，一名乐于助人的助手"),
    ("human", "{input}")
])

qa_chain = system_prompt | model | StrOutputParser()

async def chat_response(message, history):
    partial_message = ""
    async for chunk in qa_chain.astream({"input": message}):
        partial_message += chunk
        print(chunk, end="", flush=True)
        yield partial_message

def create_chatbot():
    # 自定义CSS样式 - 居中显示
    css = """
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .header-text {
        text-align: center;
        margin-bottom: 20px;
    }
    """

    with gr.Blocks(title="DeepSeek Chat", css=css) as demo:
        with gr.Column(elem_classes=["main-container"]):
            # 居中显示标题
            gr.Markdown(
                "# 🤖 LangChain 聊天机器人 ",
                elem_classes=["header-text"]
            )
            gr.Markdown(
                "基于 LangChain LCEL 构建的流式对话机器人",
                elem_classes=["header-text"]
            )

            chatbot = gr.Chatbot(
                height=500,
                show_copy_button=True,
                avatar_images=(
                    "https://cdn.jsdelivr.net/gh/twitter/twemoji@v14.0.2/assets/72x72/1f464.png",
                    "https://cdn.jsdelivr.net/gh/twitter/twemoji@v14.0.2/assets/72x72/1f916.png"
                ),

            )

            with gr.Row():
                msg = gr.Textbox(
                    placeholder="请输入您的问题...",
                    container=False,
                    scale=7
                )
                submit = gr.Button("发送", scale=1, variant="primary")
                clear = gr.Button("清空", scale=1)

        # 处理消息发送
        async def respond(message, chat_history):
            if not message.strip():
                yield "", chat_history
                return

            # 1. 添加用户消息到历史并立即显示
            chat_history = chat_history + [(message, None)]
            yield "", chat_history  # 立即显示用户消息

            # 2. 流式生成AI回应
            async for response in chat_response(message, chat_history):
                # 更新最后一条消息的AI回应
                chat_history[-1] = (message, response)
                yield "", chat_history

        # 清空对话历史的函数
        def clear_history():
            return [], ""

        # 绑定事件
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        submit.click(respond, [msg, chatbot], [msg, chatbot])
        clear.click(clear_history, outputs=[chatbot, msg])

    return demo

# 启动界面
demo = create_chatbot()
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    debug=True
)
