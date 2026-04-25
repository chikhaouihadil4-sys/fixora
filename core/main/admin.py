from django.contrib import admin
from .models import Artisan, Review

@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'city', 'is_approved')  # باش تشوف الاسم والخدمة والمدينة والحالة
    list_filter = ('is_approved', 'city', 'service')          # باش تصفّي حسب الموافقة أو المدينة أو الخدمة
    search_fields = ('name', 'service', 'city')              # باش تقدّر تبحث بسهولة

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'artisan', 'rating')


