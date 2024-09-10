from django.urls import path
from inquiries.views import (AcademicRequestsCreateView,
                             AcademicRequestsUpdateView,AcademicRequestsListView,AcademicRequestsDeleteView,
                             AdmininstrativeRequestsListView,AdministrativeRequestsCreateView,
                             AdministrativeRequestsDeleteView,AdministrativeRequestsUpdateView)

urlpatterns = [
    path('academicrequest/new/',AcademicRequestsCreateView.as_view(),name ='academic-requests-create'),
    path('academicrequest/<int:pk>/update/',AcademicRequestsUpdateView.as_view(),name ='academic-requests-update'),
    path('academicrequest/<int:pk>/delete/',AcademicRequestsDeleteView.as_view(),name='academic-requests-delete'),
    path('academicrequest/',AcademicRequestsListView.as_view(),name='academic-requests-list'),
    path('adminrequest/new/',AdministrativeRequestsCreateView.as_view(),name='admin-requests-create'),
    path('adminrequest/<int:pk>/update/',AdministrativeRequestsUpdateView.as_view(),name='admin-requests-update'),
    path('adminrequest/<int:pk>/delete/',AdministrativeRequestsDeleteView.as_view(),name='admin-requests-delete'),
    path('adminrequest/',AdmininstrativeRequestsListView.as_view(),name='admin-requests-list'),
]
