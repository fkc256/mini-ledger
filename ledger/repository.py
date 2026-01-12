import os
import csv

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "ledger.csv")
CSV_COLUMNS = ["date", "type", "category", "description", "amount"]


def load_transactions(path: str = CSV_PATH):
    """CSV가 있으면 읽고, 없으면 빈 리스트."""
    if not os.path.exists(path):
        return []

    transactions = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        # 컬럼 검증(최소한)
        if reader.fieldnames is None:
            return []

        missing = [c for c in CSV_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV 컬럼이 누락되었습니다: {missing}")

        for row in reader:
            # amount는 int로
            try:
                row["amount"] = int(row["amount"])
            except Exception:
                row["amount"] = 0
            # 필요한 키만 유지
            tx = {k: row.get(k, "") for k in CSV_COLUMNS}
            transactions.append(tx)

    return transactions


def save_transactions(transactions, path: str = CSV_PATH):
    """전체 덮어쓰기 저장."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for t in transactions:
            row = {
                "date": t.get("date", ""),
                "type": t.get("type", ""),
                "category": t.get("category", ""),
                "description": t.get("description", ""),
                "amount": int(t.get("amount", 0)),
            }
            writer.writerow(row)
