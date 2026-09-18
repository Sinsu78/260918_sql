def run(supabase):
    # 로그인/회원가입 메뉴
    while True:
        print("\n===== 로그인 / 회원가입 =====")
        print("1. 로그인")
        print("2. 회원가입")
        print("0. 이전 메뉴로")

        choice = input("선택: ")

        if choice == "1":
            login(supabase)

        elif choice == "2":
            signup(supabase)

        elif choice == "0":
            break

        else:
            print("잘못된 입력입니다.")


def login(supabase):
    # 로그인
    login_id = input("아이디: ")
    password = input("비밀번호: ")

    response = (
        supabase
        .schema("library")
        .table("members")
        .select("member_id, login_id, member_name")
        .eq("login_id", login_id)
        .eq("password", password)
        .execute()
    )

    if response.data:
        member = response.data[0]
        print(f"\n{member['member_name']}님, 로그인되었습니다.")
        return member["member_id"]

    print("아이디 또는 비밀번호가 올바르지 않습니다.")


def signup(supabase):
    # 회원가입
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


if __name__ == "__main__":
    from db.supabase_client import get_client

    client = get_client()
    run(client)