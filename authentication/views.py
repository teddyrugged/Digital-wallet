from rest_framework import generics, status
from rest_framework.response import Response

from authentication.serializers import RegisterSerializer


# Create your views here.
class RegisterApiView(generics.GenericAPIView):
    # Prevents authentication on this page
    authentication_classes = []

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'message': 'Success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
