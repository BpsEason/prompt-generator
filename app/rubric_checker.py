# app/rubric_checker.py - Rubric 驗收標準檢查 (P3)
from typing import Dict, Any
import json
import logging
from .utils.llm_connector import call_llm_api
from .config import settings

logger = logging.getLogger(__name__)

class RubricChecker:
    def __init__(self):
        self.rubric_prompt_template = """
        [SYSTEM: 嚴格的行銷品質評審]
        你的任務是根據以下 Rubric 驗收標準，評估提供的『原始 Prompt』和『生成內容』。
        請忽略語氣和創意，專注於 **邏輯與指令遵循度**。
        請以 **單一 JSON 格式** 輸出結果，不要添加任何解釋或額外文字。

        [RUBRIC 驗收標準]
        1. score_target_audience (0-5分): 生成內容的語氣、詞彙是否符合 Prompt 指定的客群？
        2. score_brand_style (0-5分): 是否遵循 Prompt 指定的風格模組？
        3. score_cta_clarity (0-5分): 行動呼籲是否清晰、有說服力，並且出現在文案結尾？
        4. score_feasibility (0-5分): 內容是否能直接用於廣告/社群，無明顯語法錯誤？

        [INPUT DATA]
        --- 原始 Prompt ---
        {full_prompt}
        --- 生成內容 ---
        {generated_content}
        """

    async def check(self, full_prompt: str, generated_content: str) -> Dict[str, Any]:
        """執行 Rubric 評分任務 (已異步化)"""
        
        checker_prompt = self.rubric_prompt_template.format(
            full_prompt=full_prompt,
            generated_content=generated_content
        )
        
        # 異步呼叫 LLM 進行評分
        mock_score = await call_llm_api(
            checker_prompt, 
            model=settings.RUBRIC_CHECKER_MODEL, 
            task="rubric_check"
        )
        
        try:
            # 捕獲 JSON 解析錯誤
            result = json.loads(mock_score)
            
            # 計算總分並判斷 PASS/FAIL
            total_score = result.get('score_target_audience', 0) +                           result.get('score_brand_style', 0) +                           result.get('score_cta_clarity', 0) +                           result.get('score_feasibility', 0) 
            
            result['total_score'] = total_score
            result['overall_pass'] = total_score >= 12
            
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Rubric 檢查器輸出非 JSON 格式: {e}")
            return {"error": "Rubric 檢查器輸出非標準 JSON。", "raw_output": mock_score, "overall_pass": False}
        except Exception as e:
            logger.error(f"Rubric 檢查發生未預期錯誤: {e}")
            return {"error": f"未預期錯誤: {e}", "overall_pass": False}
