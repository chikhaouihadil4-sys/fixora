from django.contrib import admin
from .models import Artisan, Service, Review, ServiceRequest, Complaint


@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'status', 'rating', 'is_blocked')
    list_filter = ('status', 'is_blocked')
    search_fields = ('name', 'city', 'phone')
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'artisan')
    list_filter = ('artisan',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'artisan', 'rating')


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'artisan', 'service', 'status', 'created_at')
    list_filter = ('status', 'artisan')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = ('id', 'get_sender', 'get_target', 'service', 'reason', 'status', 'created_at')
    list_filter = ('status', 'sender_type')
    search_fields = ('service', 'reason')

    actions = ['accept_complaints', 'reject_complaints']

    def get_sender(self, obj):
        if obj.sender_type == "user":
            return obj.user.username if obj.user else "-"
        return obj.artisan.name if obj.artisan else "-"

    def get_target(self, obj):
        if obj.sender_type == "user":
            return obj.artisan.name if obj.artisan else "-"
        return obj.user.username if obj.user else "-"

    def accept_complaints(self, request, queryset):
        for c in queryset:
            c.status = 'accepted'
            c.save()

            if c.artisan:
                c.artisan.is_blocked = True
                c.artisan.save()

    def reject_complaints(self, request, queryset):
        for c in queryset:
            c.status = 'rejected'
            c.save()