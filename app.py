import streamlit as st
import pandas as pd
import altair as alt

from ledger.repository import load_transactions, save_transactions
from ledger.services import calc_summary, calc_category_expense
from ledger.utils import to_date_str, normalize_text

st.set_page_config(page_title="나만의 미니 가계부", layout="wide")

st.title("🧾 나만의 미니 가계부 (지출 관리 서비스)")

# 1) 데이터 로드
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
    else:
        new_tx = {
            "date": to_date_str(date_value),
            "type": ttype,
            "category": category_n,
            "description": desc_n,
            "amount": int(amount),
        }
        transactions.append(new_tx)
        save_transactions(transactions)
        st.sidebar.success(
            f"✅ 등록 완료: {new_tx['date']} / {new_tx['type']} / {new_tx['category']} / {new_tx['description']} / {new_tx['amount']:,}원"
        )
        st.rerun()

st.sidebar.divider()
st.sidebar.header("🔎 필터(선택)")

# 간단한 기간 필터(도전 D1) - 값이 하나면 Streamlit 버전에 따라 단일 날짜로 나올 수 있어 방어
date_range = st.sidebar.date_input("기간 선택", value=None)

keyword = st.sidebar.text_input("검색어(내용 포함)", placeholder="예: 점심").strip()
keyword = keyword if keyword else ""

type_filter = st.sidebar.selectbox("구분 필터", ["전체", "지출", "수입"])
category_filter = st.sidebar.text_input("카테고리 필터(비우면 전체)", "").strip()

# 3) 필터 적용
filtered = transactions[:]
# [:]의 의미 : 원본 데이터(transactions)를 보존하기 위해 리스트 전체를 복사하여 
# 필터링용 새로운 리스트(filtered)를 생성함 ([:]는 전체 복사를 의미)
# 한마디로 요약하면: 원본은 건드리지 않고, 마음껏 가공할 수 있는 "연습장"을 하나 새로 만든 것이라고 이해하기

# 기간 필터
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range[0], date_range[1]
    start_s, end_s = to_date_str(start_date), to_date_str(end_date)
    filtered = [t for t in filtered if start_s <= t["date"] <= end_s]
# 코드 수정 필요 시작 날짜랑 끝나는 날짜가 있어야 하는데 시작 날짜만 클릭 됨

# 검색 필터 : 내용 (description)이라는 특정 키워드가 포함된 내역만 추출
 if keyword:
    kw = keyword.lower()
    filtered = [t for t in filtered if kw in str(t.get("description", "")).lower()]

# 각 거래 데이터의 '내용'을 가져와 소문자로 바꾼 뒤, 검색어가 포함되어 있는지 확인
# t.get("description", "")을 사용해 데이터가 없는 경우(None)에도 에러 없이 처리



# 구분 필터 : 수입 / 지출 중 사용자가 선택한 항목만 추출
if type_filter != "전체":   # 사용자가 전체를 선택한 경우에는 필터링을 건너뛰어 모든 데이터를 유지함

    filtered = [t for t in filtered if t.get("type") == type_filter]    # 데이터의 '구분(type)' 값이 사용자가 선택한 값과 정확히 일치하는 것만 필터링

# 카테고리 필터 : 사용자가 특정 카테고리를 선택했을 경우 해당 데이터만 추출
if category_filter:
    cf = category_filter.lower()
    filtered = [t for t in filtered if cf == str(t.get("category", "")).lower()]

# 4) 요약 통계(F3) - 필터된 기준으로 계산
income, expense, balance = calc_summary(filtered)

#작동 원리: services.py에 정의된 calc_summary 함수를 호출합니다.

#그냥 전체 데이터(transactions)를 쓰는 게 아니라, 
#위에서 필터링을 거친 filtered 리스트를 전달합니다. 
#덕분에 사용자가 날짜를 고르거나 검색을 하면 그에 맞는 합계가 실시간으로 바뀝니다.


c1, c2, c3 = st.columns(3)
c1.metric("💰 총 수입", f"{income:,} 원")
c2.metric("💸 총 지출", f"{expense:,} 원")
c3.metric("🏦 현재 잔액", f"{balance:,} 원")

# st.metric: Streamlit에서 제공하는 지표 전용 위젯입니다. 제목은 크게, 숫자는 강조해서 예쁘게 보여줍니다.


st.divider()

# 5) 거래 목록 조회(F2)
st.subheader(f"📌 거래 내역 (총 {len(filtered)}건)")
if not filtered:
    st.info("등록된 거래가 없습니다.")
else:
    df = pd.DataFrame(filtered) # 의미: 딕셔너리들이 담긴 리스트(filtered)를 판다스의 **DataFrame(표 객체)**으로 변환합니다.
    #이유: 판다스를 사용해야 컬럼 순서를 바꾸거나 이름을 한글로 변경하는 등의 '표 가공'이 매우 쉬워지기 때문입니다.

   
    df = df[["date", "type", "category", "description", "amount"]] # 보기 좋은 컬럼 순서 고정
    df.columns = ["날짜", "구분", "카테고리", "내용", "금액"]
    st.dataframe(df, use_container_width=True)

st.divider()

# 6) 카테고리별 지출 통계 (지출만)
st.subheader("📊 카테고리별 지출 통계 (지출만)")

cat_map = calc_category_expense(filtered) 
#의미: services.py에 정의된 함수를 사용하여, 필터링된 데이터(filtered) 내의 지출 내역을 카테고리별로 합산한다.

if not cat_map:
    st.info("표시할 지출 데이터가 없습니다.")
else:
    cat_df = (
        pd.DataFrame( #딕셔너리 형태를 그래프를 그리기 쉬운 표(DataFrame) 형태로 바꿉니다.
            [{"카테고리": k, "지출합계": v} for k, v in cat_map.items()]    # 
        )
        .sort_values("지출합계", ascending=False)   # 지출이 가장 큰 순서대로 내림차순으로 정렬한다.(그래프에서 가장 높은 막대가 맨 앞에 오게 된다.)
    )

    chart = (
        alt.Chart(cat_df)
        .mark_bar() # 막대 그래프를 그리겠다고 정의
        .encode(
            x=alt.X("카테고리:N", axis=alt.Axis(labelAngle=0)), # x축에 카테고리 이름을 둔다.
            y=alt.Y("지출합계:Q"),  # y축에 지출합계 이름을 둔다.
            tooltip=["카테고리", "지출합계"],   # 마우스를 그래프에 올렸을 때 정보 표시하기 위한 기능
        )
    )

    st.altair_chart(chart, use_container_width=True) # 차트 표시
    st.dataframe(cat_df, use_container_width=True) # 표
