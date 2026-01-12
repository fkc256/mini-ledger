from datetime import date, datetime


def to_date_str(d) -> str:
    """Streamlit date_input 결과(date/datetime)를 'YYYY-MM-DD' 문자열로 통일."""
    if isinstance(d, datetime):
        return d.date().isoformat()
    if isinstance(d, date):
        return d.isoformat()
    # 문자열이 들어오는 경우도 방어
    return str(d)[:10]


def normalize_text(s: str) -> str:
    """앞뒤 공백 제거 + 내부적으로 None 방어."""
    if s is None:
        return ""
    return str(s).strip()
