from django.urls import path
from .import views

urlpatterns=[
    path('send_email/', views.senddriverenquiry.as_view(), name='send_email'),
    path('single_enq/<int:id>/', views.Getsingle_enq.as_view(), name='single_enq'), # For Reterive single enquiry
    # path()
]