from django.urls import path
from .views import RegisterUser, LoginView, ProfileView, SaveMikoa
from rest_framework_simplejwt import views as jwt_views

app_name = 'authUser'

urlpatterns = [
    path('register', RegisterUser),
    path('login', LoginView),
    path('create_profile', ProfileView),
    path('refresh_token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('x', SaveMikoa)
]
