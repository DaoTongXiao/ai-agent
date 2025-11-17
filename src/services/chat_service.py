from collections.abc import AsyncGenerator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config.settings import openai_settings


class ChatService:
    """基于 LangChain 的对话服务"""

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=openai_settings.api_key,
            base_url=str(openai_settings.base_url),
            model=openai_settings.model,
            temperature=openai_settings.temperature,
            max_tokens=openai_settings.max_tokens,
            top_p=openai_settings.top_p,
            frequency_penalty=openai_settings.frequency_penalty,
            presence_penalty=openai_settings.presence_penalty,
            timeout=openai_settings.timeout,
            max_retries=openai_settings.max_retries,
            streaming=True,  # 启用流式输出
        )

    async def chat_stream(self, messages: list[dict], system_prompt: str | None = None) -> AsyncGenerator[str]:
        """
        流式对话接口

        Args:
            messages: 消息列表，每个消息包含 role 和 content
            system_prompt: 系统提示词（可选）

        Yields:
            流式的文本片段
        """
        try:
            # 构建 LangChain 消息格式
            langchain_messages = []

            # 添加系统消息
            if system_prompt:
                langchain_messages.append(SystemMessage(content=system_prompt))

            # 转换用户消息
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")

                if role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))
                elif role == "system":
                    langchain_messages.append(SystemMessage(content=content))

            # 使用流式调用
            async for chunk in self.llm.astream(langchain_messages):
                if hasattr(chunk, "content") and chunk.content:
                    yield chunk.content

        except Exception as e:
            yield f"Error: {str(e)}"

    async def chat_once(self, messages: list[dict], system_prompt: str | None = None) -> str:
        """
        非流式对话接口

        Args:
            messages: 消息列表
            system_prompt: 系统提示词（可选）

        Returns:
            完整的回复文本
        """
        try:
            # 构建 LangChain 消息格式
            langchain_messages = []

            # 添加系统消息
            if system_prompt:
                langchain_messages.append(SystemMessage(content=system_prompt))

            # 转换用户消息
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")

                if role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))
                elif role == "system":
                    langchain_messages.append(SystemMessage(content=content))

            # 调用模型
            response = await self.llm.ainvoke(langchain_messages)
            return response.content

        except Exception as e:
            return f"Error: {str(e)}"


# 全局对话服务实例
chat_service = ChatService()
