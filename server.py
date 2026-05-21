import os
import time
import uuid
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from notebooklm import NotebookLMClient

app = FastAPI(title="NotebookLM OpenAI Compatible API")

# --- OpenAI API 模型定义 ---

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False
    # 可以根据需要添加更多参数，如 max_tokens 等

# --- NotebookLM 客户端初始化 ---
# 从环境变量中获取 notebook_id
NOTEBOOK_ID = os.environ.get("notebook_id")

async def get_notebooklm_response(prompt: str) -> str:
    """
    调用 notebooklm-py 库获取结果的包装函数。
    """
    if not NOTEBOOK_ID:
        raise Exception("Environment variable 'notebook_id' is not set.")
        
    try:
        async with await NotebookLMClient.from_storage() as client:
            result = await client.chat.ask(NOTEBOOK_ID, prompt)
            return result.answer
    except Exception as e:
        raise Exception(f"NotebookLM 调用失败: {str(e)}")

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="Messages array cannot be empty")
        
    # 获取最后一条用户消息
    # 如果 NotebookLM 支持多轮对话，可以将所有 messages 格式化为它支持的格式
    last_message = req.messages[-1].content
    
    try:
        # 获取 NotebookLM 结果
        notebooklm_result = await get_notebooklm_response(last_message)
        
        # 如果请求了 stream 模式，目前出于简单起见，我们仍返回普通结构（或者可以抛出不支持的错误）
        # 完整的流式实现需要依赖 notebooklm-py 是否支持流式生成以及使用 StreamingResponse 返回 SSE
        if req.stream:
            raise HTTPException(status_code=400, detail="Stream mode is not implemented yet")

        # 组装为 OpenAI Compatible 的响应格式
        response_data = {
            "id": f"chatcmpl-{uuid.uuid4().hex}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": req.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": notebooklm_result
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,           
                "total_tokens": 0
            }
        }
        return JSONResponse(content=response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # 运行服务器: python server.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
