# app/utils/llm_connector.py - LLM API 串接層 (異步化)

from typing import Dict, Any
import asyncio
import random
import json

# 假設這裡使用 OpenAI Python SDK 的非同步客戶端
# import openai
# from openai import AsyncOpenAI
# client = AsyncOpenAI(api_key=...)

async def call_llm_api(prompt: str, model: str, task: str = "generation") -> str:
    """
    統一的 LLM API 異步呼叫函數 (使用 asyncio.sleep 模擬延遲)。
    """
    
    print(f"\n--- 模擬 LLM 呼叫: Model={model}, Task={task} ---")
    
    # 模擬 API 呼叫的網路延遲，釋放 Event Loop
    await asyncio.sleep(random.uniform(0.1, 0.5)) 
    
    if task == "rubric_check":
        # 模擬 Rubric Checker 任務的 JSON 輸出
        mock_result = {
            "score_target_audience": random.randint(3, 5),
            "score_brand_style": random.randint(3, 5),
            "score_cta_clarity": random.randint(3, 5),
            "score_feasibility": random.randint(3, 5),
            "notes": f"模擬 Rubric 評分結果 (Model: {model})。請替換為真實 LLM 輸出。"
        }
        # Rubric Checker 應返回 JSON 字串
        return json.dumps(mock_result, ensure_ascii=False, indent=2)
    
    elif task == "generation":
        # 模擬行銷文案生成任務
        style = "熱血" if "熱情" in prompt else "專業"
        product = "AI 簡報工具"
        cta = "立即免費試用" if "立即免費試用" in prompt else "歡迎聯繫"
        
        return f"""
        【{style}衝刺！異步處理讓你的專案更高效！】
        剛畢業的你，是否對簡報感到焦慮？別擔心！{product} 讓你一鍵生成專業簡報，
        把時間用在最重要的事上！充分利用了 FastAPI 的異步特性，提高吞吐量！
        #異步 #生產級 #AI工具
        **🔥 趕快行動！{cta}！**
        """
    
    return f"Mock Output for prompt: {prompt[:50]}..."
