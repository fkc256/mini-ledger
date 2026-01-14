def calc_summary(transactions):
    """
    calc_summary(transactions) -> (income, expense, balance)
    - income: type == "수입" 합
    - expense: type == "지출" 합
    - balance: income - expense
    """
    income = 0
    expense = 0

    for t in transactions:
        ttype = t.get("type")
        amt = int(t.get("amount", 0))

        if ttype == "수입":
            income += amt
        elif ttype == "지출":
            expense += amt

    return income, expense, income - expense


def calc_category_expense(transactions):
    """
    지출(type=="지출")만 대상으로 카테고리별 합계 dict 반환
    예) {"식비": 22000, "교통": 4500}
    """
    result = {}
    for t in transactions:
        if t.get("type") != "지출":
            continue
        cat = t.get("category", "기타") or "기타"
        amt = int(t.get("amount", 0))
        result[cat] = result.get(cat, 0) + amt
    return result
