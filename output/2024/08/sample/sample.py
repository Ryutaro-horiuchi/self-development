#DjangoでHTTPリクエストを受け取り、JSON形式で{"message": hello}というレスポンスを返すコードを作成してください
from django.http import JsonResponse

def hello_world(request):
    return JsonResponse({"message": "hello"})

from django.test import TestCase
from django.urls import reverse

class HelloWorldTests(TestCase):
    def test_hello_world(self):
        response = self.client.get(reverse('hello_world'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "hello"})
