from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import reverse
from rest_framework import generics, status
from rest_framework.response import Response

from authentication.serializers import RegisterSerializer
from .utils import Utils


# Create your views here.
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
