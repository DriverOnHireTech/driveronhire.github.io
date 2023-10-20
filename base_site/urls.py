from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
# from driver_management.views import MyModelList, DriverDetailsView
from enquiry.views import MyEnquiryList, MyEnquiryDelete, MyEnquiryUpdate, MyEnquiryGetList

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from user_master.views import home

schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    path("", home, name='home'),
    path("admin/", admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', include('user_master.urls')),
    path('api/booking/', include('booking.urls')),


    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),
    path('driver/', include('driver_management.urls')),
    path('api/enquiry/', MyEnquiryList.as_view(), name='enquiry-list'),
    path('api/enquiry/<int:id>', MyEnquiryGetList.as_view(), name='enquiry-list-id'),
    path('api/enquiry/<int:id>/update', MyEnquiryUpdate.as_view(), name='enquiry-update-list'),
    path('api/enquiry/<int:id>/delete', MyEnquiryDelete.as_view(), name='enquiry-delete-list'),
    path('auth/', include('authentication.urls')),
     path('api/enquiry/', include('enquiry.urls')), 
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)