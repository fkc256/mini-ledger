import os #os와 소통하기 위해 임포트
import csv #CSV 파일을 읽고 쓰기 위해 임포트 

DATA_DIR = "data" # 데이터 파일을 저장할 폴더 이름
CSV_PATH = os.path.join(DATA_DIR, "ledger.csv")#폴더명 + 파일명 전체 경로에 생성 (data/ledger.py)
CSV_COLUMNS = ["date", "type", "category", "description", "amount"] #CSV 파일에서 사용될 열의 이름(컬럼명) 정의


def load_transactions(path: str = CSV_PATH):
    """CSV가 있으면 리스트로 변환하여 읽고, 없으면 빈 리스트."""

    #지정된 경로에 파일이 존재하는지 확인, 없으면 빈 리스트 
    if not os.path.exists(path):
        return []

    transactions = [] #거래 내역을 담을 리스트 생성

    #r = 읽기 모드 , utf-8 = 인코딩으로 열기
    with open(path, "r", encoding="utf-8", newline="") as f:
        #CSV의 첫 줄을 key로 사용하는 딕셔너리 형태로 읽기 설정 
        reader = csv.DictReader(f)

        # 컬럼 검증(최소한)
        if reader.fieldnames is None:
            return []
        
        #정의된 csv_columns 중 파일에 누락된 컬럼이 있는지 확인
        missing = [c for c in CSV_COLUMNS if c not in reader.fieldnames]
        if missing:
            #필수 컬럼이 없으면 에러를 발생 프로그램에 알림
            raise ValueError(f"CSV 컬럼이 누락되었습니다: {missing}")
        #파일의 각 행을 반복하며 처리
        for row in reader:
            # amount는 int로
            try:
                #문자열로 저장된 데이터를 int로 변환
                row["amount"] = int(row["amount"])
            except Exception:
                #변환 실패 시 기본값 0으로 설정
                row["amount"] = 0
            # 필요한 키만 유지
            tx = {k: row.get(k, "") for k in CSV_COLUMNS}
            transactions.append(tx)

    return transactions #전체 거래내역 리스트 반환


def save_transactions(transactions, path: str = CSV_PATH):
    """전체 덮어쓰기 저장."""
    #데이터 저장 폴더가 없다면 자동으로 생성 
    os.makedirs(os.path.dirname(path), exist_ok=True)

    #w = 쓰기 모드, utf-8 = 인코딩 
    with open(path, "w", encoding="utf-8", newline="") as f:
        #딕셔너리 데이터를 csv 형태로 쓰기 위한 설정 
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)

        #csv 파일의 맨 첫 출에 컬럼 이름쓰기
        writer.writeheader()

        #transactions 리스트에 있는 각 거래 항목을 한 줄씩 기록 
        for t in transactions:
            row = {
                "date": t.get("date", ""), # 날짜 가져오기
                "type": t.get("type", ""), #구분(수입/지출) 가져오기
                "category": t.get("category", ""), # 카테고리 가져오기
                "description": t.get("description", ""), #내용 가져오기 
                "amount": int(t.get("amount", 0)),# 금액을 정수로 확실히 변환하여 가져오기
            }
            writer.writerow(row) # 실제 파일에 한 줄 쓰기
