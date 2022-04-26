import json

from django.conf import settings
import requests
from rest_framework import generics, permissions, response, status

from . import serializers
from .models import Wallet, Currency
from authentication.utils import Utils


class FundWalletApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.FundWalletSerializers
    queryset = Wallet.objects.all()

    def get(self, request, pk):
        obj = Wallet.objects.get(pk=pk)
        serializer = serializers.FundWalletSerializers(obj)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.data['amount']
            data = Wallet.objects.get(pk=kwargs['pk'])
            currency_id = data.currency_id_id

            if serializer.data['currency_id'] == currency_id:
                data.amount += amount
                data.save()
                return self.get(request, kwargs['pk'])
            else:
                _from = Currency.objects.get(pk=serializer.data['currency_id']).symbol
                _to = Currency.objects.get(pk=currency_id).symbol
                url = f'{settings.DATA_URL}latest?access_key={settings.DATA_API}'

                try:
                    # Makes request to the api to get rates
                    r = Utils.make_request(url)
                    if r.status_code != 200:
                        return r
                    results = json.loads(r.content)

                    wallet_currency = results['rates'][_to]
                    from_currency = results['rates'][_from]

                    # round converted amount to two decimal places
                    amount = round((amount * wallet_currency) / from_currency, 2)

                    # update wallet amount
                    data.amount += amount
                    data.save()
                    return self.get(request, kwargs['pk'])

                except Exception as er:
                    return response.Response({'error': er}, status=status.HTTP_400_BAD_REQUEST)


class WalletApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WalletSerializers
    queryset = Wallet.objects.all()

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()

    def get(self, request):
        return response.Response(request.COOKIES)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.context['username_id'] = request.user
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Wallet Created', 'details': serializer.data}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
