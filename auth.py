def run(supabase):
    """
    로그인 / 회원가입 진입 메뉴
    """

    while True:
        print("\n===== 로그인 / 회원가입 =====")
        print("1. 로그인")
        print("2. 회원가입")
        print("0. 이전 메뉴")

        choice = input("선택: ")

        if choice == "1":
            result = login_menu(supabase)

            if result is not None:
                return result

        elif choice == "2":
            signup(supabase)

        elif choice == "0":
            return None

        else:
            print("잘못된 입력입니다.")


def login_menu(supabase):
    """
    로그인 시 회원 / 비회원 선택
    """

    while True:
        print("\n===== 로그인 =====")
        print("1. 회원")
        print("2. 비회원")
        print("0. 이전")

        choice = input("선택: ")

        if choice == "1":
            return member_login(supabase)

        elif choice == "2":
            print("\n비회원으로 입장합니다.")
            return {
                "role": "guest"
            }

        elif choice == "0":
            return None

        else:
            print("잘못된 입력입니다.")


def member_login(supabase):
    """
    회원 로그인

    1. librarian의 관리자 ID/PW 확인
    2. 관리자 계정이 아니면 members에서 일반회원 확인
    """

    login_id = input("아이디: ")
    password = input("비밀번호: ")

    # ---------------------------------
    # 1. 관리자 로그인 확인
    # ---------------------------------

    librarian_response = (
        supabase
        .schema("library")
        .table("librarian")
        .select("librarian_id, librarian_name")
        .eq("librarian_id_for_login", login_id)
        .eq("librarian_pw_for_login", password)
        .execute()
    )

    if librarian_response.data:
        librarian = librarian_response.data[0]

        print(
            f"\n{librarian['librarian_name']}님, "
            "관리자로 로그인되었습니다."
        )

        return {
            "role": "admin",
            "librarian_id": librarian["librarian_id"],
            "name": librarian["librarian_name"]
        }

    # ---------------------------------
    # 2. 일반회원 로그인 확인
    # ---------------------------------

    member_response = (
        supabase
        .schema("library")
        .table("members")
        .select("member_id, login_id, member_name")
        .eq("login_id", login_id)
        .eq("password", password)
        .execute()
    )

    if member_response.data:
        member = member_response.data[0]

        print(
            f"\n{member['member_name']}님, "
            "로그인되었습니다."
        )

        return {
            "role": "member",
            "member_id": member["member_id"],
            "login_id": member["login_id"],
            "name": member["member_name"]
        }

    # ---------------------------------
    # 3. 로그인 실패
    # ---------------------------------

    print("\n아이디 또는 비밀번호가 올바르지 않습니다.")
    return None


def signup(supabase):
    """
    일반회원 회원가입
    """

    print("\n===== 회원가입 =====")

    login_id = input("아이디: ")
    password = input("비밀번호: ")
    member_name = input("이름: ")
    email = input("이메일: ")
    phone_number = input("전화번호: ")

    # 아이디 중복 확인
    check_response = (
        supabase
        .schema("library")
        .table("members")
        .select("member_id")
        .eq("login_id", login_id)
        .execute()
    )

    if check_response.data:
        print("이미 존재하는 아이디입니다.")
        return

    # 회원가입
    response = (
        supabase
        .schema("library")
        .table("members")
        .insert({
            "login_id": login_id,
            "password": password,
            "member_name": member_name,
            "email": email,
            "phone_number": phone_number
        })
        .execute()
    )

    if response.data:
        print("회원가입이 완료되었습니다.")
    else:
        print("회원가입에 실패했습니다.")


# 직접 실행할 때만 사용
if __name__ == "__main__":
    from db.supabase_client import get_client

    client = get_client()
    run(client)