def calc_summary(transactions): 
    #  전체 거래 내역 분석 수입, 지출, 잔액의 총합을 계산
    #- transactions : 가계부 데이터 리스트
    """
    calc_summary(transactions) -> (income, expense, balance)
    - income: type == "수입" 합
    - expense: type == "지출" 합
    - balance: income - expense
    """
    income = 0 # 수입 총합 저장 변수
    expense = 0# 지출 총합 저장 변수

    for t in transactions: #변수 t에 전체 내역을 하나씩 꺼내 반복
        ttype = t.get("type") #데이터 타입을 t.get으로 가져옴
        amt = int(t.get("amount", 0))#금액부분을 정수로 형 변환
        #데이터가 없을 시 0으로 처리함

        if ttype == "수입": #ttype이 수입인 경우
            income += amt #수입 금액에 더함
        elif ttype == "지출":#ttype이 지출인 경우
            expense += amt#지출 금액에 더함

    return income, expense, income - expense 
    #총 지출,총 수입, 잔액을 반환 


def calc_category_expense(transactions):
    #지출 내역 중 카테고리의 합을 계산하는 함수

    """
    지출(type=="지출")만 대상으로 카테고리별 합계 dict 반환
    예) {"식비": 22000, "교통": 4500}
    """
    result = {} # 빈 딕셔너리  생성
    for t in transactions: #전체 내역을 순환
        if t.get("type") != "지출": #수입 데이터를 제외하는 필터링
            continue 
        cat = t.get("category", "기타") or "기타" #카테고리가 데이터가 없을 경우 "기타"로 처리
      
        amt = int(t.get("amount", 0)) #지출 금액을 정수로 변환 
        
        result[cat] = result.get(cat, 0) + amt #딕셔너리에 해당 카테고리가 있으면 기존 값에 더함 없으면 0에 더함

    return result
"""
[작동 원리]
위 사용된 코드는 입력>분류>계산>출력 순으로 나열된 코드입니다 

calc_summary 함수는 나의 재무상태를 나타내주며 if문을 사용하여 두 가지 type에 맞게
지출과, 수입을 계산 해줍니다 
마지막 retrun부분에서는 수입 - 지출을 계산하여 남은 잔액을 보여주는 게 
이 함수의 역할입니다

calc_category_expense 함수는 나의 소비를 보여주며 카테고리가 붙은 
상자에 금액을 쌓는 역할을 하는게 이 함수의 역할입니다
"""

"""
[발표멘트]
calc_summary 함수는 사용자의 전체 자산 흐름 (수입,지출,잔액)이라는 3가지 지표로 요약. 데이터가 누락 되어도 시스템이 멈추는 일 없도록 
amt = int(t.get("amount", 0)) 구문으로 예외처리를 적용했습니다

calc_category_expense 함수는 단순 합계가 아닌 내가 돈을 어디에 가장 많이 쓰고 있는지를 분석해줍니다. 딕셔너리 구조를 사용하여 별도의 수정 없이 대응이 가능한 확장성과  cat = t.get("category", "기타") or "기타" 구문을 이용하여 비어있는 카테고리 또는 빈 문자열인 경우를 잡아내는것이 특징입니다
"""
