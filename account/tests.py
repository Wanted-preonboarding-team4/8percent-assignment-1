import json, jwt

from django.test import TestCase, Client, client

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
class PostingViewTest(TestCase):
    def setUp(self):
        user_info = User.objects.create(
            name = "강대훈",
            email="foreat13@gmail.com",
            password="temp123456"
        )

        Account.objects.create(
            name="강대훈",
            account_number="620-217259-361",
            password=8647,
            balance=0,
            user=user_info
            )

    def test_deposit_post_success(self):
        client = Client()
        body ={
        "name": "강대훈",
        "account_number" : "620-217259-361",
        "password" : "8647",
        "amount" :5000,
        "user":{
            "name": "강대훈",
            "email":"foreat13@gmail.com",
            "password":"temp123456"
        }
}
        response = client.post('/account/deposit', json.dumps(body), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_deposit_post_not_match_account(self):
        client = Client()
        body = {
        "name": "강대훈",
        "account_number" : "620-217259-362",
        "password" : "8647",
        "amount" :5000,
        "user":{
            "name": "강대훈",
            "email":"foreat13@gmail.com",
            "password":"temp123456"
        }
}
        response = client.post('/account/deposit', json.dumps(body), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_deposit_post_not_match_user(self):
        client = Client()
        body = {
        "name": "강대훈",
        "account_number" : "620-217259-361",
        "password" : "8647",
        "amount" :5000,
        "user":{
            "name": "강대훈",
            "email":"foreat16@gmail.com",
            "password":"temp123456"
        }
}
        response = client.post('/account/deposit', json.dumps(body), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_deposit_post_fail_not_match_password(self):
        client = Client()
        body = {
        "name": "강대훈",
        "account_number" : "620-217259-361",
        "password" : "8646",
        "amount" :0,
        "user":{
            "name": "강대훈",
            "email":"foreat13@gmail.com",
            "password":"temp123456"
        }
}
        response = client.post('/account/deposit', json.dumps(body), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        Account.objects.all().delete()
