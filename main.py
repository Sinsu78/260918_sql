# main.py
from db.supabase_client import get_client
import auth, catalog, loans, overdue, recommend, room_booking, stats


def guest_menu(supabase):
    """비회원 메뉴: 책 목록, 회의실 조회, 이달의 랭킹만 가능"""
    while True:
        print("\n===== 비회원 메뉴 =====")
        print("1. 책 목록")
        print("2. 회의실 조회")
        print("3. 이달의 대출왕/도서왕 top3")
        print("0. 이전 메뉴로")
        choice = input("선택: ").strip()

        if choice == "1":
            catalog.run(supabase)  # 비회원용 catalog 호출
        elif choice == "2":
            room_booking.run(supabase)
        elif choice == "3":
            stats.run(supabase)
        elif choice == "0":
            break
        else:
            print("잘못된 입력입니다.")


def member_menu(supabase, user_info):
    """회원(로그인) 메뉴: 사서면 마지막에 불량도서관리 메뉴 추가"""
    is_librarian = user_info.get("role") == "admin" or user_info.get("is_librarian", False)
    user_name = user_info.get("name") or user_info.get("member_name", "")

    while True:
        print(f"\n===== 회원 메뉴 (로그인: {user_name}) =====")
        print("1. 책 목록 (관심도서 포함)")
        print("2. 대출 현황/반납")
        print("3. 대출 이력 기반 추천도서")
        print("4. 회의실 조회/대여")
        print("5. 이달의 대출왕/도서왕 top3")
        if is_librarian:
            print("6. 불량도서관리 (사서 전용)")
        print("0. 로그아웃")
        choice = input("선택: ").strip()

        if choice == "1":
            catalog.run(supabase, user_info)  # 회원 세션 전달
        elif choice == "2":
            loans.run(supabase, user_info)
        elif choice == "3":
            recommend.run(supabase, user_info)  # 회원 세션 전달
        elif choice == "4":
            room_booking.run(supabase, user_info)
        elif choice == "5":
            stats.run(supabase)
        elif choice == "6" and is_librarian:
            overdue.run(supabase)
        elif choice == "0":
            print("로그아웃 되었습니다.")
            break
        else:
            print("잘못된 입력입니다.")


def main_menu():
    supabase = get_client()

    while True:
        print("\n===== 도서관 시스템 =====")
        print("1. 회원")
        print("2. 비회원")
        print("0. 종료")
        choice = input("선택: ").strip()

        if choice == "1":
            user_info = auth.run(supabase)
            if user_info:
                member_menu(supabase, user_info)
            else:
                print("로그인에 실패했거나 취소되었습니다.")
        elif choice == "2":
            guest_menu(supabase)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")


if __name__ == "__main__":
    main_menu()