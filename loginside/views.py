from django.shortcuts import render
import requests
import base64
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from users.models import User
# Create your views here.
def signup(request):
    return render(request,'signupReal.html')

def login(request):
    return render(request,'loginReal.html')

def signedup(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        image=None
        if 'image' in request.FILES:           
            image=request.FILES['image']
            print(image)
        
            
        payload={
            "name":name,
            'email':email,
            "phone":phone,
            "password":password,
            "image":image            
        }

        resp=requests.post('http://localhost:8000/api/register',payload).json()
        print("after api call")
        print(resp)
        context=None
        if resp is not None:
            context=resp
        return render(request,'home.html',context)
    
def loggedin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        payload={
            'email':email,
            "password":password,           
        }
        resp=requests.post('http://localhost:8000/api/login',payload).json()
        
        key=resp['jwt']
        try:
            print("gddh")
            payloadd=jwt.decode(key,'secret',algorithms=['HS256'])
            
        except:
            raise AuthenticationFailed('Unauthenticated')
        print(payloadd)
        user = User.objects.filter(id=payloadd['id']).first()
        dict={'name':user.name,'email':user.email,'phone':user.phone,'image':user.image}
        return render(request,'home.html',dict)
        