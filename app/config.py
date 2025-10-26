# app/config.py - 環境變數與應用程式配置
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # 配置文件的設定，例如 .env 檔案
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    # LLM 服務配置
    LLM_API_KEY: Optional[str] = None # 建議使用 pydantic_settings 從 .env 或環境變數載入
    LLM_BASE_URL: Optional[str] = "https://api.openai.com/v1"
    
    # 模型名稱
    GENERATION_MODEL: str = "gpt-4o-mini"
    RUBRIC_CHECKER_MODEL: str = "gpt-3.5-turbo"
    
    # 專案資訊
    PROJECT_NAME: str = "Prompt Generator API"
    PROJECT_VERSION: str = "2.0.0"

settings = Settings()
