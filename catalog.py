import requests
from config import SUPABASE_URL, HEADERS

class BookManager:
    """도서 목록 및 장르 관련 조회를 담당하는 클래스"""
    def __init__(self, base_url: str = SUPABASE_URL, headers: dict = HEADERS):
        self.base_url = base_url
        self.headers = headers

    def get_all_books(self) -> dict:
        """1. 전체 책 리스트 조회"""
        url = f"{self.base_url}/books?select=*&order=title.asc"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "error": response.text}

    def get_books_by_genre(self, genre: str) -> dict:
        """2. 장르별 도서 조회"""
        url = f"{self.base_url}/books?genre=eq.{genre}&select=*&order=title.asc"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "error": response.text}