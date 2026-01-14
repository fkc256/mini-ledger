import streamlit as st # 웹 화면을 만드는 도구
import pandas as pd # 표를 만들기 위한 도구
import altair as alt # 그래프를 그리기 위한 도구

from ledger.repository import load_transactions, save_transactions
# 저장된 가계부를 불러오기 / 가계부 저장하기 함수 (저장관련함수)
from ledger.services import calc_summary, calc_category_expense
# 총 수입, 지출, 잔액 계산 / 카테고리별 지출 계산 (계산로직)
from ledger.utils import to_date_str, normalize_text
# 문자열 / 날짜 정리

st.set_page_config(page_title="나만의 미니 가계부", layout="wide")

st.title("🧾 나만의 미니 가계부 (지출 관리 서비스)")

# 1) 데이터 로드 -> ledger.csv 파일을 읽음 / 거래 목록을 리스트로 가져옴
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
    else: # 거래를 딕셔너리로 만듦
        new_tx = {
            "date": to_date_str(date_value),
            "type": ttype,
            "category": category_n,
            "description": desc_n,
            "amount": int(amount),
        }
        transactions.append(new_tx) # 거래 목록에 추가
        save_transactions(transactions) # CSV 파일로 저장

        st.sidebar.success(
            f"✅ 등록 완료: {new_tx['date']} / {new_tx['type']} / {new_tx['category']} / {new_tx['description']} / {new_tx['amount']:,}원"
        )
        st.rerun() #app.py 를 다시 실행 / load_transcations() 재호출

st.sidebar.divider()
st.sidebar.header("🔎 필터(선택)")

# 간단한 기간 필터(도전 D1) - 값이 하나면 Streamlit 버전에 따라 단일 날짜로 나올 수 있어 방어
date_range = st.sidebar.date_input("기간 선택", value=None)

"""
 st.date_input() 는 기본적으로 단일날짜선택 
 from datetime import date, timedelta
 today = date.today()
 date_range = st.sidebar.date_input(
    "기간 선택",
    value=(today - timedelta(days=7), today)
 )
 """


keyword = st.sidebar.text_input("검색어(내용 포함)", placeholder="예: 점심").strip()
keyword = keyword if keyword else ""

type_filter = st.sidebar.selectbox("구분 필터", ["전체", "지출", "수입"]) # 드롭다운 메뉴를 생성
category_filter = st.sidebar.text_input("카테고리 필터(비우면 전체)", "").strip() # 특정 카테고리 이름으로 거래 데이터를 검색

# 3) 필터 적용
filtered = transactions[:]

# 기간 필터
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range[0], date_range[1]
    start_s, end_s = to_date_str(start_date), to_date_str(end_date)
    filtered = [t for t in filtered if start_s <= t["date"] <= end_s]

# 검색 필터
if keyword:
    kw = keyword.lower()
    filtered = [t for t in filtered if kw in str(t.get("description", "")).lower()]

# 구분 필터
if type_filter != "전체":
    filtered = [t for t in filtered if t.get("type") == type_filter]

# 카테고리 필터
if category_filter:
    cf = category_filter.lower()
    filtered = [t for t in filtered if cf == str(t.get("category", "")).lower()]

# 4) 요약 통계(F3) - 필터된 기준으로 계산
income, expense, balance = calc_summary(filtered)

c1, c2, c3 = st.columns(3)
c1.metric("💰 총 수입", f"{income:,} 원")
c2.metric("💸 총 지출", f"{expense:,} 원")
c3.metric("🏦 현재 잔액", f"{balance:,} 원")

st.divider()

# 5) 거래 목록 조회(F2)
st.subheader(f"📌 거래 내역 (총 {len(filtered)}건)")
if not filtered:
    st.info("등록된 거래가 없습니다.")
else:
    df = pd.DataFrame(filtered)
    # 보기 좋은 컬럼 순서 고정
    df = df[["date", "type", "category", "description", "amount"]]
    df.columns = ["날짜", "구분", "카테고리", "내용", "금액"]
    st.dataframe(df, use_container_width=True)

st.divider()

# 6) 카테고리별 지출 통계 (지출만)
st.subheader("📊 카테고리별 지출 통계 (지출만)")

cat_map = calc_category_expense(filtered)

if not cat_map:
    st.info("표시할 지출 데이터가 없습니다.")
else:
    cat_df = (
        pd.DataFrame(
            [{"카테고리": k, "지출합계": v} for k, v in cat_map.items()]
        )
        .sort_values("지출합계", ascending=False)
    )

    chart = (
        alt.Chart(cat_df)
        .mark_bar()
        .encode(
            x=alt.X("카테고리:N", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("지출합계:Q"),
            tooltip=["카테고리", "지출합계"],
        )
    )

    st.altair_chart(chart, use_container_width=True)
    st.dataframe(cat_df, use_container_width=True)
