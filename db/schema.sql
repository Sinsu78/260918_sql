create schema library;

-- 1번 멤버
CREATE TABLE library.members (
    member_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    login_id text UNIQUE NOT NULL,
    password text NOT NULL,
    member_name text NOT NULL,
    email text UNIQUE NOT NULL,
    phone_number text UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2번 책목록
CREATE TABLE library.books (
    book_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publisher TEXT,
    pub_year VARCHAR(10),
    isbn VARCHAR(20) UNIQUE,
    genre TEXT DEFAULT '기타',
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2번 관심도서
CREATE TABLE library.wishlist (
    wish_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES library.members(member_id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES library.books(book_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(member_id, book_id)
);

-- 3번 사서
CREATE TABLE library.librarian (
    librarian_id INTEGER PRIMARY KEY,
    librarian_name TEXT NOT NULL,
    hire_date TIMESTAMP NOT NULL
);

-- 3번 대출도서
CREATE TABLE library.loans (
    loan_id BIGSERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES library.members(member_id),
    loan_time TIMESTAMP NOT NULL,
    book_id INTEGER NOT NULL REFERENCES library.books(book_id),
    librarian_id INTEGER NOT NULL REFERENCES library.librarian(librarian_id),
    left_book_num INTEGER NOT NULL CHECK (left_book_num >= 0 AND left_book_num <= 3)
);

-- 3번 반납
CREATE TABLE library.returns (
    return_id BIGSERIAL PRIMARY KEY,
    loan_id BIGINT NOT NULL REFERENCES library.loans(loan_id),
    member_id INTEGER NOT NULL REFERENCES library.members(member_id),
    book_id INTEGER NOT NULL REFERENCES library.books(book_id),
    return_time TIMESTAMP NOT NULL,
    overdue_yes TEXT NOT NULL CHECK (overdue_yes IN ('정상','불량'))
);

-- 4번 불량도서
CREATE TABLE library.overdue (
    overdue_id BIGSERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES library.books(book_id),
    overdue_date TIMESTAMP NOT NULL,
    overdue_reason TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('폐기','해결')),
    action_detail TEXT,
    action_date TIMESTAMP NOT NULL
);

-- 6번 룸
CREATE TABLE library.rooms (
    room_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    room_max integer NOT NULL,
    room_status boolean NOT NULL default true,
    memo text
);

-- 6번 회의실 예약
CREATE TABLE library.room_booking (
    reservation_id BIGSERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES library.rooms(room_id),
    member_id INTEGER NOT NULL REFERENCES library.members(member_id),
    member_number integer NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    booking_status boolean NOT NULL default true
);

-- 7번 랭킹
CREATE TABLE library.stats (
    stats_id BIGSERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES library.members(member_id),
    stat_month DATE NOT NULL,
    borrow_count INTEGER NOT NULL,
    ranking INTEGER NOT NULL,
    UNIQUE(member_id, stat_month)
);

-- 권한/보안 설정
ALTER TABLE library.members DISABLE ROW LEVEL SECURITY;
ALTER TABLE library.books DISABLE ROW LEVEL SECURITY;
ALTER TABLE library.wishlist DISABLE ROW LEVEL SECURITY;
ALTER TABLE library.librarian DISABLE ROW LEVEL SECURITY;
ALTER TABLE library.loans DISABLE ROW LEVEL SECURITY;
ALTER TABLE library.returns DISABLE ROW LEVEL SECURITY;
ALTER TABLE library.overdue DISABLE ROW LEVEL SECURITY;
ALTER TABLE library.rooms DISABLE ROW LEVEL SECURITY;
ALTER TABLE library.room_booking DISABLE ROW LEVEL SECURITY;
ALTER TABLE library.stats DISABLE ROW LEVEL SECURITY;

GRANT ALL ON ALL TABLES IN SCHEMA library TO anon, authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA library TO anon, authenticated, service_role;