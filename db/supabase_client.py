# db/supabase_client.py
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

# 싱글톤 패턴: client를 한 번만 만들고 재사용
_client: Client | None = None


def get_client() -> Client:
    """
    Supabase client를 반환한다.
    이미 생성된 게 있으면 재사용하고, 없으면 새로 만든다.
    모든 features/*.py 파일은 이 함수를 통해 client를 받아서 사용해야 한다.
    """
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# 이 파일 단독 테스트용
if __name__ == "__main__":
    client = get_client()
    print("Supabase client 연결 성공!")
    print(client)