from django.urls import path
from .views import MemberInfoView
from .views import MemberUpdateView
from .views import ImportDataView
from .views import upload_file
from .views import get_member_info_csv
from .views import MemberInfoList

app_name = "app_member"

urlpatterns = [
    path('info/', MemberInfoView.as_view(), name='info'),
    path('update/', MemberUpdateView.as_view(), name="update"),
    path('import/', ImportDataView.as_view(), name="import"),
    path('upload_file/', upload_file, name='upload_file'),
    path('downinfo/', get_member_info_csv, name='downinfo'),
    path('infolist/', MemberInfoList.as_view(), name='infolist')
]