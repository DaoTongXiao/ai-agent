from collections.abc import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from schemas.chat import ChatRequest, ChatResponse, StreamChunk
from services.chat_service import chat_service

router = APIRouter(tags=["chat"])


@router.post(
    "/chat/",
    response_model=None,
    summary="Chat endpoint",
    description=(
        "支持流式和非流式对话，使用 LangChain ChatOpenAI。\n"
        "发送聊天消息到 AI 模型，支持流式（stream=True）和非流式（stream=False）响应。\n"
        "流式响应使用 StreamingResponse 返回 NDJSON 格式的 StreamChunk，每行一个 chunk，"
        "content 为生成的文本片段，done 表示是否完成。\n"
        "非流式响应直接返回 ChatResponse，content 为完整回复。\n"
        "依赖 chat_service 的 chat_stream 和 chat_once 方法。"
    ),
)
async def chat_endpoint(request: ChatRequest) -> ChatResponse | StreamingResponse:
    """
    处理聊天请求端点。

    :param request: ChatRequest，包含 messages（消息列表）、system_prompt（系统提示词）和 stream（是否启用流式输出）。
    :return: StreamingResponse (stream=True) 或 ChatResponse (stream=False)。
    """
    # 转换消息格式
    messages = [message.model_dump() for message in request.messages]

    if request.stream:

        async def generate() -> AsyncGenerator[str]:
            async for chunk in chat_service.chat_stream(messages, request.system_prompt or ""):
                yield StreamChunk(content=chunk, done=False).model_dump_json() + "\n"
            yield StreamChunk(content="", done=True).model_dump_json() + "\n"

        return StreamingResponse(generate(), media_type="application/x-ndjson")
    else:
        content = await chat_service.chat_once(messages, request.system_prompt or "")
        return ChatResponse(content=content, role="assistant")
