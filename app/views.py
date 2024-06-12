from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from . serializers import SignUpSerializer,SignInSerializer,AuthorSerializer,HomeSerializer,AgendaSerializer,ConferenseSectionSerializer,DirectionSerializer,SponsorSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
import random
from datetime import timedelta,datetime
from . models import User,Paper,Home,Agenda,ConferenseSection,Sponsor,Direction
from rest_framework import generics

from django.shortcuts import render, redirect

from rest_framework.serializers import ValidationError


class SignUpAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')
        confirm_password = serializer.validated_data.get('confirm_password')
        # birth_date = serializer.validated_data.get('birth_date')
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        email = serializer.validated_data.get('email')
        affiliation =  serializer.validated_data.get('affiliation')

        gender = serializer.validated_data.get('gender')
        if User.objects.filter(phone=phone, status='approved').exists():
            raise ValidationError(
                detail={"error": "Bunday foydalanuvchi ro'yxatdan o'tgan"},
                code=400
            )
        
        user = User.objects.filter(phone=phone)
        if user.exists():
            user = user.first()
        else:
            user = User.objects.create(phone=phone, first_name=first_name,last_name=last_name, gender = gender,password=password,confirm_password=confirm_password,email=email,affiliation=affiliation)
        user.set_password(password)
        # user.set_password(confirm_password)
        code = random.randrange(1000, 9999)      
        user.code = code
        user.expire_date = datetime.now() + timedelta(seconds=60)
        user.save()

        print(code)
        return Response(
            data={
                "user": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "password": user.password,
                "confirm_password": user.confirm_password,
                "gender": user.gender,
                "affiliation": user.affiliation,


            },
            status=201
            )

class SignInAPIView(APIView):
    
    
    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data)

        email= request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is None or user.status != "approved":
            raise ValidationError(detail={
                "error":"Siz ro'yxatdan o'tmagansiz"},
                code = 400
                )


        token, created = Token.objects.get_or_create(user=user)
        return Response(
            data={
                'token': token.key,
                'user': user.id
            }
        )
    


from rest_framework import viewsets
from .models import Author, Paper
from .serializers import AuthorSerializer, PaperSerializer

class AuthorCreateAPIView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class PaperCreateAPIView(generics.CreateAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

class HomeListAPIView(ListAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

class AgendaListAPIView(ListAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

class ConferenseSectionListAPIView(ListAPIView):
    queryset = ConferenseSection.objects.all()
    serializer_class = ConferenseSectionSerializer


class SponsorListAPIView(ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


class DirectionListAPIView(ListAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer