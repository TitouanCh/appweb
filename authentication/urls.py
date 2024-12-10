from django.urls import path
from authentication.views import *

urlpatterns = [
        path('login/', login_view, name='login'),
        path('logout/', logout_view, name='logout'),
        path('signup/', signup_view, name='signup')
        ]
