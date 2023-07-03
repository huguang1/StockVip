from django.urls import path

from .views import IndexHandle
from .views import logout
from .views import LoginHandle

app_name = "app_index"


urlpatterns = [
    path('', IndexHandle.as_view(), name="index"),
    path('logout/', logout, name='logout'),
    path('login/', LoginHandle.as_view(), name='login')
]
