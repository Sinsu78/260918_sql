class BookManager:
    """도서 목록 및 장르 관련 조회를 담당하는 클래스"""
    def __init__(self, supabase):
        self.supabase = supabase

    def get_all_books(self):
        """1. 전체 책 리스트 조회"""
        try:
            response = (
                self.supabase
                .schema("library")
                .table("books")
                .select("*")
                .order("title")
                .execute()
            )
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_books_by_genre(self, genre: str):
        """2. 장르별 도서 조회"""
        try:
            response = (
                self.supabase
                .schema("library")
                .table("books")
                .select("*")
                .eq("genre", genre)
                .order("title")
                .execute()
            )
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}