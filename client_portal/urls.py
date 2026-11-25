from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='client_register'),
    path('login/', auth_views.LoginView.as_view(template_name='client_portal/login.html'), name='client_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='client_logout'),
    path('dashboard/', views.dashboard, name='client_dashboard'),
    path('project-submit/', views.project_submit, name='project_submit'),
    path('quotations/', views.my_quotations, name='my_quotations'),
    path('messages/', views.message_inbox, name='message_inbox'),
    path('messages/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
]

urlpatterns += [
    path(
        'messages/<int:conversation_id>/updates/',
        views.conversation_updates,
        name='conversation_updates'
    ),
    path(
        'notifications/count/',
        views.notification_count,
        name='notification_count'
    ),
]
