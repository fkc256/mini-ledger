from datetime import date, datetime

'''
def to_date_str
날짜와 기간선택에 사용되는데,
문자열이 입력되지않고 숫자만 입력가능하게 하는 함수
'''

def to_date_str(d) -> str:
    #Streamlit date_input 결과(date/datetime)를 'YYYY-MM-DD' 문자열로 통일.
    '''
    지금 기능에 사용되지않는 불필요한 코드
    날짜와 시간이 모두 입력될때 필요한 기능.
    if isinstance(d, datetime):
        return d.date().isoformat()
    '''
    if isinstance(d, date):
        return d.isoformat()
    # 문자열이 들어오는 경우도 방어
    return str(d)[:10]


'''
def normalize_text
새 거래를 입력할때 카테고리와 내용에 공란이 발생하지 않게하며,
앞뒤 공백도 제거하는 함수
'''
def normalize_text(s: str) -> str:

    if s is None:
        return ""
    return str(s).strip()



