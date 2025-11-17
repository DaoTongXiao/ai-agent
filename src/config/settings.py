from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class OpenAIModelSettings(BaseSettings):
    """
    OpenAI 风格的大模型接口配置类
    """

    # API 基础设置
    api_key: str = Field(default="", description="API 密钥")
    base_url: str = Field(default="https://api.openai.com/v1", description="API 基础 URL")

    # 模型设置
    model: str = Field(default="gpt-3.5-turbo", description="默认使用的模型名称")
    max_tokens: Optional[int] = Field(default=None, ge=1, le=4096, description="最大生成 token 数")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="温度参数，控制随机性")
    top_p: Optional[float] = Field(default=1.0, ge=0.0, le=1.0, description="核采样参数")
    frequency_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0, description="频率惩罚")
    presence_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0, description="存在惩罚")

    # 请求设置
    timeout: Optional[float] = Field(default=60.0, gt=0, description="请求超时时间（秒）")
    max_retries: Optional[int] = Field(default=3, ge=0, le=10, description="最大重试次数")

    # 环境变量配置
    class Config:
        env_prefix = "OPENAI_"
        env_file = ".env"


# 全局配置实例
OpenAIModelSettings.model_rebuild()
openai_settings = OpenAIModelSettings()
