# app/router.py - 獨立的 API 路由管理
from fastapi import APIRouter

router = APIRouter(prefix="/prompt", tags=["Prompt Generation"])
# 建議將 main.py 中的核心路由移至此處，實現模組化
