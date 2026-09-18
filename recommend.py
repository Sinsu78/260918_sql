import requests
from config import SUPABASE_URL, HEADERS

class recommend:
    def get_recommended_books_by_loans(self, member_id: int, limit: int = 5) -> dict:
            """4. 대출 이력 기반 추천도서 조회"""
            loans_url = f"{self.base_url}/loans?member_id=eq.{member_id}&select=book_id,books(genre)"
            loans_res = requests.get(loans_url, headers=self.headers)
            
            if loans_res.status_code != 200:
                return {"success": False, "error": loans_res.text}
            
            loans_data = loans_res.json()
            
            if not loans_data:
                fallback_url = f"{self.base_url}/books?select=*&order=created_at.desc&limit={limit}"
                fallback_res = requests.get(fallback_url, headers=self.headers)
                return {
                    "success": True,
                    "favorite_genre": None,
                    "message": "대출 이력이 없어 최신 등록 도서를 추천합니다.",
                    "data": fallback_res.json()
                }
            
            genre_counts = {}
            borrowed_book_ids = set()
            
            for item in loans_data:
                borrowed_book_ids.add(item.get("book_id"))
                book_info = item.get("books")
                if book_info and book_info.get("genre"):
                    genre = book_info.get("genre")
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
                    
            top_genre = max(genre_counts, key=genre_counts.get) if genre_counts else None
            
            if top_genre:
                books_url = f"{self.base_url}/books?genre=eq.{top_genre}&select=*&order=created_at.desc"
                books_res = requests.get(books_url, headers=self.headers)
                
                if books_res.status_code == 200:
                    all_genre_books = books_res.json()
                    recommended_books = [
                        b for b in all_genre_books if b["book_id"] not in borrowed_book_ids
                    ][:limit]
                    
                    return {
                        "success": True,
                        "favorite_genre": top_genre,
                        "message": f"선호 장르인 [{top_genre}]의 안 읽으신 추천 도서입니다.",
                        "data": recommended_books
                    }

            fallback_url = f"{self.base_url}/books?select=*&order=created_at.desc&limit={limit}"
            fallback_res = requests.get(fallback_url, headers=self.headers)
            return {
                "success": True,
                "favorite_genre": None,
                "message": "최신 등록 도서를 추천합니다.",
                "data": fallback_res.json()
            }