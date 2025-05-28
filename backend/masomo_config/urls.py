from django.contrib import admin
from django.urls import path, include  # Ensure to import 'include'
from students.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL
    path('', include('students.urls', namespace='students')),  # students app URLs
    path('teachers/', include('teachers.urls')),  # teachers app URLs

    # Authentication
    path('login/',  CustomLoginView.as_view(),  name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
]
