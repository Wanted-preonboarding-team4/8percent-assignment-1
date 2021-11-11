import json, unittest, jwt
from django.test import TestCase, Client

from account.models import Account
from users.models import User


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
