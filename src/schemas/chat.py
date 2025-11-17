from typing import Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """聊天消息模型"""

    role: str = Field(..., description="消息角色：user、assistant、system")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    """聊天请求模型"""

    messages: list[ChatMessage] = Field(..., description="消息列表")
    system_prompt: Optional[str] = Field(None, description="系统提示词")
    stream: bool = Field(True, description="是否启用流式输出")


class ChatResponse(BaseModel):
    """聊天响应模型（非流式）"""

    content: str = Field(..., description="回复内容")
    role: str = Field("assistant", description="回复角色")


class StreamChunk(BaseModel):
    """流式响应数据块"""

    content: str = Field(..., description="内容片段")
    done: bool = Field(False, description="是否完成")


class ErrorResponse(BaseModel):
    """错误响应模型"""

    error: str = Field(..., description="错误信息")
    code: int = Field(..., description="错误代码")