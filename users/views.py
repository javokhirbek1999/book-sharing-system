import jwt
from django.http import request
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status, generics, views
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UserSerializer, LoginSerializer
from .models import User
from .utils import Util


class RegisterView(generics.GenericAPIView):

    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('users:email_verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = f"Hello {user.name}!\nPlease use the link below to activate your account \n {absurl}"
        data = {'email_body':email_body, 'to_email':user.email, 'email_subject':'Verify your account'}

        Util.send_mail(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):

    serializer_class = UserSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="Enter verification token", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):

        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'status':'Email is successfully activated'},status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError:
            return Response({'status':'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'status':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
            
    