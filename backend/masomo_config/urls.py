from django.contrib import admin
from django.urls import path, include  # Ensure to import 'include'
from students.views import CustomLoginView, CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL
    path('', include('students.urls', namespace='students')),  # students app URLs
    path('teachers/', include('teachers.urls')),  # teachers app URLs

    # Authentication
    path('login/',  CustomLoginView.as_view(),  name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)