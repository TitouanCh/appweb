from django.urls import path
from authentication.views import *

urlpatterns = [
        path('login/', login_view, name='login'),
        path('logout/', logout_view, name='logout'),
        path('signup/', signup_view, name='signup'),
        path('profile/', profile_view, name='profile'),
        path('role-requests/', request_view, name='role-request'),
        path('process-request/', process_request, name='process-request'),
        ]
