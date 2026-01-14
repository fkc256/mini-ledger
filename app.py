import streamlit as st #웹 화면을 만드는 도구
import pandas as pd # 표를 만들기 위한 도구
import altair as alt # 그래프를 그리기 위한 도구

from ledger.repository import load_transactions, save_transactions
# 저장된 가계부를 불러오기/ 가계부 저장하기 함수(저장관련함수)
from ledger.services import calc_summary, calc_category_expense
# 총 수입, 지출, 잔액 계산/ 카테고리별 지출 계산 (계산 로직)
from ledger.utils import to_date_str, normalize_text
# 문자열/ 날짜 정리 

st.set_page_config(page_title="나만의 미니 가계부", layout="wide")

st.title("🧾 나만의 미니 가계부 (지출 관리 서비스)")

# 1) 데이터 로드 > ledger.csv 파일을 읽음 / 거래 목록을 리스트로 가져옴
transactions = load_transactions()

# 2) 사이드바 - 입력 폼 (F1) 
st.sidebar.header("➕ 새 거래 등록")

date_value = st.sidebar.date_input("날짜")
ttype = st.sidebar.selectbox("구분", ["지출", "수입"])
category = st.sidebar.text_input("카테고리", placeholder="예: 식비, 교통, 급여")
description = st.sidebar.text_input("내용", placeholder="예: 점심(김밥)")
amount = st.sidebar.number_input("금액(원)", min_value=0, step=1000)

if st.sidebar.button("등록"):
    category_n = normalize_text(category)
    desc_n = normalize_text(description)

    if not category_n:
        st.sidebar.error("카테고리는 비어 있을 수 없습니다.")
    elif not desc_n:
        st.sidebar.error("내용은 비어 있을 수 없습니다.")
    else: #거래를 딕셔너리로 만듬 

        new_tx = {
            "date": to_date_str(date_value),
            "type": ttype,
            "category": category_n,
            "description": desc_n,
            "amount": int(amount),
        }
        transactions.append(new_tx) # 거래 목록에 추가 
        save_transactions(transactions) #CSV 파일로 저장 
        st.sidebar.success(
            f"✅ 등록 완료: {new_tx['date']} / {new_tx['type']} / {new_tx['category']} / {new_tx['description']} / {new_tx['amount']:,}원"
        )
       

st.sidebar.divider()
st.sidebar.header("🔎 필터(선택)")

# 간단한 기간 필터(도전 D1) - 값이 하나면 Streamlit 버전에 따라 단일 날짜로 나올 수 있어 방어
date_range = st.sidebar.date_input(
    "기간 선택",
    value=[]
)

# 사이드 바 '내용' 검색을 위한 텍스트 입력창 생성 (양 끝 공백 제거)
keyword = st.sidebar.text_input("검색어(내용 포함)",
placeholder="예: 점심").strip()
#검색어가 입력되지 않았을 경우 빈 문자열로 초기화
keyword = keyword if keyword else ""


type_filter = st.sidebar.selectbox("구분 필터", ["전체", "지출", "수입"]) #거래 유형(전체,지출,수입)을 선택할 수 있는 드롭다운 메뉴를 생성
category_filter = st.sidebar.text_input("카테고리 필터(비우면 전체)", "").strip() # 특정 카테고리 이름으로 거래 데이터를 검색

# 3) [필터 적용] 원본 거래 데이터(transactions)을 복사, 필터링용 리스트 생성
filtered = transactions[:]

# [기간 필터] 시작일과 종료일이 포함된 date_range 값이 유요한지 확인
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range[0], date_range[1]
    #시작일과 종료일 할당 
    start_s, end_s = to_date_str(start_date), to_date_str(end_date)#날짜 객체를 리스트 컴프리헨션을 사용하여 범위 내 데이터만 추출
    filtered = [t for t in filtered if start_s <= t["date"] <= end_s]

# [검색 필터] 사용자가 입력한 검색어가 포함된 거래 내역만 추출
if keyword:
    kw = keyword.lower() #대소문자 구분 없이 검색하기 위해 소문자로 변환
    filtered = [t for t in filtered if kw in str(t.get("description", "")).lower()]

# [구분 필터] '전체'가 아닌경우 '지출'또는'수입'에 맞는 데이터만 추출
if type_filter != "전체":
    filtered = [t for t in filtered if t.get("type") == type_filter]

# [카테고리] 필터 카테고리 입력값이 있는경우 정확히 일치하는 카테고리만 추출
if category_filter:
    cf = category_filter.lower()
    filtered = [t for t in filtered if cf == str(t.get("category", "")).lower()]

# 4) 요약 통계(F3) - 필터된 기준으로 계산
income, expense, balance = calc_summary(filtered)

c1, c2, c3 = st.columns(3) #화면을 3개의 컬럼으로 나누어 배치
#첫 번째 열(컬럼)에 총 수입 표시 (1000 단위의 쉼표 포함)
c1.metric("💰 총 수입", f"{income:,} 원")
#두 번째 열엔 총지출 표시
c2.metric("💸 총 지출", f"{expense:,} 원")
#세 번재 열엔 잔액 표시
c3.metric("🏦 현재 잔액", f"{balance:,} 원")

st.divider()#시각적 구분을 위한 수평선

# 5) 거래 목록 조회(F2) 필터링 된 거래 건수 표시
st.subheader(f"📌 거래 내역 (총 {len(filtered)}건)")
if not filtered: #필터링된 결과가 없을 경우 안내메세지
    st.info("등록된 거래가 없습니다.")
else:
    #필터링된 리스트를 데이터프레임으로 전환
    df = pd.DataFrame(filtered)
    # 보기 좋은 컬럼 순서 고정
    df = df[["date", "type", "category", "description", "amount"]]
    #열(컬럼) 제목을 한글로 변경
    df.columns = ["날짜", "구분", "카테고리", "내용", "금액"]
    #화면 너비 맞추기 
    st.dataframe(df, use_container_width=True)

st.divider() 

# 6) 카테고리별 지출 통계 (지출만)
st.subheader("📊 카테고리별 지출 통계 (지출만)")

#필터링된 데이터에서 카테고리별 지출 합계를 계산하여 맵(딕셔너리) 생성
cat_map = calc_category_expense(filtered)

#지출 데이터가 없을 경우 안내메세지
if not cat_map:
    st.info("표시할 지출 데이터가 없습니다.")
else:
    #딕셔너리 데이터를 데이터 프레임으로 변환 지출 많은 순으로 정렬
    cat_df = (
        pd.DataFrame(
            [{"카테고리": k, "지출합계": v} for k, v in cat_map.items()]
        )
        .sort_values("지출합계", ascending=False)
    )
    #Altair 라이브러리 사용 막대 그래프 정의
    chart = (
    alt.Chart(cat_df)
    .mark_bar() # 막대 그래프 형태를 사용
    .encode(
        x=alt.X(
            "카테고리:N", #X축: 카테고리
            sort="-y",#Y축 지출 합계 값에 따라 내림차순
            axis=alt.Axis(labelAngle=0)#Xㅜㄱ 레이블 각도를 0도로 설정함
        ),
        y=alt.Y(
            "지출합계:Q",#Y축: 지출합계 수량데이터
            title="지출 합계",#축의 제목 설정
            axis=alt.Axis(titleAngle=0) #축의 제목 각도 설정
        ),
        tooltip=["카테고리", "지출합계"],#마우스 오버 시 정보를 보여주는 툴팁 추가
    )
)

    #생성된 차트를 화면에 표시
    st.altair_chart(chart, use_container_width=True)
    
    #차트 아래 상세 수치 데이터프레임 추가 표시
    st.dataframe(cat_df, use_container_width=True)
