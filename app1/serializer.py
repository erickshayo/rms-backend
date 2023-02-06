from rest_framework.serializers import ModelSerializer
from app1.models import Citizen

class CitizenSerializer(ModelSerializer):
    class Meta:
        model = Citizen
        fields = '__all__'
