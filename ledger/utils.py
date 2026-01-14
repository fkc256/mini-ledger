from datetime import date, datetime


def to_date_str(d) -> str:
# 날짜와 기간선택에 사용됨, 문자열이 입력 되지 않고 숫자만
# 입력 가능하게 하는 함수
    if isinstance(d, date):
        return d.isoformat()
    # 문자열이 들어오는 경우도 방어
    return str(d)[:10]


def normalize_text(s: str) -> str:
    #새 거래를 입력할때 카테고리와 내용에 공란이 발생하지 않게하며,
    #앞 뒤 공백도 제거하는 함수
    if s is None:
        return ""
    return str(s).strip()
