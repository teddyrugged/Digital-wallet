from django.core.mail import EmailMessage
from django.conf import settings
import requests
from rest_framework import response, status


class Utils:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'], body=data['body'], to=[data['receiver']]
        )
        email.send()

    @staticmethod
    def make_request(url):
        try:
            r = requests.get(url)
            return r
        except ConnectionError:
            return response.Response({'message': 'Website is not Available'}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return response.Response({'message': "Connection Error. -> Invalid URL"}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def fine(obj):
        from pprint import pprint
        pprint(obj)
