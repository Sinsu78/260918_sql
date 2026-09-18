from datetime import datetime, timedelta


def run(supabase, user_info):
    """
    도서 대출 / 반납 메뉴
    """
    member_id = user_info["member_id"]

    while True:
        print("\n===== 도서 대출 / 반납 =====")
        print("1. 대출하기")
        print("2. 반납하기")
        print("0. 메뉴로 돌아가기")

        choice = input("선택: ")

        if choice == "1":
            borrow_book(supabase, member_id)

        elif choice == "2":
            return_book(supabase, member_id)

        elif choice == "0":
            print("메뉴로 돌아갑니다.")
            break

        else:
            print("잘못된 입력입니다.")


def get_current_loans(supabase, member_id):
    """
    현재 회원이 대출 중인 도서 조회
    """

    # 회원의 전체 대출 기록 조회
    loan_response = (
        supabase
        .schema("library")
        .table("loans")
        .select(
            "loan_id, member_id, loan_time, book_id, librarian_id"
        )
        .eq("member_id", member_id)
        .execute()
    )

    # 회원의 반납 기록 조회
    return_response = (
        supabase
        .schema("library")
        .table("returns")
        .select("loan_id")
        .eq("member_id", member_id)
        .execute()
    )

    # 이미 반납한 loan_id
    returned_loan_ids = {
        row["loan_id"]
        for row in return_response.data
    }

    # 아직 반납하지 않은 대출만 추출
    current_loans = [
        loan
        for loan in loan_response.data
        if loan["loan_id"] not in returned_loan_ids
    ]

    return current_loans


def borrow_book(supabase, member_id):
    """
    도서 대출
    최대 3권까지 대출 가능
    """

    print("\n===== 도서 대출 =====")

    # ---------------------------------
    # 1. 현재 대출 권수 확인
    # ---------------------------------

    current_loans = get_current_loans(
        supabase,
        member_id
    )

    current_count = len(current_loans)
    left_book_num = 3 - current_count

    print(
        f"현재 대출 가능한 권 수는 {left_book_num}권 입니다."
    )

    # ---------------------------------
    # 2. 최대 3권 제한
    # ---------------------------------

    if current_count >= 3:
        print("최대 3권까지 대출할 수 있습니다.")
        print("현재 대출 중인 도서를 반납해주세요.")
        return

    # ---------------------------------
    # 3. 대출할 도서번호 입력
    # ---------------------------------

    try:
        book_id = int(input("대출할 도서번호: "))
    except ValueError:
        print("도서번호는 숫자로 입력해주세요.")
        return

    # ---------------------------------
    # 4. 도서 존재 여부 확인
    # ---------------------------------

    book_response = (
        supabase
        .schema("library")
        .table("books")
        .select(
            "book_id, title, author, is_available"
        )
        .eq("book_id", book_id)
        .execute()
    )

    if not book_response.data:
        print("존재하지 않는 도서입니다.")
        return

    book = book_response.data[0]

    # ---------------------------------
    # 5. 현재 회원이 이미 대출 중인지 확인
    # ---------------------------------

    current_book_ids = {
        loan["book_id"]
        for loan in current_loans
    }

    if book_id in current_book_ids:
        print("이미 대출 중인 도서입니다.")
        return

    # ---------------------------------
    # 6. 다른 회원이 대출 중인지 확인
    # ---------------------------------

    if book["is_available"] is False:
        print("현재 대출 중인 도서입니다.")
        return

    # ---------------------------------
    # 7. 손상 도서 여부 확인
    #
    # overdue에 없음 → 대출 가능
    # action = 해결 → 대출 가능
    # action = 폐기 → 대출 불가
    # ---------------------------------

    overdue_response = (
        supabase
        .schema("library")
        .table("overdue")
        .select(
            "overdue_id, book_id, overdue_reason, action"
        )
        .eq("book_id", book_id)
        .execute()
    )

    if overdue_response.data:

        overdue = overdue_response.data[0]

        if overdue["action"] == "폐기":
            print("\n대출할 수 없는 도서입니다.")
            print("해당 도서는 폐기 처리된 도서입니다.")
            return

        elif overdue["action"] == "해결":
            print("손상 이력이 있으나 현재 해결된 도서입니다.")

    # ---------------------------------
    # 8. 처리한 사서번호 입력
    # ---------------------------------

    try:
        librarian_id = int(
            input("처리한 사서번호: ")
        )
    except ValueError:
        print("사서번호는 숫자로 입력해주세요.")
        return

    # ---------------------------------
    # 9. 사서 존재 여부 확인
    # ---------------------------------

    librarian_response = (
        supabase
        .schema("library")
        .table("librarian")
        .select(
            "librarian_id, librarian_name"
        )
        .eq("librarian_id", librarian_id)
        .execute()
    )

    if not librarian_response.data:
        print("존재하지 않는 사서번호입니다.")
        return

    # ---------------------------------
    # 10. 대출 후 남은 대출 가능 권수
    # ---------------------------------

    left_book_num = 3 - (current_count + 1)

    # ---------------------------------
    # 11. loans 테이블에 INSERT
    # ---------------------------------

    loan_response = (
        supabase
        .schema("library")
        .table("loans")
        .insert({
            "member_id": member_id,
            "loan_time": datetime.now().isoformat(),
            "book_id": book_id,
            "librarian_id": librarian_id,
            "left_book_num": left_book_num
        })
        .execute()
    )

    if not loan_response.data:
        print("대출 처리에 실패했습니다.")
        return

    # ---------------------------------
    # 12. books 대출 가능 여부 변경
    # ---------------------------------

    (
        supabase
        .schema("library")
        .table("books")
        .update({
            "is_available": False
        })
        .eq("book_id", book_id)
        .execute()
    )

    # ---------------------------------
    # 13. 대출 완료
    # ---------------------------------

    print("\n도서 대출이 완료되었습니다.")
    print(f"도서명 : {book['title']}")
    print(f"저자 : {book['author']}")
    print(f"대출 권수 : {current_count + 1}권")
    print(f"남은 대출 가능 권수 : {left_book_num}권")
    print("대출 기간 : 14일")


def return_book(supabase, member_id):
    """
    도서 반납
    """

    print("\n===== 도서 반납 =====")

    # ---------------------------------
    # 1. 반납할 도서번호 입력
    # ---------------------------------

    try:
        book_id = int(input("반납할 도서번호: "))
    except ValueError:
        print("도서번호는 숫자로 입력해주세요.")
        return

    # ---------------------------------
    # 2. 현재 대출 중인 도서 확인
    # ---------------------------------

    current_loans = get_current_loans(
        supabase,
        member_id
    )

    target_loans = [
        loan
        for loan in current_loans
        if loan["book_id"] == book_id
    ]

    if not target_loans:
        print("현재 대출 중인 도서가 아닙니다.")
        return

    loan = target_loans[0]

    # ---------------------------------
    # 3. 도서 정보 확인
    # ---------------------------------

    book_response = (
        supabase
        .schema("library")
        .table("books")
        .select(
            "book_id, title, author"
        )
        .eq("book_id", book_id)
        .execute()
    )

    if not book_response.data:
        print("도서 정보를 찾을 수 없습니다.")
        return

    book = book_response.data[0]

    # ---------------------------------
    # 4. 연체 여부 확인
    # ---------------------------------

    loan_time = datetime.fromisoformat(
        loan["loan_time"].replace("Z", "+00:00")
    )

    due_date = loan_time + timedelta(days=14)

    now = datetime.now(loan_time.tzinfo)

    if now > due_date:
        overdue_status = "연체"
    else:
        overdue_status = "정상"

    # ---------------------------------
    # 5. returns 테이블에 INSERT
    # ---------------------------------

    return_response = (
        supabase
        .schema("library")
        .table("returns")
        .insert({
            "loan_id": loan["loan_id"],
            "member_id": member_id,
            "book_id": book_id,
            "return_time": datetime.now().isoformat(),
            "overdue_yes": overdue_status
        })
        .execute()
    )

    if not return_response.data:
        print("반납 처리에 실패했습니다.")
        return

    # ---------------------------------
    # 6. books 대출 가능 여부 변경
    # ---------------------------------

    (
        supabase
        .schema("library")
        .table("books")
        .update({
            "is_available": True
        })
        .eq("book_id", book_id)
        .execute()
    )

    # ---------------------------------
    # 7. 반납 완료
    # ---------------------------------

    print("\n도서 반납이 완료되었습니다.")
    print(f"도서명 : {book['title']}")
    print(f"반납 상태 : {overdue_status}")

    if overdue_status == "연체":
        print(
            f"반납 예정일 : "
            f"{due_date.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("반납 예정일이 지나 연체되었습니다.")