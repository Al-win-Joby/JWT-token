from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import FileUploadParser
from .serializers import UserSerializers
from .models import User
import jwt,datetime
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
class RegisterView(APIView):
    
    def post(self,request):        
        serializer=UserSerializers(data=request.data)        
        serializer.is_valid(raise_exception=True)      
        print("________________________")          
        #serializer.save()
        serializer.created(serializer.data)        
        return Response(serializer.data)            


class LoginView(APIView):
    def post(self,request):
        
        email=request.data['email']
        password=request.data['password']

        user=User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User Not Found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token=jwt.encode(payload,'secret',algorithm='HS256')

        response= Response()
        
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token,
        }
        return response


class UserViews(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer=UserSerializers(user)
        print(Response(serializer.data))
        return Response(serializer.data)
        return render('home.html', Response(serializer.data))
    
    def post(self, request):
        print("hello-----------------------------")
        user = User.objects.get(id='16')
        serializer=UserSerializers(user)
        print(Response(serializer.data))
        return Response(serializer.data)


class LogoutViews(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')
    
        if not token:
            raise AuthenticationFailed('No user')
        print("token deleted")
        resp=Response()
        resp.delete_cookie('jwt')
        
        resp.data={
            'success':"token deleted",
        }
        
        return resp