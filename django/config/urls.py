from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
#from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
] + static('/static/', document_root='static')