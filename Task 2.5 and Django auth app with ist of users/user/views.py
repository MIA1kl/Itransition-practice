from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import CustomUserSerializer, UserLoginSerializer, UserActionSerializer, CustomUserListSerializer
from rest_framework.permissions import IsAuthenticated
from .authentication import CustomUserBackend
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class UserManagementView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBlockView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserActionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = self.get_object()
        user.block_user()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserUnblockView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserActionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = self.get_object()
        user.unblock_user()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserActionSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance == self.request.user:
            instance.delete_user()
        else:
            instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Use the custom authentication backend for authentication
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Update the last_login field
                user.last_login = timezone.now()
                user.save()

                # Generate and return tokens
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
