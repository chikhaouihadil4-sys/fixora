from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', views.login_user, name='login'),
    path('register_user/', views.register_user, name='register_user'),
    path('register_artisan/', views.register_artisan, name='register_artisan'),

    
    path('profile/<int:id>/', views.profile, name='profile'),

    path('add_review/<int:id>/', views.add_review, name='add_review'),
    path('search/', views.search_results, name='search_results'),

    path('logout/', views.logout_user, name='logout'),

    path('request_service/<int:id>/', views.request_service, name='request_service'),
    path('artisan_requests/', views.artisan_requests, name='artisan_requests'),

    path('accept_request/<int:id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:id>/', views.reject_request, name='reject_request'),

    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('user-history/', views.user_history, name='user_history'),
    path('artisan-history/', views.artisan_history, name='artisan_history'),

    # Complaints
    path('complaint/user/<int:id>/', views.send_complaint, {'target_type': 'user'}, name='send_complaint_user'),
    path('complaint/artisan/<int:id>/', views.send_complaint, {'target_type': 'artisan'}, name='send_complaint_artisan'),
    path('complaints/history/', views.complaints_history, name='complaints_history'),

    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('accept-complaint/<int:id>/', views.accept_complaint, name='accept_complaint'),
    path('reject-complaint/<int:id>/', views.reject_complaint, name='reject_complaint'),
    path('block/artisan/<int:id>/', views.block_artisan, name='block_artisan'),
    path('artisan/approve/<int:id>/', views.accept_artisan, name='approve_artisan'),
    path('artisan/reject/<int:id>/', views.reject_artisan, name='reject_artisan'),
    path('block-user/<int:id>/', views.block_user, name='block_user'),
    path('unblock-user/<int:id>/', views.unblock_user, name='unblock_user'),

    path('block-artisan/<int:id>/', views.block_artisan, name='block_artisan'),
    path('unblock-artisan/<int:id>/', views.unblock_artisan, name='unblock_artisan'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)