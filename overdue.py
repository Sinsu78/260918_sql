
import pandas as pd
from datetime import datetime


def run(supabase):
    """
    손상 도서 관리 메뉴
    """
    while True:
        print("\n===== 손상 도서 관리 =====")
        print("1. 손상도서확인")
        print("2. 손상도서입력")
        print("0. 메뉴로 돌아가기")

        choice = input("선택: ")

        if choice == "1":
            show_overdue(supabase)

        elif choice == "2":
            insert_overdue(supabase)

        elif choice == "0":
            print("메인 메뉴로 돌아갑니다.")
            break

        else:
            print("잘못된 입력입니다.")


def show_overdue(supabase):
    """
    overdue 테이블의 손상 도서 정보를
    DataFrame 형태로 출력
    """
    response = (
        supabase
        .schema("library")
        .table("overdue")
        .select("*")
        .execute()
    )

    if not response.data:
        print("\n등록된 손상 도서가 없습니다.")
        return

    # Supabase 조회 결과를 DataFrame으로 변환
    df = pd.DataFrame(response.data)

    print("\n===== 손상 도서 목록 =====")
    print(df.to_string(index=False))


def insert_overdue(supabase):
    """
    손상 도서 정보를 overdue 테이블에 INSERT
    """

    print("\n===== 손상 도서 입력 =====")

    # ---------------------------------
    # 1. 도서번호 입력
    # ---------------------------------

    try:
        book_id = int(input("손상된 도서번호: "))
    except ValueError:
        print("도서번호는 숫자로 입력해주세요.")
        return

    # ---------------------------------
    # 2. 도서 존재 여부 확인
    # ---------------------------------

    book_response = (
        supabase
        .schema("library")
        .table("books")
        .select("book_id, title, author")
        .eq("book_id", book_id)
        .execute()
    )

    if not book_response.data:
        print("존재하지 않는 도서입니다.")
        return

    book = book_response.data[0]

    print(f"\n도서명 : {book['title']}")
    print(f"저자 : {book['author']}")

    # ---------------------------------
    # 3. 손상 사유 입력
    # ---------------------------------

    overdue_reason = input("손상 사유: ")

    if not overdue_reason.strip():
        print("손상 사유를 입력해주세요.")
        return

    # ---------------------------------
    # 4. 조치 선택
    # ---------------------------------

    print("\n조치를 선택해주세요.")
    print("1. 폐기")
    print("2. 해결")

    action_choice = input("선택: ")

    if action_choice == "1":
        action = "폐기"

    elif action_choice == "2":
        action = "해결"

    else:
        print("잘못된 입력입니다.")
        return

    # ---------------------------------
    # 5. 조치 상세 내용
    # ---------------------------------

    action_detail = input("조치 상세 내용: ")

    # ---------------------------------
    # 6. 현재 시간
    # ---------------------------------

    now = datetime.now().isoformat()

    # ---------------------------------
    # 7. overdue 테이블 INSERT
    # ---------------------------------

    response = (
        supabase
        .schema("library")
        .table("overdue")
        .insert({
            "book_id": book_id,
            "overdue_date": now,
            "overdue_reason": overdue_reason,
            "action": action,
            "action_detail": action_detail,
            "action_date": now
        })
        .execute()
    )

    # ---------------------------------
    # 8. 결과 출력
    # ---------------------------------

    if response.data:
        print("\n손상 도서 정보가 입력되었습니다.")
        print(f"도서명 : {book['title']}")
        print(f"손상 사유 : {overdue_reason}")
        print(f"조치 : {action}")

    else:
        print("\n손상 도서 입력에 실패했습니다.")


# 직접 실행할 때만 사용
if __name__ == "__main__":
    from db.supabase_client import get_client

    client = get_client()
    run(client)