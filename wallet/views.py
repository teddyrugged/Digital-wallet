import json

from django.forms import model_to_dict
from django.conf import settings
import requests
from rest_framework import generics, permissions, response, status

from . import serializers
from .models import Wallet, Currency
from authentication.utils import Utils
from . import my_permissions


class WithdrawWalletApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.FundWalletSerializers
    queryset = Wallet.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return response.Response({'data': serializer.data, 'user': request.user.username, 'pk': kwargs['pk']}, status=status.HTTP_201_CREATED)


class FundWalletApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.WithdrawWalletSerializers
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
            selected_currency = serializer.data['currency_id']

            if selected_currency == currency_id:
                data.amount += amount
                data.save()
                return self.get(request, kwargs['pk'])
            else:
                _from = Currency.objects.get(pk=selected_currency).symbol
                _to = Currency.objects.get(pk=currency_id).symbol
                url = f'{settings.DATA_URL}latest?access_key={settings.DATA_API}'

                try:
                    if request.user.is_noob:

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
                    else:
                        # Checks if there is an existing wallet for the user with the same currency
                        wallets = Wallet.objects.filter(username_id=request.user, currency_id_id=selected_currency)
                        print('selected', selected_currency)
                        if wallets:
                            # Update the existing wallet with the new amount
                            wallets[0].amount += amount
                            wallets[0].save()
                            return response.Response({'message': f"Your '{wallets[0].name}' has been funded with {amount}"}, status=status.HTTP_202_ACCEPTED)
                        else:
                            # Create a new wallet with the amount and currency
                            cur_instance = Currency.objects.get(pk=selected_currency)
                            Wallet.objects.create(username_id=request.user, amount=amount, currency_id=cur_instance,
                                                  name=f'{request.user.first_name} {cur_instance.name} Wallet').save()
                            return response.Response({'message': 'Wallet Successfully Created', 'wallet': cur_instance.name}, status=status.HTTP_201_CREATED)
                        return self.get(request, kwargs['pk'])

                except Exception as er:
                    return response.Response({'error': er}, status=status.HTTP_400_BAD_REQUEST)


class WalletApiView(generics.ListCreateAPIView):
    permission_classes = [my_permissions.IsElite, permissions.IsAuthenticated]
    serializer_class = serializers.WalletSerializers
    queryset = Wallet.objects.all()


    def get(self, request):
        # Get all wallets associated with the user
        user_wallet = Wallet.objects.filter(username_id=request.user)

        # Convert the models to dictionary for each wallet
        wallets = [model_to_dict(wallet) for wallet in user_wallet]
        return response.Response(wallets, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.context['username_id'] = request.user
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Wallet Created', 'details': serializer.data}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
