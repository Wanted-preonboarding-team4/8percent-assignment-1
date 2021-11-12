import json, jwt
from datetime import datetime
import bcrypt
from django.test import TestCase, Client

from users.models import User
from account.models import Account, Transaction, TransactionType
from env import SECRET_KEY, ALGORITHM


class PostTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(
                id=1,
                name="dog",
                email="dog@gmail.com",
                password="dog1234!",
            ),
            User(
                id=2,
                name="cat",
                email="cat@naver.com",
                password="cat1234!",
            )
        ])
        self.token1 = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)
        self.token2 = jwt.encode({'id': User.objects.get(id=2).id}, SECRET_KEY, ALGORITHM)

        Account.objects.bulk_create([
            Account(
                id=1,
                name="dog",
                password=1111,
                account_number=111111111,
                balance=0,
                user_id=1
            ),
            Account(
                id=2,
                name="cat",
                password=2222,
                account_number=222222222,
                balance=0,
                user_id=2
            )
        ])

    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()

    def test_account_post_success(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "dog",
            "password": "1111",
            "balance": 0
        }
        response = client.post('/account', json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "MESSAGE": "SUCCESS",
        })

    def test_account_post_not_password_rule(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "dog",
            "password": "111111",
            "balance": 0
        }
        response = client.post('/account', json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "MESSAGE": "숫자 4자리를 입력해주세요."
        })

    def test_account_post_key_error(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "dog",
            "passwordsss": "1111",
            "balance": 0
        }
        response = client.post('/account', json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "MESSAGE": "KEY_ERROR"
        })


class DepositViewTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(
                id=1,
                name="강대훈",
                email="foreat13@gmail.com",
                password="temp123456"
            ),

            User(
                id=2,
                name="대훈강",
                email="foreat12@gmail.com",
                password="rkdeognsWKd123"
            )
        ])

        Account.objects.bulk_create([
            Account(
                id=1,
                name="강대훈",
                account_number="1234567",
                password=bcrypt.hashpw("8647".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                balance=0,
                user_id=1
            ),
            Account(
                id=2,
                name="대훈강",
                account_number="12435622",
                password=bcrypt.hashpw("8646".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                balance=0,
                user_id=2
            ),
        ]
        )

        TransactionType.objects.bulk_create([
            TransactionType(
                id=1,
                type="입금"
            ),
            TransactionType(
                id=2,
                type="출금"
            )
        ])

        self.token1 = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)
        self.token2 = jwt.encode({'id': User.objects.get(id=2).id}, SECRET_KEY, ALGORITHM)

    def test_deposit_post_success(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "강대훈",
            "account_id": 1,
            "password": "8647",
            "amount": 5000,
            "user_id": 1
        }
        response = client.post('/account/deposit', json.dumps(body), content_type='application/json', **headers)
        print("현재 금액 : ",Account.objects.get(id=body['account_id']).balance)
        self.assertEqual(response.status_code, 200)

    def test_deposit_post_not_match_account(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "강대훈",
            "account_id": 2,
            "password": "8647",
            "amount": 5000,
            "user_id": 1
        }
        response = client.post('/account/deposit', json.dumps(body), content_type='application/json', **headers)
        print("현재 금액 : ", Account.objects.get(id=body['account_id']).balance)
        self.assertEqual(response.status_code, 404)

    def test_deposit_post_not_match_user_id(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "강대훈",
            "account_id": 1,
            "password": "8647",
            "amount": 5000,
            "user_id": 2
        }
        response = client.post('/account/deposit', json.dumps(body), content_type='application/json', **headers)
        print("현재 금액 : ", Account.objects.get(id=body['account_id']).balance)
        self.assertEqual(response.status_code, 404)

    def test_deposit_post_fail_not_match_password(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "강대훈",
            "account_id": 1,
            "password": "8646",
            "amount": 0,
            "user_id": 1
        }
        response = client.post('/account/deposit', json.dumps(body), content_type='application/json', **headers)
        print("현재 금액 : ", Account.objects.get(id=body['account_id']).balance)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()


class WithdrawViewTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(
                id=1,
                name="강대훈",
                email="foreat13@gmail.com",
                password="temp123456"
            ),

            User(
                id=2,
                name="대훈강",
                email="foreat12@gmail.com",
                password="rkdeognsWKd123"
            )
        ])

        Account.objects.bulk_create([
            Account(
                id=1,
                name="강대훈",
                account_number="620-217259-361",
                password=bcrypt.hashpw("8647".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                balance=100000,
                user_id=1
            ),
            Account(
                id=2,
                name="대훈강",
                account_number="620-217259-362",
                password=bcrypt.hashpw("8646".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                balance=50000,
                user_id=2
            ),
        ]
        )

        TransactionType.objects.bulk_create([
            TransactionType(
                id=1,
                type="입금"
            ),
            TransactionType(
                id=2,
                type="출금"
            )
        ])
        self.token1 = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)
        self.token2 = jwt.encode({'id': User.objects.get(id=2).id}, SECRET_KEY, ALGORITHM)

    def test_withdraw_post_success(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "강대훈",
            "account_id": 1,
            "password": "8647",
            "amount": 5000,
            "user_id": 1
        }
        response = client.post('/account/withdraw', json.dumps(body), content_type='application/json', **headers)
        print("현재 금액 : ", Account.objects.get(id=body['account_id']).balance)
        self.assertEqual(response.status_code, 200)

    def test_withdraw_post_not_match_account(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "강대훈",
            "account_id": 2,
            "password": "8647",
            "amount": 5000,
            "user_id": 1
        }
        response = client.post('/account/withdraw', json.dumps(body), content_type='application/json', **headers)
        print("현재 금액 : ", Account.objects.get(id=body['account_id']).balance)
        self.assertEqual(response.status_code, 404)

    def test_withdraw_post_not_match_user_id(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "강대훈",
            "account_id": 1,
            "password": "8647",
            "amount": 5000,
            "user_id": 2
        }
        response = client.post('/account/withdraw', json.dumps(body), content_type='application/json', **headers)
        print("현재 금액 : ", Account.objects.get(id=body['account_id']).balance)
        self.assertEqual(response.status_code, 404)


    def test_withdraw_post_lack_of_money(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token1}
        body = {
            "name": "강대훈",
            "account_id": 1,
            "password": "8646",
            "amount": 1500000,
            "user_id": 1
        }
        response = client.post('/account/withdraw', json.dumps(body), content_type='application/json', **headers)
        print("현재 금액 : ", Account.objects.get(id=body['account_id']).balance)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()

class TransactionViewTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(
                id=1,
                name="dog",
                email="dog@gmail.com",
                password="doggg12345!",
            ),
            User(
                id=2,
                name="cat",
                email="cat@naver.com",
                password="cattt12345!",
            )
        ])
        self.token1 = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)
        self.token2 = jwt.encode({'id': User.objects.get(id=2).id}, SECRET_KEY, ALGORITHM)

        Account.objects.bulk_create([
            Account(
                id=1,
                name="dog",
                password=1111,
                account_number='111111111',
                balance=50000,
                user_id=1
            ),
            Account(
                id=2,
                name="cat",
                password=2222,
                account_number='222222222',
                balance=50000,
                user_id=2
            )
        ])

        TransactionType.objects.bulk_create([
            TransactionType(
                id=1,
                type="입금"
            ),
            TransactionType(
                id=2,
                type="출금"
            )
        ])

        Transaction.objects.bulk_create([
            Transaction(
                id=1,
                amount=1000,
                transaction_counterparty = '111111111',
                created_at = datetime.now(),
                description = '첫번째',
                balance = 49000,
                user_id = 1,
                account_id = 1,
                transaction_type_id = 2
            ),
            Transaction(
                id=2,
                amount=1000,
                transaction_counterparty = '111111111',
                created_at = datetime.now(),
                description = '두번째',
                balance = 48000,
                user_id = 1,
                account_id = 1,
                transaction_type_id = 2
            ),
            Transaction(
                id=3,
                amount=1000,
                transaction_counterparty = '111111111',
                created_at = datetime.now(),
                description = '세번째',
                balance = 47000,
                user_id = 1,
                account_id = 1,
                transaction_type_id = 2
            )
        ])
    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()
        TransactionType.objects.all().delete()
        Transaction.objects.all().delete()
    
    def test_transaction_list_get_success(self):
        client = Client()
        headers = {"HTTP_Authorization" : self.token1}
        # token   = header["Authorization"] 
        # payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        # user    = User.objects.get(id = payload['id'])

        response = client.get(
            '/account/transactions/1?startPeriod=2021-11-12&endPeriod=2021-11-14&transaction_type=all',
        **headers)
        
        written1 = Transaction.objects.get(id=1).created_at.strftime(r"%Y.%m.%d %H:%M:%S")
        written2 = Transaction.objects.get(id=2).created_at.strftime(r"%Y.%m.%d %H:%M:%S")
        written3 = Transaction.objects.get(id=3).created_at.strftime(r"%Y.%m.%d %H:%M:%S")

        test = {
                "Result": [
            {
                "transaction_date": written1,
                "amount": 1000,
                "balance": 49000,
                "transaction_type": "출금",
                "description": '첫번째',
                "transaction_counterparty": "11111****"
            },
            {
                "transaction_date": written2,
                "amount": 1000,
                "balance": 48000,
                "transaction_type": "출금",
                "description": '두번째',
                "transaction_counterparty": "11111****"
            },
            {
                "transaction_date": written3,
                "amount": 1000,
                "balance": 47000,
                "transaction_type": "출금",
                "description": '세번째',
                "transaction_counterparty": "11111****"
                },
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)