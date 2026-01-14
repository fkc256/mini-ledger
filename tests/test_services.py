import unittest # 코드 정상 작동 확인을 위한 도구
from ledger.services import calc_summary, calc_category_expense #테스트할 함수 부분 호출 


class TestServices(unittest.TestCase):# 수입,지출 잔고 계산을 잘 반영하는지 확인 
    def test_calc_summary(self): 
        transactions = [
            {"type": "수입", "amount": 10000},
            {"type": "지출", "amount": 3000},
            {"type": "지출", "amount": 2000},
        ]
        income, expense, balance = calc_summary(transactions)
        self.assertEqual(income, 10000)#실험값 수입 10000과 예상 값 10000 비교
        self.assertEqual(expense, 5000)#실험값 지출 3000+2000과 예상값 5000비교
        self.assertEqual(balance, 5000)#실험값 10000-3000+2000과 예상값 잔고 5000비교

    ##보완1 데이터가 아예 없을 때 0을 반환하는지 테스트
    def test_calc_summary_empty(self):

        transactions = []
        income, expense, balance = calc_summary(transactions)
        self.assertEqual(income, 0)
        self.assertEqual(expense, 0)
        self.assertEqual(balance, 0)

    ##보완2 amount가 숫자가 아닌 문자열일 때의 방어 로직 확인
    def test_calc_summary_invalidamount(self):
        transactions = [{"type": "수입", "amount": "10000"}]
        income, _ , _ = calc_summary(transactions) #calc_summary에는 income,expense,income-expense가 튜플로 있는데 이것중 income만 쓰겠다는것
        self.assertEqual(income, 10000) # 문자열 "10000"도 숫자로 잘 처리되는지 확인


    def test_calc_category_expense(self): # 수입을 제외하고 지출 금액만 항목별로 합해서 계산하고 있는지 확인
        transactions = [
            {"type": "지출", "category": "식비", "amount": 8000},
            {"type": "지출", "category": "식비", "amount": 2000},
            {"type": "수입", "category": "급여", "amount": 1000000},
            {"type": "지출", "category": "교통", "amount": 1500},
        ]
        
        result = calc_category_expense(transactions)
        self.assertEqual(result["식비"], 10000)#실험값 8000+2000이 식비 지출 합계 예상값 10000과 일치 확인
        self.assertEqual(result["교통"], 1500) #실험값 1500이 교통 지출 합계 예상값 1500과 일치 확인
        self.assertTrue("급여" not in result)  #실험값 수입인 급여가 예상대로 제외가 되었는지 확인

    ##보완1 """금액이 0원인 항목이 있어도 잘 작동하는지 테스트"""
    def test_calc_category_expense_with_zero(self):

        transactions = [
            {"type": "지출", "category": "식비", "amount": 0},
            {"type": "지출", "category": "교통", "amount": 2000}
        ]
        result = calc_category_expense(transactions)
        self.assertEqual(result["식비"], 0)    #실험값 식비 0일 때 식비 지출 예상값 0과 일치 확인
        self.assertEqual(result["교통"], 2000) #실험값 교통 2000일 때 교통 지출 예상값 2000과 일치 확인

if __name__ == "__main__":
    unittest.main()

