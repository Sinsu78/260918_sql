# config.py
import os
from dotenv import load_dotenv

# .env 파일 읽어오기
load_dotenv()

SUPABASE_URL = os.getenv("https://qmuqaehymfmkwcfjzoed.supabase.co")
SUPABASE_KEY = os.getenv("qmuqaehymfmkwcfjzoed")

# 환경변수 누락 시 바로 알려주기 (디버깅 편하게)
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL 또는 SUPABASE_KEY가 설정되지 않았습니다. "
        ".env 파일을 확인하세요."
    )