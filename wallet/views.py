from rest_framework import generics, permissions, response, status

from . import serializers
from .models import Wallet


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

            if serializer.data['currency_id'] == int(request.data['currency_id']):
                print('Here oooo')
                data.amount += amount
                data.save()
                return self.get(request, kwargs['pk'])
            return response.Response(serializer.data)
        print(request.data)



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
