from django.urls import path
from core.views import *

app_name = 'core'
urlpatterns = [
    path('', URLListView.as_view(), name='url_list'),
    path('create', URLCreateView.as_view(), name='url_create'),
    path('update/<int:pk>', update, name='url_update'),
]
