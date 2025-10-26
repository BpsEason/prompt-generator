# app/main.py - FastAPI 主程式 (生產級 V2)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import logging

from .config import settings
from .prompt_engine import PromptEngine
from .rubric_checker import RubricChecker
from .utils.llm_connector import call_llm_api

# 配置日誌記錄
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化核心服務
prompt_engine = PromptEngine(template_path="app/templates/")
rubric_checker = RubricChecker()

app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.PROJECT_VERSION
)

class PromptRequest(BaseModel):
    # 這是使用者透過前端或 API 傳入的模組參數
    prompt: Dict[str, str] = Field(
        default={
            "style": "熱血",
            "audience": "剛畢業的大學生",
            "format": "社群貼文",
            "product": "AI 簡報生成工具",
            "cta": "立即免費試用"
        },
        description="所有行銷模組化參數，會傳給 PromptEngine 拼接。"
    )

@app.post("/generate_marketing_content", response_model=Dict[str, Any])
async def generate_content_api(request: PromptRequest):
    """
    接收模組化參數，組裝 Prompt，異步生成內容，並進行 Rubric 驗收。
    """
    logger.info("接收到新的生成請求。")
    try:
        # 1. 組裝 Prompt
        full_prompt = prompt_engine.generate_full_prompt(request.prompt)
        logger.debug(f"生成的 Prompt: {full_prompt[:100]}...")
        
        # 2. 異步呼叫 GPT 模型
        generated_text = await call_llm_api(
            full_prompt, 
            model=settings.GENERATION_MODEL, 
            task="generation"
        )

        # 3. 異步執行 Rubric 驗收
        rubric_result = await rubric_checker.check(full_prompt, generated_text)
        
        if not rubric_result.get('overall_pass'):
            logger.warning("生成內容未通過 Rubric 檢查。")

        return {
            "status": "success",
            "input_config": request.prompt,
            "generated_content": generated_text,
            "rubric_score": rubric_result
        }

    except Exception as e:
        logger.error(f"處理請求時發生嚴重錯誤: {e}", exc_info=True)
        # 返回標準 HTTP 500 錯誤
        raise HTTPException(
            status_code=500, 
            detail=f"服務內部錯誤，請檢查日誌。錯誤類型: {type(e).__name__}"
        )
