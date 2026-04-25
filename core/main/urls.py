from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', views.login_user, name='login'),
    
    path('register_user/', views.register_user, name='register_user'),

    path('register_artisan/', views.register_artisan, name='register_artisan'),

    path('results/', views.results, name='results'),

    path('profile/<int:id>/', views.profile, name='profile'),

    path('add_review/<int:id>/', views.add_review, name='add_review'),
    
    path('search/', views.search_results, name='search_results'),
      
    path('logout/', views.logout_user, name='logout'),

    
      

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
