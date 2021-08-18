from django.urls import path, include
from django.conf.urls import url
from users import views
from users.knox_views import views as _views

app_name = 'users'


urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='create'),
    path('send/otp/', views.SendOTPView.as_view(), name='send'),
    path('verify/otp/', views.VerifyOTPView.as_view(), name='verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', _views.LogoutView.as_view(), name='logout'),
]