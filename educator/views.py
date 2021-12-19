# ------ rest framework imports -------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
# ------ For Sending E-Mail -------
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from Unacademy.settings import EMAIL_HOST_USER

from .models import Educator, OTP

from .serializers import AccountSerializer

import random
from django.utils import timezone
import datetime

@api_view(['POST'])
def send_otp(request):
    return otp(request.data.get('email'))

# a seperate function so that it can be called from anywhere
def otp(to_email):
    # generating 4-digit OTP
    # to_email = email or request.data.get('email',)
    otp = random.randint(1000, 9999)
    if OTP.objects.filter(otp = otp).exists():
        if(otp > 9000):
            otp = random.randint(1000, otp)
        else:
            otp = random.randint(otp, 9999)
    OTP.objects.filter(otpEmail__iexact = to_email).delete()

    from_email = EMAIL_HOST_USER
    subject = 'OTP for Sign-Up'
    text_content = f'Your One Time Password for signing up on EduTech is {otp}.\nValid for only 3 minutes.\nDO NOT SHARE IT WITH ANYBODY.'
    html_content = f'<span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px;"><p style="font-size: 18px;">DO NOT SHARE IT WITH ANYBODY.</p><p>Valid for only 5 minutes.</p><p>Your One Time Password for signing up on EduTech is <strong style="font-size: 18px;">{otp}</strong>.</p></span>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    OTP.objects.create(otp = otp, otpEmail = to_email, time_created = timezone.now())
    return Response({'message': 'OTP sent successfully'}, status=status.HTTP_201_CREATED)

class AccountCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format = None):
        try:
            user_email = request.data.get('email',)
            password = request.data.get('password',)
            name = request.data.get('name',)
            # print(OTP.objects.get(otpEmail__iexact = user_email).is_verified)
            # checking if user already exists
            if Educator.objects.filter(email__iexact = user_email).exists():
                message = {'message':'User already exists. Please Log-In'}
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)

            elif OTP.objects.filter(otpEmail__iexact = user_email).exists() and OTP.objects.get(otpEmail__iexact = user_email).is_verified:
                # for validation of password (default and custom)
                # validate_password throws exception for valdation errors
                serializer = AccountSerializer(data=request.data)
                try:
                    validate_password(password)
                    if serializer.is_valid():
                        serializer.save()
                    return Response(serializer.data)
                except:
                    return Response({'message': 'Please Enter a valid password. Password should have atleast 1 Capital Letter, 1 Number and 1 Special Character in it.'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Email Not verified. Please verify first.'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Please provide the required details.'}, status=status.HTTP_204_NO_CONTENT)

class OTPView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format = None):
        data_otp = request.data.get("otp",)
        data_email = request.data.get("email",)
        current_time = timezone.now()
        # user will always be correct as front end retains it from previous step
        otp_obj = OTP.objects.get(otpEmail__iexact = data_email)
        # OTP expired
        if otp_obj.time_created + datetime.timedelta(minutes=3) < current_time:
            message = {'message':'OTP expired'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        else:
            if OTP.objects.filter(otp = data_otp).exists() and (OTP.objects.get(otp = data_otp) == OTP.objects.get(otpEmail = data_email)):
                if otp_obj.time_created + datetime.timedelta(minutes=3) > current_time:
                    # OTP verified
                    otp_obj.is_verified = True
                    otp_obj.save()
                    message = {'message':'User verified'}
                    return Response(message,status=status.HTTP_202_ACCEPTED)
                # OTP expired
                message = {'message':'OTP expired'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
            # OTP doesn't match
            else:
                message = {'message':'OTP doesn\'t match'}
                return Response(message,status=status.HTTP_401_UNAUTHORIZED)
