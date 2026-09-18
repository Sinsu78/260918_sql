from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(url, key)
print("Supabase Client 생성 완료")

email = input("이메일: ").strip()
password = input("비밀번호: ").strip()

try:
    login = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })

    member_id = login.user.id

    print("로그인 성공")
    print("현재 member_id:", member_id)

except Exception as e:
    print("로그인 실패:", e)
    raise SystemExit

def run(supabase): # 책 목록 메뉴 진입점  # id값 필요해요!
    while True:
        print('')
        print("1. 회의실 조회/예약")
        print("0. 이전 메뉴로")
        choice = input("선택: ")
        if choice == "1":
            select_room(supabase) # id값 필요해요!
        elif choice == "0":
            break
        else:
            print("잘못된 입력입니다.")
def reservate_room(supabase, member_id): # 회의실 조회/예약
    response = supabase.schema("library").table("rooms").select("*, room_booking(*)").execute()
    rooms_data = response.data
    while True:
        print("")
        try:
            room_id = int(input("예약할 방 번호: "))
            target_room = next((r for r in rooms_data if r["room_id"] == room_id), None)
            if not target_room:
                print(f"오류! {room_id}호 방이 존재하지 않습니다.")
                continue
            room_max = target_room.get("room_max", 0)
            member_number = int(input(f"이용 인원수 (최대 {room_max}명): "))
            if member_number <= 0:
                print("오류! 이용 인원은 최소 1명 이상이어야 합니다.")
                continue
            if member_number > room_max:
                print(f"오류! 해당 방의 최대 수용 인원({room_max}명)을 초과했습니다.")
                continue
            start_time = input("시작 시간 (형식: 00:00): ")
            end_time = input("종료 시간 (형식: 00:00): ")
            time_format = "%H:%M"
            new_start = datetime.strptime(start_time, time_format)
            new_end = datetime.strptime(end_time, time_format)
            if new_start >= new_end:
                print("오류! 종료 시간은 시작 시간보다 나중이어야 합니다.")
                continue
            existing_bookings = target_room.get("room_booking", [])
            conflict = False  # 시간 중복 여부 플래그
            for b in existing_bookings:
                start = b.get("start_time")
                end = b.get("end_time")
                if start and end:
                    ex_start = datetime.strptime(start[:5], time_format)
                    ex_end = datetime.strptime(end[:5], time_format)
                    if new_start < ex_end and new_end > ex_start: # 시간 중복 조건 체크
                        print(f"이미 예약된 시간대입니다. (기존 예약: {start[:5]} ~ {end[:5]})")
                        conflict = True
                        break
            if conflict: continue
            supabase.schema("library").table("room_booking").insert({
                "room_id": room_id,
                "member_id": member_id,
                "member_number": member_number,
                "start_time": start_time,
                "end_time": end_time,
                "booking_status": True
            }).execute()
            print(f"{member_number}명 {room_id}호 {start_time}부터 {end_time}까지 예약이 성공적으로 완료되었습니다!")
            break
        except Exception as e:
            print("오류! 잘못 입력하셨습니다.", e)
def check_room(supabase): # 회의실 조회
    response = supabase.schema("library").table("rooms").select("*, room_booking(*)").execute()
    rooms_data = response.data
    for room in rooms_data:
        bookings = room.get("room_booking", [])
        is_booked = len(bookings) > 0
        status_text = "예약 있음" if is_booked else "예약 없음"
        print(f"[방 번호: {room['room_id']}호] (최대 {room['room_max']}명) | 예약 상태: {status_text}")
        if is_booked:
            for b in bookings:
                start = b.get("start_time")
                end = b.get("end_time", "")
                time_info = f"{start} ~ {end}" if end else f"{start}"
                print(f"예약 시간: {time_info}")
        else:
            print("예약이 없습니다.")
def select_room(supabase): # id값 필요해요!
    while True:
        member_id = 2
        print('')
        print("1. 회의실 조회 / 2. 회의실 예약 / 0. 이전 메뉴로")
        r_select = input("선택: ")
        if r_select == "1":
            check_room(supabase)
        elif r_select == "2":
            reservate_room(supabase, member_id)
        elif r_select == "0":
            break
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    run(supabase) # id값 필요해요!