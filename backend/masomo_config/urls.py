from django.contrib import admin
from django.urls import path, include  # Ensure to import 'include'

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL
    path('', include('students.urls')),  # Include the students app URLs
    
]
