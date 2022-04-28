import json

from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import reverse
import jwt
import requests
from rest_framework import generics, status, exceptions
from rest_framework.response import Response

from authentication.serializers import RegisterSerializer, LoginSerializer
from authentication.models import User, Currency
from .utils import Utils


class LogoutApiView(generics.GenericAPIView):
    def get(self, request):
        logout(request)
        if 'jwt' in request.COOKIES:
            del request.COOKIES['jwt']
        return Response({'message': 'Logged Out'}, status=status.HTTP_200_OK)


class LoginApiView(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        if not request.data.get('username'):
            raise exceptions.NotAcceptable('Username is missing')
        if not request.data['password']:
            raise exceptions.NotAcceptable('Password is missing')

        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                serializer = self.serializer_class(user)
                resp = Response(serializer.data, status=status.HTTP_200_OK)
                resp.set_cookie(key='jwt', value=serializer.data['token'], httponly=True)
                return resp
            return Response({'message', 'Incorrect Authentication Details'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except User.DoesNotExist:
            return Response({'message', 'Invalid User'}, status=status.HTTP_404_NOT_FOUND)


class RegisterApiView(generics.GenericAPIView):
    # Prevents authentication on this page
    authentication_classes = []

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token = serializer.data['token']

            try:
                relative_url = reverse('verify-email')
                data = {
                    'subject': 'Registration Complete',
                    'body': f"This is a verification message. Click link to verify your email http://{get_current_site(request).domain}{relative_url}?token={token}",
                    'receiver': serializer.data['email']
                }

                Utils.send_email(data)
                return Response({'message': 'Success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as err:
                return Response({'message': 'Error', 'data': str(err)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailApiView(generics.GenericAPIView):
    authentication_classes = []

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS512')
            print(payload['user'])
            user = User.objects.get(username=payload['user'])

            user.is_active = True
            user.save()

            return Response({'message': 'User Successfully Verified'}, status=status.HTTP_202_ACCEPTED)
        except jwt.ExpiredSignatureError as err:
            return Response({'error': f'Link is expired: {err}'}, status=status.HTTP_417_EXPECTATION_FAILED)
        except jwt.exceptions.DecodeError as err:
            return Response({'error': f'Invalid Token: {err}'}, status=status.HTTP_417_EXPECTATION_FAILED)


class UpdateCurrenciesApiView(generics.GenericAPIView):
    authentication_classes = []

    def get(self, request):
        try:
            url = f'{settings.DATA_URL}symbols?access_key={settings.DATA_API}'
            r = requests.get(url)
            if r.status_code == 200:
                results = json.loads(r.content)
                # To remove existing currencies
                Currency.objects.all().delete()

                for cur in results['symbols']:
                    # To save each symbol and currency inside the database
                    Currency.objects.create(name=results['symbols'][cur], symbol=cur).save()
                return Response({'message': 'Currencies Updated', 'data': results['symbols']}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid Response'}, status=status.HTTP_400_BAD_REQUEST)
        except ConnectionError:
            return Response({'message': 'Website is not Available'}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return Response({'message': "Connection Error. -> Invalid URL"}, status=status.HTTP_404_NOT_FOUND)
