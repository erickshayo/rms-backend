from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializer import UserSerializer
from django.contrib.auth import authenticate, login, logout
from .token import get_user_token
from .models import User, Profile
from app1.models import Wilaya, Kata, Mtaa, Citizen
from mtaa import tanzania
# Create your views here.

@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def RegisterUser(request):
    if request.method == "POST":
        data = request.data
        username = data['username']
        # user = None
        user = User.objects.filter(username=username)
        if user:
            message = {'message': 'user does exist'}
            return Response(message)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            message = {'save': True}
            return Response(message)
        else:
            message = {'save': False}
            return Response(message)
    return Response({'message': "hey bro"})


# {
#     "first_name":"mike",
#     "last_name":"cyril",
#     "username":"mike",
#     "email":"mike@gmail.com",
#     "password":"123",
#     "type":"wilaya"
# }

@api_view(["POST"])
@permission_classes([AllowAny])
def LoginView(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        user_id = User.objects.values('id', 'type', 'username', 'email', 'is_staff', 'citizen').get(username=username)
        # profile_id = Profile.objects.values('id', 'ward_id', 'user_id', 'phone', 'description').get(user_id=user_id)

        response = {
            'user': user_id,
            # 'profile_id': profile_id,
            'token': get_user_token(user),
        }

        return Response(response)
    else:
        response = {
            'msg': 'Invalid username or password',
        }

        return Response(response)


# {
#     "username": "mike",
#     "password": "123"
# }


@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def ProfileView(request):
    user_id = User.objects.get(id=request.data['user_id'])
    mtaa = Mtaa.objects.get(id=request.data['mtaa'])
    wilaya = Wilaya.objects.get(id=request.data['wilaya'])
    kata = Kata.objects.get(id=request.data['kata'])

    profile = Profile.objects.create(user_id=user_id, mtaa=mtaa, wilaya=wilaya, kata=kata)
    profile.save()
    response = {
        'msg': 'Successful creating profile',
    }

    return Response(response)

# {
#     "user_id": 1,
#     "mtaa": 1,
#     "kata": 1,
#     "wilaya": 1
# }

@api_view(['GET'])
@permission_classes([AllowAny])
def SaveMikoa(request):
    dist = tanzania.get('Dar-es-salaam').districts
    # mk = Mkoa.objects.get(id=ml['id'])
    districtss = [entry for entry in dist]
    print(districtss)
    dataD = []
    for z in districtss:
        # d = districtss[z]
        w_tosave = Wilaya.objects.create(name=z)
        w_tosave.save()
        x = Wilaya.objects.values('id', 'name').get(name=z)
    dist = Wilaya.objects.values('name', 'id').all()
    x = [a for a in dist]
    for u in x:
        s = tanzania.get('Dar-es-salaam').districts.get(u['name']).wards
        print(s)
        wilay = Wilaya.objects.get(id=u['id'])
        # sl = [z for z in s]
        for i  in s:
            print(i)
            data = Kata.objects.create(wilaya_id=wilay, name=i)
    # data.append({'id': ml['id'], 'name': ml['name'], 'districts': dataD})
    print("saved district")
    return Response(data)