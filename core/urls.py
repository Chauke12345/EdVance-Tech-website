from django.urls import path
from . import views, staff_views

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.packages, name='packages'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('staff/', staff_views.staff_dashboard, name='staff_dashboard'),

    path('staff/enquiries/', staff_views.staff_enquiry_list, name='staff_enquiry_list'),
    path('staff/enquiries/<int:enquiry_id>/', staff_views.staff_enquiry_detail, name='staff_enquiry_detail'),
    path('staff/enquiries/<int:enquiry_id>/review/', staff_views.staff_enquiry_review, name='staff_enquiry_review'),

    path('staff/clients/', staff_views.staff_client_list, name='staff_client_list'),
    path('staff/clients/<int:client_id>/', staff_views.staff_client_detail, name='staff_client_detail'),

    path('staff/quotations/', staff_views.staff_quotation_list, name='staff_quotation_list'),
    path('staff/quotations/create/', staff_views.staff_quotation_create, name='staff_quotation_create'),
    path('staff/quotations/<int:quotation_id>/', staff_views.staff_quotation_detail, name='staff_quotation_detail'),

    path('staff/projects/', staff_views.staff_project_list, name='staff_project_list'),
    path('staff/projects/<int:project_id>/', staff_views.staff_project_detail, name='staff_project_detail'),
]
