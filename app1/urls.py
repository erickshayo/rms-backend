from django.urls import path
from .views import *

app_name = 'app1'

urlpatterns = [
    path('wilaya', getWilaya),
    path('kata', getKata),
    path('mtaa', getMtaa),
    path('get_wilaya_info', getWilayaInfo),
    path('get_kata_info', getKataInfo),
    path('get_mtaa_info', getMtaaInfo),
    path('addCitizen', createCitizen),
    path('wilaya', getWilaya),
    path('kata/<int:id>', getKata),
    path('mtaa/<int:id>', getMtaa),
    path('get_all_citizens', get_all_citizens),
    path('citizen/<str:pk>', CitizenDetails.as_view())

]
