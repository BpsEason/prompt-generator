# app/prompt_engine.py - Prompt 組合邏輯 (核心 P1)

from typing import Dict, Any
import yaml
import os
import logging

logger = logging.getLogger(__name__)

class PromptEngine:
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.templates = self._load_templates()
        self.main_template = self._load_main_template()
        logger.info(f"PromptEngine 初始化完成，已載入 {len(self.templates)} 個模組類型。")

    def _load_templates(self) -> Dict[str, Any]:
        """
        載入 app/templates/ 下所有 YAML 檔案作為模組庫，並增加錯誤處理。
        """
        all_templates = {}
        for filename in os.listdir(self.template_path):
            if filename.endswith(('.yaml', '.yml')):
                module_type = filename.split('.')[0]
                filepath = os.path.join(self.template_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data:
                            all_templates[module_type] = data
                except FileNotFoundError:
                    logger.error(f"錯誤: 找不到模組檔案 {filepath}")
                except yaml.YAMLError as e:
                    logger.error(f"錯誤: {filepath} 格式錯誤: {e}")
                except Exception as e:
                    logger.error(f"載入 {filepath} 發生未預期錯誤: {e}")
        return all_templates
    
    def _load_main_template(self) -> str:
        """核心 Prompt 結構，使用 f-string 佔位符"""
        return """
        [SYSTEM INSTRUCTION]
        你是一位頂尖的行銷文案專家。
        {style_fragment}
        {audience_fragment}
        {context_fragment}
        
        [CONTEXT PARAMETERS]
        - 產品/服務: {product_desc}
        - 呼籲行動 (CTA): {cta_text}
        
        [TASK INSTRUCTION]
        請根據上述所有條件和限制，為產品生成一篇 {format_type}。
        請確保內容符合品牌風格、目標受眾的語氣，並且 **CTA 必須清晰且放在結尾**。
        """

    def generate_full_prompt(self, user_config: Dict[str, str]) -> str:
        """根據傳入的參數，生成最終的 Prompt 字串"""
        # ... (邏輯不變，已驗證設計良好) ...
        fragments = {}
        context_data = {}
        
        for module_type, module_name in user_config.items():
            if module_type in self.templates and module_name in self.templates[module_type]:
                module_config = self.templates[module_type][module_name]
                
                if module_type in ['style', 'audience', 'context']:
                    fragments[f"{module_type}_fragment"] = module_config.get("prompt_fragment", "")
                
                if module_type == 'product':
                    context_data["product_desc"] = module_config.get("description", module_name)
                elif module_type == 'cta':
                    context_data["cta_text"] = module_config.get("description", module_name)
                elif module_type == 'format':
                    context_data['format_type'] = module_name
        
        template_params = {
            "style_fragment": fragments.get("style_fragment", "[風格: 未指定]"),
            "audience_fragment": fragments.get("audience_fragment", "[受眾: 未指定]"),
            "context_fragment": fragments.get("context_fragment", "[情境: 未指定]"),
            "product_desc": context_data.get("product_desc", "[未指定產品]"),
            "cta_text": context_data.get("cta_text", "[未指定 CTA]"),
            "format_type": context_data.get("format_type", "短文案")
        }

        full_prompt = self.main_template.format(**template_params)
        return full_prompt
