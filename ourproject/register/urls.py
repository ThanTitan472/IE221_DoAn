from django.urls import path
from .views import *


urlpatterns = [

path('', register, name='register'),
path('login/', login_view, name='login'),
path('logout/', logout, name='logout'),

]