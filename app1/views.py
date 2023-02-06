from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authUser.models import User
from .serializer import CitizenSerializer
# Create your views here.

@api_view(["GET"])
@permission_classes([AllowAny])
def getWilaya(request):
    data = Wilaya.objects.values('id', 'name').all()
    response = {"data": data}
    return Response(response)


@api_view(["POST"])
@permission_classes([AllowAny])
def getKata(request):
    wilaya = Wilaya.objects.get(id=request.data['wilaya_id'])
    data = Kata.objects.values('id', 'name').filter(id=wilaya)
    response = {"data": data}
    return Response(response)


# {
#     "wilaya_id": 1
# }
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_citizens(request):
    data = Citizen.objects.values('id','nida','firstname','lastname','gender','email','phone_no','wilaya','kata','mtaa','house_no').all()
    c = request.GET.get('c', None)
    print(c)
    if c is not None:
        data = data.filter(id=c)
    d = [e for e in data]
    z=[]
    for i in d:
        wilaya = Wilaya.objects.values('name').get(id=i['wilaya'])
        kata = Kata.objects.values('name').get(id=i['kata'])
        mtaa = Mtaa.objects.values('name').get(id=i['mtaa'])
        data2 = {
            'id': i['id'],
            'nida': i['nida'],
            'firstname':i['firstname'],
            'lastname': i['lastname'],
            'gender': i['gender'],
            'email': i['email'],
            'phone_no': i['phone_no'],
            'wilaya':wilaya['name'],
            'kata': kata['name'],
            'mtaa': mtaa['name'],
            'house_no': i['house_no'],
        }
        z.append(data2)
    return Response(z)

class CitizenDetails(APIView):
    def get(self, request, pk):
        try:
            citizen = Citizen.objects.get(id=pk)
        except Citizen.DoesNotExist:
            return Response("Citizen not found", status=404)
        serializer = CitizenSerializer(instance=citizen, many=False)
        return Response(serializer.data)
    def put(self, request, pk):
        try:
            citizen = Citizen.objects.get(id=pk)
        except Citizen.DoesNotExist:
            return Response("Citizen not found", status=404)

        serializer = CitizenSerializer(instance=citizen, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True})
        return Response(serializer.errors)

@api_view(["POST"])
@permission_classes([AllowAny])
def getMtaa(request):
    kata = Kata.objects.get(id=request.data['kata_id'])
    data = Mtaa.objects.values('id', 'name').filter(id=kata)
    response = {"data": data}
    return Response(response)


# {
#     "kata_id": 1
# }


@api_view(["POST"])
@permission_classes([AllowAny])
def createCitizen(request):
    print(request.data)
    kata = Kata.objects.get(id=request.data['kata'])
    mtaa = Mtaa.objects.get(id=request.data['mtaa'])
    wilaya = Wilaya.objects.get(id=request.data['wilaya'])
    #
    print(wilaya)
    citizen = Citizen.objects.create(
        nida=request.data['nida'], firstname=request.data['firstname'],
        lastname=request.data['lastname'], kata=kata, mtaa=mtaa, wilaya=wilaya,
        phone_no=request.data['phone_no'], email=request.data['email'],
        gender=request.data['gender'], house_no=request.data['house_no']
    )
    citizen.save()
    user = User()
    user.username = request.data['email']
    user.email = request.data['email']
    user.set_password(request.data['phone_no'])
    user.citizen = citizen
    user.save()
    response = {"data": "successful save"}
    return Response(response)


# {
#     "nida": "2020020200202022",
#     "firstname": "mike",
#     "lastname": "cyril",
#     "mtaa": 1,
#     "kata": 1,
#     "wilaya": 1
# }


@api_view(["POST"])
@permission_classes([AllowAny])
def getWilayaInfo(request):
    wilaya = Wilaya.objects.get(id=request.data['wilaya_id'])
    citizen = Citizen.objects.values('id', 'nida', 'firstname',
                                     'lastname', 'mtaa', 'kata',
                                     'wilaya').filter(wilaya=wilaya)
    a = [entry for entry in citizen]
    b = []
    for c in a:
        data = {
            'nida': c['nida'],
            'firstname': c['firstname'],
            'lastname': c['lastname'],
            'mtaa': Mtaa.objects.values('name').get(id=c['mtaa'])['name'],
            'kata': Kata.objects('name').get(id=c['name'])['name'],
            'wilaya': Wilaya.objects('name').get(id=c['name'])['name']
        }
        b.append(data)

    response = {
        "number_of_citizens": len(a),
        "citizen_list": b
    }
    return Response(response)


# {
#     "wilaya_id": 1
# }

@api_view(["POST"])
@permission_classes([AllowAny])
def getKataInfo(request):
    kata = Kata.objects.get(id=request.data['kata_id'])
    citizen = Citizen.objects.values('id', 'nida', 'firstname',
                                     'lastname', 'mtaa', 'kata',
                                     'wilaya').filter(kata=kata)
    a = [entry for entry in citizen]
    b = []
    for c in a:
        data = {
            'nida': c['nida'],
            'firstname': c['firstname'],
            'lastname': c['lastname'],
            'mtaa': Mtaa.objects.values('name').get(id=c['mtaa'])['name'],
            'kata': Kata.objects('name').get(id=c['name'])['name'],
            'wilaya': Wilaya.objects('name').get(id=c['name'])['name']
        }
        b.append(data)

    response = {
        "number_of_citizens": len(a),
        "citizen_list": b
    }
    return Response(response)


# {
#     "kata_id": 1
# }


@api_view(["POST"])
@permission_classes([AllowAny])
def getMtaaInfo(request):
    mtaa = Mtaa.objects.get(id=request.data['mtaa_id'])
    citizen = Citizen.objects.values('id', 'nida', 'firstname',
                                     'lastname', 'mtaa', 'kata',
                                     'wilaya').filter(mtaa=mtaa)
    a = [entry for entry in citizen]
    b = []
    for c in a:
        data = {
            'nida': c['nida'],
            'firstname': c['firstname'],
            'lastname': c['lastname'],
            'mtaa': Mtaa.objects.values('name').get(id=c['mtaa'])['name'],
            'kata': Kata.objects('name').get(id=c['name'])['name'],
            'wilaya': Wilaya.objects('name').get(id=c['name'])['name']
        }
        b.append(data)

    response = {
        "number_of_citizens": len(a),
        "citizen_list": b
    }
    return Response(response)

# {
#     "mtaa_id": 1
# }



@api_view(["GET"])
@permission_classes([AllowAny])
def getWilaya(request):
    wilaya = Wilaya.objects.values('id', 'name').all()
    response = wilaya
    return Response(response)




@api_view(["GET"])
@permission_classes([AllowAny])
def getKata(request,id):
    wilaya = Wilaya.objects.get(id=id)
    kata = Kata.objects.values('id', 'name').filter(wilaya_id=wilaya)
    response = {
        'kata': kata
    }
    return Response(response)
# {
#     "wilaya_id": 1
# }

@api_view(["GET"])
@permission_classes([AllowAny])
def getMtaa(request, id):
    kata = Kata.objects.get(id=id)
    mtaa = Mtaa.objects.values('id', 'name').filter(kata_id=kata)
    response = {
        'mtaa': mtaa
    }
    return Response(response)
# {
#     "kata_id": 1
# }