# main.py
from db.supabase_client import get_client
from features import auth, catalog, loans, overdue, recommend, room_booking, stats

def main_menu():
    client = get_client()
    while True:
        print("1. 로그인/회원가입")
        print("2. 책 목록")
        print("3. 대출 현황/반납")
        print("4. 불량도서관리")
        print("5. 대출 이력 기반 추천도서")
        print("6. 회의실 조회/대여")
        print("7. 이달의 대출왕/도서왕 top3")
        choice = input("선택: ")

        if choice == "1":
            auth.run(client)
        elif choice == "2":
            catalog.run(client)
        elif choice == "3":
            loans.run(client)
        elif choice == "4":
            overdue.run(client)
        elif choice == "5":
            recommend.run(client)
        elif choice == "6":
            room_booking.run(client)
        elif choice == "7":
            stats.run(client)
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main_menu()