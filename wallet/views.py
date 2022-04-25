from rest_framework import generics, permissions, response, status

from . import serializers
from .models import Wallet


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

