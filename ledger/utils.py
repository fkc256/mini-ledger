from datetime import date, datetime


def to_date_str(d) -> str:
    """Streamlit date_input 결과(date/datetime)를 'YYYY-MM-DD' 문자열로 통일."""
    if isinstance(d, datetime):
        return d.date().isoformat() #변수 d가 datetime 타입이면,시간 정보를 버리고 날짜만 추출한 뒤,그것을 "YYYY-MM-DD" 문자열로 바꿔서 반환한다.
    if isinstance(d, date):
        return d.isoformat() #변수 d가 datetime 타입이면,날짜 값을 "YYYY-MM-DD" 문자열로 바꿔서 반환한다. 
    # 문자열이 들어오는 경우도 방어(YYYY-MM-DD가 10글자임 그래서 이렇게 짜르겠다는 얘기, 화면 멈추는 것보다 일단은 돌아가게 하기 위해 만듬)
    return str(d)[:10]


def normalize_text(s: str) -> str:
    """앞뒤 공백 제거 + 내부적으로 None 방어."""
    if s is None:
        return ""
    return str(s).strip()
