from datetime import date
from db.supabase_client import get_client


def library_stats():

    supabase = get_client()

    current_month = date.today().replace(day=1)

    # 독서왕 데이터 가져오기
    result = (
        supabase
        .schema("library")
        .table("stats")
        .select("member_id, borrow_count, ranking")
        .eq("stat_month", str(current_month))
        .lte("ranking", 3)
        .order("ranking")
        .execute()
    )

    # 회원 정보 가져오기
    members = (
        supabase
        .schema("library")
        .table("members")
        .select("member_id, member_name")
        .execute()
    )

    member_dict = {
        member["member_id"]: member["member_name"]
        for member in members.data
    }

    # 회원 이름 붙이기
    for member in result.data:
        member["member_name"] = member_dict.get(member["member_id"], "알 수 없음")

    return result.data


def show_library_stats():

    top3 = library_stats()

    print()
    print("==============================")
    print("       📚 이달의 독서왕 📚")
    print("==============================")

    medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }

    for member in top3:
        ranking = member["ranking"]
        member_name = member["member_name"]
        borrow_count = member["borrow_count"]

        print(f"{medals[ranking]} {ranking}위  {member_name} - {borrow_count}권")

    print("==============================")


show_library_stats()